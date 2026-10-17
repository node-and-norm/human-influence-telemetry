#!/usr/bin/env python3
"""Check the exploratory packet's guardrails, not assessment conformance or truth."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT))
from src.validation.assessment import validate_assessment


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate() -> dict:
    require(digest(BASE / "preservation.json") == "0eea5548dd070cfe68539c05311c1932e574773c860695a982acb96a43b5efd6",
            "approved preservation manifest changed; do not silently refresh")
    preservation = read_json(BASE / "preservation.json")
    require(preservation["baseline_commit"] == "8272ca76c90973985573b48530fe5cb61a73254a",
            "preservation baseline changed")
    protected = preservation["files"]
    require(len(protected) == 42 and len({entry["path"] for entry in protected}) == 42,
            "protected inventory changed or contains duplicate paths; review rather than silently refresh")
    for entry in protected:
        path = ROOT / entry["path"]
        require(path.is_file() and digest(path) == entry["sha256"],
                f"protected bytes changed: {entry['path']}")
    assessment = read_json(BASE / "assessment.draft.json")
    status = read_json(BASE / "review-status.json")
    require(assessment["assessment_id"] == "HIT-SOLO-002-BM-REASSESSMENT-DRAFT-001", "identity changed")
    require(assessment["schema_version"] == assessment["specification_version"] == "0.4.0", "contract changed")
    require(assessment["assessment_scope"] == "event_specific", "scope widened")
    require(assessment["period"] == {"start": "2020-08-14", "end": "2020-08-17"}, "primary boundary changed")
    require(assessment["follow_up_period"] == {"start": "2020-08-18", "end": "2020-08-20"}, "follow-up changed")
    require(assessment["aggregation"]["predeclared"] is False, "post-inspection boundary promoted")
    sources = {c["source_id"] for c in assessment["evidence_claims"]}
    expected = {"OFQ-01", "OCR-01", "OFQ-02", "OFQ-03", "DFE-01", "OFQ-04", "PACKET"}
    expected.update(f"BM-{i:02}" for i in range(1, 9))
    require(sources == expected, "source inventory changed without amendment")
    require(len(assessment["evidence_claims"]) == 39 and len(assessment["actors"]) == 8, "draft inventory changed")
    claim_ids = {c["claim_id"] for c in assessment["evidence_claims"]}
    for reference in re.findall(r"EC-[A-Za-z0-9._-]+", json.dumps(assessment)):
        require(reference.rstrip(".") in claim_ids, f"unresolved prose claim reference: {reference}")
    require(status["assessment_id"] == assessment["assessment_id"], "review identity mismatch")
    require(status["status"] == "exploratory_draft_bounded_author_decisions_complete_nonconformant"
            and status["bounded_author_decisions_complete"] is True,
            "bounded decision completion or exploratory nonconformance status changed")
    require(status["personal_source_review"] == "pending", "personal review promoted")
    for flag in ("assessment_conformant", "independent_human_review", "manuscript_revision_authorized",
                 "publication_authorized", "scientific_conclusion_eligible", "release_gate_satisfied"):
        require(status[flag] is False, f"unsupported promotion: {flag}")
    decisions = status["decisions"]
    require([d["id"] for d in decisions] == [f"BMR-{i:02}" for i in range(1, 9)], "decision inventory changed")
    counsel = decisions[0]
    require(counsel["disposition"] == "accepted_with_limits"
            and type(counsel["accepted_value"]) is int and counsel["accepted_value"] == 1
            and counsel["proposal"] == 1 and counsel["alternatives"] == [2, "IE"]
            and counsel["personal_source_review"] == "pending", "Counsel disposition or limits changed")
    receipt = counsel["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept Counsel 1 for this bounded reassessment, retaining 2 and IE as alternatives and keeping my personal source review pending. Please record it and walk me through the next decision, keeping the manuscript unchanged."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Counsel receipt or accepted proposal bytes changed")
    judgment = decisions[1]
    require(judgment["disposition"] == "accepted_with_limits"
            and type(judgment["accepted_value"]) is int and judgment["accepted_value"] == 2
            and judgment["proposal"] == 2 and judgment["alternatives"] == []
            and judgment["personal_source_review"] == "pending", "Judgment disposition or limits changed")
    receipt = judgment["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept Judgment 2 for this bounded reassessment with those limits. Keep my personal source review pending and the manuscript unchanged. Please record it and walk me through the next decision. Thank you."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Judgment receipt or accepted proposal bytes changed")
    command = decisions[2]
    require(command["disposition"] == "accepted_with_limits"
            and type(command["accepted_value"]) is int and command["accepted_value"] == 2
            and command["proposal"] == 2 and command["alternatives"] == [1, "IE"]
            and command["personal_source_review"] == "pending", "Command disposition or limits changed")
    receipt = command["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept Command 2 for this bounded reassessment with those limits. Keep my personal source review pending and the manuscript unchanged. Please record it and walk me through the next decision. Thank you."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Command receipt or accepted proposal bytes changed")
    correction = decisions[3]
    require(correction["disposition"] == "accepted_with_limits"
            and type(correction["accepted_value"]) is int and correction["accepted_value"] == 2
            and correction["proposal"] == 2 and correction["alternatives"] == []
            and correction["personal_source_review"] == "pending", "Correction disposition or limits changed")
    receipt = correction["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept Correction 2 for this bounded reassessment with those limits. Keep my personal source review pending and the manuscript unchanged. Please record it and walk me through the Repair decision. Thank you."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Correction receipt or accepted proposal bytes changed")
    repair = decisions[4]
    require(repair["disposition"] == "accepted_with_limits"
            and type(repair["accepted_value"]) is int and repair["accepted_value"] == 2
            and repair["proposal"] == 2 and repair["alternatives"] == [1, "IE"]
            and repair["proposed_trigger"] == "triggered" and repair["accepted_trigger"] == "triggered"
            and repair["personal_source_review"] == "pending", "Repair trigger, finding or limits changed")
    receipt = repair["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept the harm trigger and Repair 2 on the limited AS/A-level record-correction route, with those limits. Keep my personal source review pending and the manuscript unchanged. Please record it and walk me through Reform. Thank you."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Repair receipt or accepted proposal bytes changed")
    reform = decisions[5]
    require(reform["disposition"] == "accepted_with_limits"
            and type(reform["accepted_value"]) is int and reform["accepted_value"] == 2
            and reform["proposal"] == 2 and reform["alternatives"] == []
            and reform["personal_source_review"] == "pending", "Reform disposition or limits changed")
    receipt = reform["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept Reform 2 with those limits and the implementation-plan qualification. Keep my personal source review pending and the manuscript unchanged. Please record it and walk me through the integrity decision. Thank you."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Reform receipt or accepted proposal bytes changed")
    integrity = decisions[6]
    integrity_components = {"institutional_record_integrity": "limited",
                            "assessment_packet_integrity": "limited"}
    require(integrity["disposition"] == "accepted_with_limits"
            and integrity["accepted_value"] == integrity_components
            and integrity["proposal"] == integrity_components and integrity["alternatives"] == []
            and integrity["proposed_overall_status"] == integrity["accepted_overall_status"] == "limited"
            and integrity["derivation_rule"] == "unreliable>IE>limited>adequate"
            and integrity["personal_source_review"] == "pending", "Integrity components, overall status or limits changed")
    receipt = integrity["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept limited for both integrity components separately and overall, with those limits. Keep my personal source review pending and the manuscript unchanged. Please record it and walk me through the final decision."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Integrity receipt or accepted proposal bytes changed")
    reporting = decisions[7]
    reporting_boundaries = "Retain expanded chronology, exploratory nonconformance and original S05/comparison boundaries; no manuscript or release change."
    require(reporting["disposition"] == "accepted_with_limits"
            and reporting["proposal"] == reporting["accepted_value"] == reporting_boundaries
            and reporting["alternatives"] == [] and reporting["personal_source_review"] == "pending",
            "Reporting and reuse disposition or limits changed")
    receipt = reporting["author_receipt"]
    require(isinstance(receipt, dict) and receipt.get("recorded_date") == "2026-10-17"
            and receipt.get("statement") == "Yes, I accept these reporting and reuse boundaries, with personal source review pending and the manuscript unchanged. Please record it and summarize what is complete and what remains open. Thank you."
            and receipt.get("assessment_sha256") == "12e9672572e703aa2828211a5774591a062e6aaadcea3dfbcddb15549d55a66c"
            and receipt["assessment_sha256"] == digest(BASE / "assessment.draft.json"),
            "Reporting and reuse receipt or accepted proposal bytes changed")
    qualification = status["source_qualifications"]
    require(len(qualification) == 1 and qualification[0]["id"] == "SQ-01"
            and qualification[0]["claim_id"] == "EC-BMR-ARCHITECTURE"
            and qualification[0]["qualified_proposition"] == "The Board agreed the changed award rule and delegated implementation actions to the Chair and Chief Regulator, including developing an implementation plan and making necessary regulatory-framework changes."
            and qualification[0]["excluded_inference"] == "This passage does not record Board approval of a completed implementation plan."
            and qualification[0]["snapshot_preserved"] is True
            and qualification[0]["personal_source_review"] == "pending"
            and qualification[0]["author_disposition"] == "accepted_with_limits"
            and qualification[0]["author_receipt_decision_id"] == "BMR-06",
            "plan-development qualification changed or promoted")
    schema = read_json(ROOT / "schema/hit-assessment.schema.json")
    result = validate_assessment(assessment, schema,
        source=str((BASE / "assessment.draft.json").relative_to(ROOT))).to_dict()
    issues = [(x["code"], x["path"]) for x in result["issues"]]
    require(result["valid"] is False and result["schema_valid"] is False
            and result["semantic_valid"] is True
            and issues == [("HIT-SCHEMA", "/aggregation/predeclared")],
            "conformance result changed; inspect before refreshing the record")

    # Local Markdown targets only; external availability and anchor truth are not checked.
    for name in ("README.md", "source-ledger.md", "boundary-amendment.md"):
        path = BASE / name
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith("#") and target != "record-check.json":
                require((path.parent / target.split("#")[0]).exists(), f"missing local target: {target}")
    files = ["README.md", "boundary-amendment.md", "source-ledger.md", "assessment.draft.json",
             "review-status.json", "preservation.json", "verification.md", "check.py", "test_check.py"]
    return {
        "assessment_id": assessment["assessment_id"],
        "check_kind": "exploratory_packet_guardrails_only",
        "guardrails_pass": True,
        "protected_files_unchanged": len(protected),
        "external_source_count": len(sources - {"PACKET"}),
        "evidence_claim_count": len(claim_ids),
        "actor_count": len(assessment["actors"]),
        "assessment_conformance": result,
        "source_truth_validated": False,
        "scientific_interpretation_validated": False,
        "personal_source_review": "pending",
        "new_author_dispositions": 8,
        "pending_author_decisions": 0,
        "bounded_author_decisions_complete": True,
        "accepted_repair_trigger": "triggered",
        "accepted_integrity": {**integrity_components, "overall_status": "limited"},
        "source_qualification_ids": ["SQ-01"],
        "accepted_source_qualification_ids": ["SQ-01"],
        "independent_human_review": False,
        "sha256": {name: digest(BASE / name) for name in files},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit", action="store_true", help="print the current report; writes no files")
    group.add_argument("--check", action="store_true", help="compare with retained record-check.json")
    args = parser.parse_args()
    try:
        report = evaluate()
        if args.emit:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            require(report == read_json(BASE / "record-check.json"), "retained check absent or stale")
            print("Packet guardrails: PASS; assessment conformance: FAIL (predeclaration); bounded author decisions: 8 accepted, 0 pending; Repair trigger: accepted; integrity: both limited, overall limited; SQ-01: accepted with limits; personal source review: PENDING")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Packet guardrails: FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
