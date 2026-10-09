#!/usr/bin/env python3
"""Render bounded development exhibits; verify saved files without dependencies."""
from __future__ import annotations

import argparse
import atexit
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = "figures/development-2026-10-08"
DATA = f"{DIRECTORY}/data.json"
MANIFEST = f"{DIRECTORY}/manifest.json"
GENERATOR = "scripts/render_development_figures.py"
REQUIREMENTS = "requirements-figures.txt"
EXHIBITS = ("assessment-architecture", "ofqual-actor-time", "qualification-preservation")
BOUNDARY_FLAGS = ("adds_empirical_observations", "independent_review",
                  "release_gate_satisfied", "scientific_conclusion_eligible")
STYLE = {"ink": "#183044", "muted": "#526272", "blue": "#205D83",
         "bluewash": "#EFF5F9", "teal": "#17685E", "tealwash": "#EDF6F3",
         "gold": "#8D6027", "goldwash": "#FCF6E9", "line": "#C8D3DA",
         "paper": "#FFFFFF"}


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def checked_path(root: Path, relative: str) -> Path:
    """Reject traversal and symlinks, including symlinked parent directories."""
    if not isinstance(relative, str):
        raise ValueError("path must be text")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "\\" in relative or not pure.parts:
        raise ValueError(f"unsafe path: {relative}")
    current = root.resolve()
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink input: {relative}")
    if not current.is_file():
        raise ValueError(f"missing regular file: {relative}")
    return current


def read_bytes(root: Path, relative: str) -> bytes:
    return checked_path(root, relative).read_bytes()


def load_data(root: Path = ROOT) -> dict:
    data = json.loads(read_bytes(root, DATA))
    if data.get("exhibit_set") != "HIT-DEVELOPMENT-FIGURES-2026-10-08":
        raise ValueError("unknown exhibit set")
    if data.get("status") != "assistant_prepared_development_exhibits_pending_author_review":
        raise ValueError("unexpected review status")
    if any(data.get(flag) is not False for flag in BOUNDARY_FLAGS):
        raise ValueError("exhibits cannot promote evidence or review status")
    if [item.get("id") for item in data.get("figures", [])] != list(EXHIBITS):
        raise ValueError("unexpected or duplicate figure identifiers")
    bindings = data.get("source_bindings", [])
    if len(bindings) != 9 or len({item.get("path") for item in bindings}) != 9:
        raise ValueError("expected nine distinct source bindings")
    for item in bindings:
        if not item.get("locator") or not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", "")):
            raise ValueError("source binding needs a locator and SHA-256")
        if digest(read_bytes(root, item["path"])) != item["sha256"]:
            raise ValueError(f"stale source binding: {item['path']}")
    for figure in data["figures"]:
        for name in ("title", "subtitle", "alt_text", "caption", "footer"):
            if not isinstance(figure.get(name), str) or not figure[name].strip():
                raise ValueError(f"missing figure {name}")
        refs = figure.get("source_refs", [])
        if not refs or any(type(i) is not int or i < 0 or i >= len(bindings) for i in refs):
            raise ValueError("invalid figure source reference")
    if data["figures"][0]["dimensions"] != ["Counsel", "Judgment", "Command", "Correction", "Repair", "Reform"]:
        raise ValueError("six substantive dimensions must remain visible")
    expected_fields = ["dimension", "finding", "evidence_state", "repair_trigger", "unresolved_proposition"]
    if data["figures"][2]["projection_fields"] != expected_fields:
        raise ValueError("projection boundary changed")
    return data


def required_versions(root: Path) -> dict:
    expected = {}
    for line in read_bytes(root, REQUIREMENTS).decode().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not re.fullmatch(r"[A-Za-z0-9_-]+==[A-Za-z0-9.]+", line):
            raise ValueError("rendering dependencies must have exact version pins")
        name, version = line.split("==")
        if name in expected:
            raise ValueError("duplicate rendering dependency")
        expected[name] = version
    return expected


