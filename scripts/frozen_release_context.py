"""Resolve three historical inputs without exempting current release checks."""
from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
import subprocess

BASE_COMMIT = "9af12f6cb891288f692990366e54b85bd21d9e24"
AMENDMENT_PATH = "release/v0.6.7/frozen-input-amendment.json"
AMENDMENT_ID = "HIT-FROZEN-RELEASE-CONTEXT-067-001"
SNAPSHOTS = {
    "RESEARCH.md": ("release/v0.6.7/frozen-context/RESEARCH.md", "8ab21bb2707790d075ee7f70c06c61064e6b396034c2b344b85425e3f5b4fc2f"),
    "CITATION.cff": ("release/v0.6.7/frozen-context/CITATION.cff", "ed25cfa3e0fc496d051596afc30cf659ae679342316374a80ba69f6ba3d0aef2"),
    ".zenodo.json": ("release/v0.6.7/frozen-context/.zenodo.json", "ca9d546c0ea1296485d7845d56df9c36b4f2f8f51eea57ce7eaff5e3c14e34b4"),
}
EXPECTED_AMENDMENT = {
    "amendment_id": AMENDMENT_ID,
    "release": "0.6.7",
    "base_commit": BASE_COMMIT,
    "scope": "Resolve only the three named historical inputs through exact tracked snapshots of the original base. This amendment does not rehash or replace the original research bindings, extension design or outputs.",
    "resolution": "The historical checks validate the frozen context. Current RESEARCH.md, CITATION.cff and .zenodo.json remain subject to separate current-release metadata checks; this amendment does not validate their present contents.",
    "historical_bindings_and_outputs_unchanged": True,
    "current_release_metadata_validated_here": False,
    "scientific_acceptance_conferred": False,
    "snapshots": [{"original_path": path, "snapshot_path": snapshot, "sha256": digest}
                  for path, (snapshot, digest) in SNAPSHOTS.items()],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL)


def tracked_bytes(root, path):
    root = root.resolve()
    require(isinstance(path, str) and path and "\\" not in path
            and not PurePosixPath(path).is_absolute()
            and not any(part in ("", ".", "..") for part in path.split("/"))
            and not any(ord(c) < 32 for c in path), "Unsafe historical snapshot path")
    target = root / path
    require(target.resolve().is_relative_to(root), "Historical snapshot escapes repository")
    cursor = target
    while cursor != root:
        require(not cursor.is_symlink(), "Historical snapshot symlink prohibited")
        cursor = cursor.parent
    require(target.is_file(), "Missing historical snapshot or amendment")
    entry = git(root, "ls-files", "--stage", "--error-unmatch", "--", path)
    require(entry.startswith((b"100644 ", b"100755 ")) and entry.count(b"\n") == 1,
            "Historical snapshot must be one tracked regular file")
    return target.read_bytes()


def decoded(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate amendment JSON key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: require(False, "Nonfinite amendment JSON value"))


def load_context(root, expected_base):
    require(expected_base == BASE_COMMIT, "Unknown historical snapshot base")
    amendment = decoded(tracked_bytes(root, AMENDMENT_PATH))
    require(json.dumps(amendment, sort_keys=True, allow_nan=False)
            == json.dumps(EXPECTED_AMENDMENT, sort_keys=True, allow_nan=False),
            "Unknown or altered historical snapshot amendment")
    result = {}
    for original, (snapshot, digest) in SNAPSHOTS.items():
        raw = tracked_bytes(root, snapshot)
        require(hashlib.sha256(raw).hexdigest() == digest, "Historical snapshot digest mismatch")
        require(raw == git(root, "show", f"{BASE_COMMIT}:{original}"),
                "Historical snapshot differs from frozen base")
        result[original] = raw
    return result


def disclosure(paths):
    return {"frozen_context_amendment": AMENDMENT_PATH,
            "historical_snapshot_paths": sorted(set(paths) & SNAPSHOTS.keys()),
            "current_release_metadata_validated_here": False}
