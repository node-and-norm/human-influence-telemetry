#!/usr/bin/env python3
"""Negative controls for development-exhibit file verification."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

import render_development_figures as figures


class FigureChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        data = figures.load_data()
        names = [figures.DATA, figures.GENERATOR, figures.REQUIREMENTS, figures.MANIFEST]
        names += [item["path"] for item in data["source_bindings"]]
        names += [f"{figures.DIRECTORY}/{name}.{suffix}" for name in figures.EXHIBITS for suffix in ("svg", "png")]
        for name in names:
            target = self.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(figures.ROOT/name, target)

    def read_json(self, path):
        return json.loads((self.root/path).read_text())

    def write_json(self, path, data):
        (self.root/path).write_text(json.dumps(data))

    def test_saved_artifacts_pass_without_render_dependencies(self):
        figures.check(self.root)

    def test_changed_source_fails(self):
        source = self.root/"SPECIFICATION.md"
        source.write_bytes(source.read_bytes()+b"\nchanged\n")
        with self.assertRaisesRegex(ValueError, "stale source binding"):
            figures.check(self.root)

    def test_changed_figure_fails(self):
        source = self.root/f"{figures.DIRECTORY}/assessment-architecture.svg"
        source.write_bytes(source.read_bytes()+b"\n")
        with self.assertRaisesRegex(ValueError, "changed saved artifact"):
            figures.check(self.root)

    def test_changed_generator_fails(self):
        source = self.root/figures.GENERATOR
        source.write_bytes(source.read_bytes()+b"\n")
        with self.assertRaisesRegex(ValueError, "changed saved artifact"):
            figures.check(self.root)

    def test_unknown_manifest_rejected(self):
        manifest = self.read_json(figures.MANIFEST)
        manifest["schema_version"] = 2
        self.write_json(figures.MANIFEST, manifest)
        with self.assertRaisesRegex(ValueError, "unknown manifest"):
            figures.check(self.root)

    def test_extra_manifest_output_rejected(self):
        manifest = self.read_json(figures.MANIFEST)
        manifest["outputs"]["../outside"] = "0"*64
        self.write_json(figures.MANIFEST, manifest)
        with self.assertRaisesRegex(ValueError, "unexpected manifest outputs"):
            figures.check(self.root)

    def test_promotion_rejected_before_hash_check(self):
        data = self.read_json(figures.DATA)
        data["scientific_conclusion_eligible"] = True
        self.write_json(figures.DATA, data)
        with self.assertRaisesRegex(ValueError, "cannot promote"):
            figures.check(self.root)

    def test_projection_scope_rejected(self):
        data = self.read_json(figures.DATA)
        data["figures"][2]["projection_fields"].append("rationale")
        self.write_json(figures.DATA, data)
        with self.assertRaisesRegex(ValueError, "projection boundary"):
            figures.load_data(self.root)

    def test_unknown_source_reference_rejected(self):
        data = self.read_json(figures.DATA)
        data["figures"][0]["source_refs"] = [99]
        self.write_json(figures.DATA, data)
        with self.assertRaisesRegex(ValueError, "invalid figure source reference"):
            figures.load_data(self.root)

    def test_duplicate_source_binding_rejected(self):
        data = self.read_json(figures.DATA)
        data["source_bindings"][1] = data["source_bindings"][0]
        self.write_json(figures.DATA, data)
        with self.assertRaisesRegex(ValueError, "nine distinct"):
            figures.load_data(self.root)

    def test_traversal_rejected(self):
        for relative in ("../outside", "/tmp/outside", "x/../SPECIFICATION.md", "x\\..\\outside"):
            with self.subTest(relative=relative), self.assertRaisesRegex(ValueError, "unsafe path"):
                figures.checked_path(self.root, relative)

    def test_symlink_rejected(self):
        path = self.root/"link"
        path.symlink_to(self.root/"SPECIFICATION.md")
        with self.assertRaisesRegex(ValueError, "symlink input"):
            figures.checked_path(self.root, "link")

    def test_missing_accessible_description_rejected(self):
        relative = f"{figures.DIRECTORY}/assessment-architecture.svg"
        path = self.root/relative
        path.write_text(path.read_text().replace('<desc id="figure-description">', "<desc>"))
        manifest = self.read_json(figures.MANIFEST)
        manifest["outputs"][relative] = figures.digest(path.read_bytes())
        self.write_json(figures.MANIFEST, manifest)
        with self.assertRaisesRegex(ValueError, "accessible description missing"):
            figures.check(self.root)

    def test_check_failure_never_regenerates_manifest(self):
        manifest_before = (self.root/figures.MANIFEST).read_bytes()
        (self.root/f"{figures.DIRECTORY}/ofqual-actor-time.png").write_bytes(b"changed")
        with self.assertRaises(ValueError):
            figures.check(self.root)
        self.assertEqual(manifest_before, (self.root/figures.MANIFEST).read_bytes())


if __name__ == "__main__":
    unittest.main()
