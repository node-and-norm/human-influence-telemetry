#!/usr/bin/env python3
"""Check the draft documentary record and retained bytes, never source truth."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.validation.assessment import validate_assessment

BASE = Path("research/strengthening/solo-002-complete")
PLAN_COMMIT = "43eae81a3a4938a46062d3c1ba41aab6655db11a"
PLAN_SHA256 = "786799a1fb27f40e58a144e60910813dd75217bc9c713bef72cdd8083a06fc66"
FILES = (
    "plan.md", "README.md", "assessment.draft.json", "source-ledger.md",
    "baseline-and-review.md", "sensitivity.md", "review-status.json",
)


def evaluate(root: Path = ROOT) -> dict:
    base = root / BASE
    for name in FILES:
        path = base / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"missing or empty development artifact: {BASE / name}")
    status = json.loads((base / "review-status.json").read_text(encoding="utf-8"))
    required = {
        "status": "draft_pending_author",
        "author_adjudication": "pending",
        "independent_review": False,
        "scientific_conclusion_eligible": False,
        "release_gate_satisfied": False,
        "assessor_type": "ai_assistant",
        "plan_freeze_commit": PLAN_COMMIT,
        "assessment_id": "HIT-SOLO-002-OFQUAL-DRAFT",
        "assessment_path": str(BASE / "assessment.draft.json"),
    }
    for key, value in required.items():
        actual = status.get(key)
        if type(actual) is not type(value) or actual != value:
            raise ValueError(f"unsupported promotion or missing provenance: {key}")
    if hashlib.sha256((base / "plan.md").read_bytes()).hexdigest() != PLAN_SHA256:
        raise ValueError("frozen plan bytes changed; preserve them and record an additive amendment")
    record = json.loads((base / "assessment.draft.json").read_text(encoding="utf-8"))
    if record.get("assessment_id") != "HIT-SOLO-002-OFQUAL-DRAFT":
        raise ValueError("development assessment identity changed")
    if "Codex AI assistant" not in record.get("assessor", {}).get("name", ""):
        raise ValueError("development record must retain its AI-assessor provenance")
    disclosure = record.get("assessor", {}).get("conflict_disclosure", "")
    if "Author adjudication is pending" not in disclosure:
        raise ValueError("draft must disclose pending author adjudication")
    if record.get("assessment_scope") != "event_specific":
        raise ValueError("exploratory event must not become a period-wide assessment")
    if record.get("period") != {"start": "2020-08-17", "end": "2020-08-17"}:
        raise ValueError("frozen event boundary changed")
    if record.get("follow_up_period") != {"start": "2020-08-18", "end": "2020-08-20"}:
        raise ValueError("frozen follow-up boundary changed")
    source_ids = {item.get("source_id") for item in record.get("evidence_claims", [])}
    if source_ids != {"OFQ-01", "OCR-01", "OFQ-02", "OFQ-03", "DFE-01", "OFQ-04", "PACKET"}:
        raise ValueError("source set differs from frozen plan and local packet disclosure")
    schema = json.loads((root / "schema/hit-assessment.schema.json").read_text(encoding="utf-8"))
    conformance = validate_assessment(record, schema, source=str(BASE / "assessment.draft.json")).to_dict()
    if not conformance["valid"]:
        raise ValueError(f"draft record does not conform: {conformance['issues']}")
    paths = [BASE / name for name in FILES] + [
        Path("scripts/validate_solo_complete.py"), Path("schema/hit-assessment.schema.json"),
        Path("src/validation/assessment.py"),
    ]
    return {
        "assessment_id": record["assessment_id"],
        "check_kind": "development_record_consistency_only",
        "conformance_valid": True,
        "source_truth_validated": False,
        "scientific_interpretation_validated": False,
        "author_adjudication": "pending",
        "independent_review": False,
        "scientific_conclusion_eligible": False,
        "evidence_claim_count": len(record["evidence_claims"]),
        "source_subset_judgments_recomputed": False,
        "sha256": {str(path): hashlib.sha256((root / path).read_bytes()).hexdigest() for path in paths},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = evaluate()
        rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        output = ROOT / BASE / "record-check.json"
        if args.write:
            output.write_text(rendered, encoding="utf-8")
        elif not output.is_file() or output.read_text(encoding="utf-8") != rendered:
            raise ValueError("retained record check is absent or stale; review before regeneration")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print("Draft complete-record consistency: PASS; source interpretation and author adjudication remain pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
