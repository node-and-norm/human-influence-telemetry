#!/usr/bin/env python3
"""Additive file and dependency checks; preserve the historical gate evaluator."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "9af12f6cb891288f692990366e54b85bd21d9e24"
MAP = "evidence/claim-evidence-map.json"
BINDINGS = "evidence/research-integrity-bindings.json"
COMPARISON = "validation/results/pre-adjudication-comparison.json"
PRESERVATION = "validation/results/preservation-manifest.json"
EXECUTION = "validation/results/pre-adjudication-execution-record.json"
LOCKED_SHA = "91b28ec23f6f446be3ccd4868d9975a7f143da917de87ab5c2f5ac0123b3ced2"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()


def decoded(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda _: require(False, "nonfinite JSON value"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_path(root, value):
    require(isinstance(value, str) and value and "\\" not in value, "unsafe repository path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and not any(p in ("", ".", "..") for p in value.split("/"))
            and not any(ord(c) < 32 for c in value), "unsafe repository path")
    target = root / value
    require(target.resolve().is_relative_to(root.resolve()), "path escapes repository")
    cursor = target
    while cursor != root:
        require(not cursor.is_symlink(), "symlink input is prohibited")
        cursor = cursor.parent
    require(target.is_file(), "missing evidence file")
    return target


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL)


def tracked_bytes(root, path):
    target = safe_path(root, path)
    entry = git(root, "ls-files", "--stage", "--error-unmatch", "--", path)
    require(entry.startswith((b"100644 ", b"100755 ")) and entry.count(b"\n") == 1,
            "evidence is not one tracked regular file")
    return target.read_bytes()


def inspect_map(data):
    require(isinstance(data, dict) and isinstance(data.get("claims"), list) and data["claims"], "missing claims")
    claims, evidence_ids, bindings = {}, set(), []
    for claim in data["claims"]:
        require(isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
                and claim["claim_id"].strip() and claim["claim_id"] not in claims, "duplicate or invalid claim ID")
        claims[claim["claim_id"]] = claim
        evidence = claim.get("evidence")
        require(isinstance(evidence, list) and evidence, "missing evidence references")
        for item in evidence:
            require(isinstance(item, dict) and isinstance(item.get("evidence_id"), str)
                    and item["evidence_id"].strip() and item["evidence_id"] not in evidence_ids, "duplicate or invalid evidence ID")
            evidence_ids.add(item["evidence_id"])
            require(isinstance(item.get("path"), str) and item["path"], "missing evidence path")
            require(item.get("integrity") in ("git_tracked", "locked_digest"), "unsupported integrity declaration")
            if item["integrity"] == "locked_digest":
                require(item["path"] == COMPARISON, "unknown locked evidence binding")
            bindings.append({"claim_id": claim["claim_id"], "evidence_id": item["evidence_id"],
                             "path": item["path"], "integrity_declaration": item["integrity"]})
    dependencies = {}
    for claim_id, claim in claims.items():
        refs = claim.get("dependencies")
        require(isinstance(refs, list) and all(isinstance(ref, str) and ref in claims for ref in refs), "unknown dependency reference")
        require(len(refs) == len(set(refs)), "duplicate dependency reference")
        require(claim_id not in refs, "self dependency")
        dependencies[claim_id] = set(refs)
    remaining = set(claims)
    while remaining:
        ready = {claim_id for claim_id in remaining if not (dependencies[claim_id] & remaining)}
        require(ready, "dependency cycle")
        remaining -= ready
    return bindings


def check_locked(comparison, preservation, execution):
    require(sha(comparison) == LOCKED_SHA, "locked comparison digest mismatch")
    entries = [item for item in preservation.get("files", []) if item.get("role") == "comparison/json"]
    require(len(entries) == 1 and entries[0].get("filename") == Path(COMPARISON).name
            and entries[0].get("sha256") == LOCKED_SHA and entries[0].get("size_bytes") == len(comparison), "preservation record does not bind the locked comparison")
    outputs = execution.get("outputs", {})
    require(outputs.get("json_filename") == Path(COMPARISON).name and outputs.get("json_sha256") == LOCKED_SHA,
            "execution record does not bind the locked comparison")


def build(root=ROOT):
    root = root.resolve()
    raw_map = tracked_bytes(root, MAP)
    bindings = inspect_map(decoded(raw_map))  # Check cycles directly before frozen-map comparison.
    require(raw_map == git(root, "show", f"{BASE_COMMIT}:{MAP}"), "claim map differs from frozen base")
    paths = sorted({item["path"] for item in bindings} | {PRESERVATION, EXECUTION, COMPARISON})
    raw_files = {}
    for path in paths:
        raw = tracked_bytes(root, path)
        require(raw == git(root, "show", f"{BASE_COMMIT}:{path}"), "evidence differs from frozen base")
        raw_files[path] = raw
    check_locked(raw_files[COMPARISON], decoded(raw_files[PRESERVATION]), decoded(raw_files[EXECUTION]))
    return {"binding_id": "HIT-RESEARCH-INTEGRITY-BINDINGS-001", "prepared_date": "2026-10-08",
            "base_commit": BASE_COMMIT, "check_kind": "file_and_dependency_consistency_only",
            "claim_map": {"path": MAP, "sha256": sha(raw_map)}, "evidence_bindings": bindings,
            "files": [{"path": path, "sha256": sha(raw_files[path])} for path in paths],
            "locked_comparison": {"path": COMPARISON, "sha256": LOCKED_SHA,
                                  "preservation_record": PRESERVATION, "execution_record": EXECUTION},
            "human_support_review_validated": False, "evidence_fitness_validated": False,
            "source_truth_validated": False, "conclusion_eligibility_recomputed": False}


def evaluate(root=ROOT, prepare=False):
    bindings = build(root)
    path = root / BINDINGS
    if prepare:
        require(not path.exists() and not path.is_symlink(), "bindings already exist; preserve the recorded freeze")
        path.write_bytes(encoded(bindings))
    require(safe_path(root.resolve(), BINDINGS).read_bytes() == encoded(bindings), "missing or altered mandatory bindings")
    return {"check_kind": "file_and_dependency_consistency_only", "claim_count": len({b["claim_id"] for b in bindings["evidence_bindings"]}),
            "evidence_binding_count": len(bindings["evidence_bindings"]), "file_count": len(bindings["files"]),
            "human_support_review_validated": False, "evidence_fitness_validated": False,
            "source_truth_validated": False, "conclusion_eligibility_recomputed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        result = evaluate(prepare=args.prepare)
    except (ValueError, TypeError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {type(exc).__name__}; inspect tracked file bindings and claim dependencies")
        return 1
    print(f"File and dependency consistency only: PASS; {result['claim_count']} claims, {result['evidence_binding_count']} evidence bindings; human review and fitness were not validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
