#!/usr/bin/env python3
"""Check additive qualitative-reanalysis records, never their scientific validity."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from frozen_release_context import disclosure, load_context

ROOT = Path(__file__).resolve().parents[1]
BASE = "research/strengthening/solo-002-extension"
ORIGINAL = "research/strengthening/solo-002-complete"
JEV = "research/strengthening/jev-review-001"
BASE_COMMIT = "9af12f6cb891288f692990366e54b85bd21d9e24"
STUDY = "HIT-SOLO-002-EXTENSION-001"
PROTECTED = tuple(f"{ORIGINAL}/{name}" for name in (
    "plan.md", "assessment.draft.json", "source-ledger.md", "baseline-and-review.md",
    "sensitivity.md", "review-status.json", "record-check.json",
)) + tuple(f"{JEV}/{name}" for name in ("sources.json", "design.json", "PROTOCOL.md", "report.md", "run-001/run.json", "run-001/analysis.json")) + (
    "SPECIFICATION.md", "schema/hit-assessment.schema.json", "docs/application-handbook.md",
    "CITATION.cff", ".zenodo.json", "evidence/claim-evidence-map.json", "release/v1.0.0/gate-register.json",
)
INPUTS = (f"{BASE}/PROTOCOL.md", f"{BASE}/design.json", f"{BASE}/formatting.json")
DIMENSIONS = ("counsel", "judgment", "command", "correction", "repair", "reform",
              "institutional_record_integrity", "assessment_packet_integrity")
SOURCE_IDS = ["OFQ-01", "OCR-01", "OFQ-02", "OFQ-03", "DFE-01", "OFQ-04"]
CONDITIONS = [
    {"id": "S05", "kind": "period", "period": {"start": "2020-08-16", "end": "2020-08-16"}, "follow_up_period": None,
     "rule": "Preserve historical event dates; later reporting may establish earlier facts, but later exercise cannot be backdated."},
    {"id": "S06", "kind": "constructed_conflict", "period": {"start": "2020-08-17", "end": "2020-08-17"}, "follow_up_period": {"start": "2020-08-18", "end": "2020-08-20"},
     "synthetic_evidence": "Constructed scenario only, not a historical document: a second account of the same replacement AS/A level grade-issue event states that no replacement AS/A level grades were sent to any schools or colleges on 19 August 2020. Both event accounts are admissible for this scenario, neither has precedence, and no reconciliation is supplied.",
     "preserved_propositions": ["DFE-01 reports issue", "regulatory direction to exam boards", "20 August GCSE issue"],
     "rule": "Reassess material effects; no automatic score or integrity downgrade."},
    {"id": "S07", "kind": "reverse_order_and_whitespace", "formatting_path": f"{BASE}/formatting.json",
     "rule": "All nine retained passages change presentation only; the complete record and six-source ledger remain available."},
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=unique,
                      parse_constant=lambda _: require(False, "Nonfinite JSON value"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def keys(value, names):
    require(isinstance(value, dict) and set(value) == set(names.split()), "Unexpected object fields")


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "Missing narrative")


def read(root, path):
    target = root / path
    require(target.is_file() and not target.is_symlink() and target.resolve().is_relative_to(root.resolve()), "Missing or unsafe input")
    return target.read_bytes()


def committed(root, commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=root, stderr=subprocess.DEVNULL)


def formatting(root):
    packet_path = f"{JEV}/sources.json"
    packet = load(root / packet_path)
    passages = []
    for source in packet["sources"]:
        metadata = {k: v for k, v in source.items() if k != "passages"}
        for passage in source["passages"]:
            require(sha(passage["text"].encode()) == passage["text_sha256"], "Original passage hash mismatch")
            passages.append({"source": metadata, "id": passage["id"], "locator": passage["locator"],
                             "original_text_sha256": passage["text_sha256"], "text": "\n  ".join(passage["text"].split())})
    require(len(passages) == 9 and len({p["id"] for p in passages}) == 9, "Expected nine unique retained passages")
    return {"study_id": STUDY, "condition_id": "S07", "source_packet_path": packet_path,
            "source_packet_sha256": sha(read(root, packet_path)), "packet_scope": packet["scope"],
            "original_passage_order": [p["id"] for p in passages], "passages": list(reversed(passages))}


def expected_design(root, transformed):
    historical = load_context(root, BASE_COMMIT)
    original = load(root / ORIGINAL / "assessment.draft.json")
    claims = [c["claim_id"] for c in original["evidence_claims"]]
    require(len(claims) == 23 and len(set(claims)) == 23, "Expected full 23-claim original record")
    originals = {}
    for path in PROTECTED:
        raw = historical[path] if path in ("CITATION.cff", ".zenodo.json") else read(root, path)
        require(raw == committed(root, BASE_COMMIT, path), "Protected base input changed")
        originals[path] = sha(raw)
    return {"study_id": STUDY, "prepared_date": "2026-10-08", "timezone": "America/New_York",
            "base_commit": BASE_COMMIT, "status": "prepared_inputs_only", "assessor_type": "ai_assistant",
            "prior_jev_results_exposure": True, "independent_review": False, "release_gate_satisfied": False,
            "source_ids": SOURCE_IDS, "claim_ids": claims, "conditions": CONDITIONS,
            "protected_sha256": originals, "protocol_sha256": sha(read(root, f"{BASE}/PROTOCOL.md")),
            "formatting_sha256": sha(encoded(transformed))}


def indexed(rows, field, expected):
    require(isinstance(rows, list) and all(isinstance(row, dict) for row in rows), "Invalid row collection")
    require([row.get(field) for row in rows] == list(expected), "Missing, duplicated, reordered or unknown row ID")
    return rows


def references(values, claims):
    require(isinstance(values, list) and values and all(isinstance(v, str) and v in claims for v in values)
            and len(values) == len(set(values)), "Invalid evidence references")


def check_results(root, results, design):
    keys(results, "study_id protocol_commit assessor_type status independent_review release_gate_satisfied author_adjudication scientific_conclusion_eligible conditions")
    expected = {"study_id": STUDY, "assessor_type": "ai_assistant", "status": "completed_pending_author_review",
                "independent_review": False, "release_gate_satisfied": False,
                "author_adjudication": "pending_for_extension", "scientific_conclusion_eligible": False}
    for key, value in expected.items():
        require(type(results[key]) is type(value) and results[key] == value, "Unsupported status promotion")
    commit = results["protocol_commit"]
    require(isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit), "Missing full protocol commit")
    for path in INPUTS:
        require(read(root, path) == committed(root, commit, path), "Result protocol commit does not bind current inputs")
    for condition in indexed(results["conditions"], "id", ("S05", "S06", "S07")):
        keys(condition, "id questions impacts overall_interpretation limitations")
        for question in indexed(condition["questions"], "id", (f"Q{n}" for n in range(1, 7))):
            keys(question, "id baseline_answer hit_answer comparison reason evidence_refs")
            for field in ("baseline_answer", "hit_answer", "reason"):
                text(question[field])
            require(question["comparison"] in ("tie", "added_distinction", "loss", "unresolved"), "Unknown proposed comparison")
            references(question["evidence_refs"], design["claim_ids"])
        for impact in indexed(condition["impacts"], "dimension", DIMENSIONS):
            keys(impact, "dimension disposition reason evidence_refs")
            require(impact["disposition"] in ("unchanged", "reassess", "unresolved"), "Unknown narrative impact")
            text(impact["reason"])
            references(impact["evidence_refs"], design["claim_ids"])
        text(condition["overall_interpretation"])
        require(isinstance(condition["limitations"], list) and condition["limitations"], "Missing limitations")
        for limitation in condition["limitations"]:
            text(limitation)


def evaluate(root=ROOT, prepare=False):
    base = root / BASE
    transformed = formatting(root)
    design = expected_design(root, transformed)
    if prepare:
        require(not any((base / name).exists() for name in ("design.json", "formatting.json", "results.json", "report.md")), "Prepared inputs or results already exist")
        (base / "formatting.json").write_bytes(encoded(transformed))
        (base / "design.json").write_bytes(encoded(design))
    require(read(root, f"{BASE}/formatting.json") == encoded(transformed), "Formatting differs from deterministic transformation")
    require(read(root, f"{BASE}/design.json") == encoded(design), "Design or mandatory input hashes differ")
    results_path = base / "results.json"
    if results_path.exists():
        check_results(root, load(results_path), design)
        require(read(root, f"{BASE}/report.md").strip(), "Missing narrative report")
    return {"check_kind": "qualitative_record_consistency_only", "results_present": results_path.exists(),
            "condition_count": 3, "source_truth_validated": False, "interpretations_recomputed": False,
            "independent_review": False, "author_adjudication": "pending_for_extension", "release_gate_satisfied": False,
            **disclosure(["CITATION.cff", ".zenodo.json"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        report = evaluate(prepare=args.prepare)
    except (ValueError, TypeError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {type(exc).__name__}; inspect extension inputs, frozen bytes and required fields")
        return 1
    state = "assistant results present" if report["results_present"] else "prepared inputs only; no results"
    print(f"Extension consistency: PASS; {state}; interpretation and author review remain pending")
    print("Historical citation and Zenodo inputs resolved through the v0.6.7 snapshot amendment; current release metadata is checked separately")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