def stack_versions(root: Path) -> dict:
    expected = required_versions(root)
    for name, version in expected.items():
        actual = importlib.metadata.version(name)
        if actual != version:
            raise ValueError(f"rendering requires {name}=={version}; found {actual}")
    return expected


def setup_renderer():
    cache = tempfile.TemporaryDirectory(prefix="hit-publication-fonts-")
    atexit.register(cache.cleanup)
    os.environ.setdefault("MPLCONFIGDIR", cache.name)
    os.environ.setdefault("XDG_CACHE_HOME", cache.name)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
    font_dir = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    fonts = {False: FontProperties(fname=str(font_dir / "DejaVuSans.ttf")),
             True: FontProperties(fname=str(font_dir / "DejaVuSans-Bold.ttf"))}
    plt.rcParams.update({"svg.fonttype": "path", "svg.hashsalt": "hit-development-2026-10-08",
                         "path.simplify": False, "text.usetex": False,
                         "figure.facecolor": "white", "savefig.facecolor": "white"})
    return plt, fonts, FancyArrowPatch, FancyBboxPatch


def render_all(data: dict, root: Path = ROOT) -> tuple[dict, dict]:
    versions = stack_versions(root)
    plt, fonts, Arrow, Box = setup_renderer()
    output = {}
    for item in data["figures"]:
        fig = plt.figure(figsize=(14, 9), dpi=180)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set(xlim=(0, 14), ylim=(0, 9))
        ax.set_axis_off()

        def text(x, y, value, size=11.5, bold=False, color="ink", **kwargs):
            return ax.text(x, y, value, fontsize=size, fontproperties=fonts[bold],
                           color=STYLE.get(color, color), va="top", linespacing=1.55,
                           **kwargs)

        def box(x, y, w, h, wash="bluewash", edge="line"):
            ax.add_patch(Box((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.07",
                             facecolor=STYLE[wash], edgecolor=STYLE[edge], linewidth=0.8))

        def arrow(x1, y1, x2, y2):
            ax.add_patch(Arrow((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=15,
                              color=STYLE["muted"], linewidth=1.25))

        text(.45, 8.60, item["title"], size=21, bold=True)
        text(.45, 8.03, item["subtitle"], size=10.7, color="muted")
        ax.plot([.45, 13.55], [7.67, 7.67], color=STYLE["line"], linewidth=.8)

        if item["id"] == "assessment-architecture":
            text(.45, 7.39, item["human_label"], size=10, bold=True, color="blue")
            for i, step in enumerate(item["steps"]):
                x = .45 + 4.45 * i
                box(x, 5.38, 3.85, 1.62)
                text(x+.18, 6.80, step["title"], size=12.5, bold=True, color="blue")
                text(x+.18, 6.33, step["body"], size=10.7)
                if i < 2:
                    arrow(x+3.92, 6.20, x+4.35, 6.20)
            arrow(11.27, 5.33, 7.8, 4.88)
            box(.45, 2.92, 8.3, 1.90, wash="bluewash")
            text(.63, 4.65, item["record_title"], size=10, bold=True, color="blue")
            text(.63, 4.22, "  ·  ".join(item["dimensions"]), size=11.3, bold=True)
            text(.63, 3.80, item["integrity_title"], size=10.5, bold=True)
            text(.63, 3.46, item["integrity"], size=10.2)
            text(.63, 3.11, item["record_footer"], size=8.8, color="muted")
            box(9.35, 2.92, 4.0, 1.90, wash="goldwash")
            text(9.53, 4.63, item["limits_title"], size=11.5, bold=True, color="gold")
            text(9.53, 4.20, item["limits"], size=10.6)
            arrow(4.60, 2.87, 4.60, 2.42)
            text(.45, 2.27, item["checks_label"], size=10, bold=True, color="teal")
            for i, check in enumerate(item["checks"]):
                x = .45 + i*4.45
                box(x, .61, 3.85, 1.29, wash="tealwash")
                text(x+.18, 1.71, check["title"], size=11.2, bold=True, color="teal")
                text(x+.18, 1.28, check["body"], size=10.0)

        elif item["id"] == "ofqual-actor-time":
            text(.45, 7.39, item["event_label"], size=9.6, bold=True, color="blue")
            for i, event in enumerate(item["events"]):
                x = .45+i*4.45
                box(x, 4.87, 3.85, 2.12)
                text(x+.18, 6.79, event["date"], size=12.1, bold=True, color="blue")
                text(x+.18, 6.37, event["actor"], size=11.7, bold=True)
                text(x+.18, 5.95, event["body"], size=10.3)
                text(x+.18, 5.13, event["refs"], size=8.9, color="muted")
                if i < 2:
                    arrow(x+3.92, 6.04, x+4.35, 6.04)
            text(.45, 4.53, item["source_label"], size=9.6, bold=True, color="teal")
            for i, pub in enumerate(item["publications"]):
                x = .45+i*3.35
                box(x, 2.40, 3.05, 1.75, wash="tealwash")
                text(x+.17, 3.95, pub["date"], size=11.6, bold=True, color="teal")
                text(x+.17, 3.52, pub["body"], size=10.3)
            for i, boundary in enumerate(item["boundaries"]):
                x = .45+i*6.75
                box(x, .65, 6.4, 1.35, wash="goldwash")
                text(x+.18, 1.81, boundary["title"], size=11.3, bold=True, color="gold")
                text(x+.18, 1.37, boundary["body"], size=10.4)

        else:
            widths = [2.58, 3.52, 3.50, 3.50]
            xs = [.45, 3.03, 6.55, 10.05]
            for x, w, heading in zip(xs, widths, item["headers"]):
                box(x, 6.65, w-.04, .67, wash="bluewash")
                text(x+.14, 7.10, heading, size=10.8, bold=True, color="blue")
            for row_number, row in enumerate(item["rows"]):
                top = 6.28-row_number*1.75
                for col, value in enumerate(row):
                    text(xs[col]+.14, top, value, size=10.7 if col else 10.8,
                         bold=col == 0)
                ax.plot([.45, 13.55], [top-1.43, top-1.43], color=STYLE["line"], linewidth=.7)
            box(.45, 1.65, 13.10, 1.05, wash="goldwash")
            text(.64, 2.49, item["projection_title"], size=9.6, bold=True, color="gold")
            text(.64, 2.07, "  |  ".join(item["projection_fields"]), size=11.0)
            text(.45, 1.30, item["boundary"], size=10.6, color="muted")

        text(.45, .27, item["footer"], size=8.1, color="muted")
        svg_buffer, png_buffer = io.BytesIO(), io.BytesIO()
        fig.savefig(svg_buffer, format="svg", metadata={"Date": None,
                    "Creator": "HIT deterministic development-figure renderer"})
        fig.savefig(png_buffer, format="png", dpi=180, metadata={
            "Software": "HIT deterministic development-figure renderer",
            "Title": item["title"], "Description": item["alt_text"]})
        plt.close(fig)
        svg = svg_buffer.getvalue().decode()
        svg = re.sub(r"(<svg\b[^>]*)(>)", r'\1 role="img" aria-labelledby="figure-title figure-description"\2', svg, count=1)
        description = (f'\n <title id="figure-title">{escape(item["title"])}</title>'
                       f'\n <desc id="figure-description">{escape(item["alt_text"])}</desc>')
        svg = re.sub(r"(<svg\b[^>]*>)", lambda match: match.group(1)+description, svg, count=1)
        output[f'{DIRECTORY}/{item["id"]}.svg'] = svg.encode()
        output[f'{DIRECTORY}/{item["id"]}.png'] = png_buffer.getvalue()
    return output, versions


def make_manifest(data: dict, output: dict, versions: dict, root: Path = ROOT) -> dict:
    tracked = [DATA, GENERATOR, REQUIREMENTS]
    return {
        "schema_version": 1,
        "exhibit_set": data["exhibit_set"],
        "scope": "Saved artifact integrity and optional SVG render reproduction; no scientific adjudication.",
        "saved_artifact_check": "SHA-256 of authored inputs, source bindings and all six saved outputs.",
        "render_reproduction_check": "Strict regenerated SVG bytes with pinned Python dependencies; PNG hashes identify saved previews and are not a cross-platform pixel-reproduction claim.",
        "font": "Matplotlib-bundled DejaVu Sans; SVG glyphs converted to paths.",
        "runtime_versions": versions,
        "inputs": {name: digest(read_bytes(root, name)) for name in tracked},
        "outputs": {name: digest(value) for name, value in sorted(output.items())},
    }


def check(root: Path = ROOT, render: bool = False) -> None:
    data = load_data(root)
    manifest = json.loads(read_bytes(root, MANIFEST))
    expected_keys = {"schema_version", "exhibit_set", "scope", "saved_artifact_check",
                     "render_reproduction_check", "font", "runtime_versions", "inputs", "outputs"}
    if set(manifest) != expected_keys or manifest["schema_version"] != 1 or manifest["exhibit_set"] != data["exhibit_set"]:
        raise ValueError("unknown manifest structure or exhibit set")
    if set(manifest["inputs"]) != {DATA, GENERATOR, REQUIREMENTS}:
        raise ValueError("unexpected manifest inputs")
    expected_outputs = {f"{DIRECTORY}/{name}.{suffix}" for name in EXHIBITS for suffix in ("svg", "png")}
    if set(manifest["outputs"]) != expected_outputs:
        raise ValueError("unexpected manifest outputs")
    if manifest["runtime_versions"] != required_versions(root):
        raise ValueError("manifest runtime differs from pinned rendering dependencies")
    for path, expected in {**manifest["inputs"], **manifest["outputs"]}.items():
        if digest(read_bytes(root, path)) != expected:
            raise ValueError(f"changed saved artifact: {path}")
    for name in EXHIBITS:
        svg = read_bytes(root, f"{DIRECTORY}/{name}.svg").decode()
        if '<title id="figure-title">' not in svg or '<desc id="figure-description">' not in svg:
            raise ValueError("SVG accessible description missing")
    if render:
        output, versions = render_all(data, root)
        if versions != manifest["runtime_versions"]:
            raise ValueError("rendering runtime differs from saved manifest")
        for path, value in output.items():
            if path.endswith(".svg") and value != read_bytes(root, path):
                raise ValueError(f"SVG reproduction differs: {path}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Explicitly regenerate figures and manifest after source review")
    mode.add_argument("--check", action="store_true", help="Verify saved artifact hashes using only the standard library")
    mode.add_argument("--render-check", action="store_true", help="Also regenerate and compare SVG bytes in the pinned rendering environment")
    args = parser.parse_args(argv)
    try:
        if args.write:
            data = load_data()
            output, versions = render_all(data)
            manifest = make_manifest(data, output, versions)
            for relative in [*output, MANIFEST]:
                target = ROOT / relative
                if target.is_symlink() or any(parent.is_symlink() for parent in target.parents if parent != ROOT):
                    raise ValueError(f"refusing symlink output: {relative}")
            for relative, value in output.items():
                target = ROOT / relative
                target.write_bytes(value)
            (ROOT / MANIFEST).write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
            print("Wrote three development exhibits and six output artifacts; source bindings preserved.")
        else:
            check(render=args.render_check)
            label = "saved artifact integrity + SVG render reproduction" if args.render_check else "saved artifact integrity"
            print(f"PASS: {label}; no scientific or release-status promotion.")
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError, importlib.metadata.PackageNotFoundError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
