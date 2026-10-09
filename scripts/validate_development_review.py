#!/usr/bin/env python3
"""Check development-review records, not quotation authenticity or scientific truth."""
from pathlib import Path

from validate_claim_bindings import decoded, safe_path, require
from validate_solo_extension import evaluate as extension_check

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "research/strengthening/solo-002-author-review.json"
ORIGINAL = "research/strengthening/solo-002-complete/assessment.draft.json"
REGISTER = "paper/development-claim-register.json"
MANUSCRIPT = "paper/development-manuscript.md"
EXTENSION = "research/strengthening/solo-002-extension/results.json"
VALUE_KEYS = {1: {"case_use"}, 2: {"Counsel"}, 3: {"Judgment"}, 4: {"Command", "Correction", "Reform"},
              5: {"Repair", "route"}, 6: {"comparison"}, 7: {"institutional_record_integrity", "assessment_packet_integrity"}}


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "Missing text")


def literal(value, expected):
    require(type(value) is type(expected) and value == expected, "Contradictory review boundary")


def values(number, accepted):
    require(isinstance(accepted, dict) and set(accepted) == VALUE_KEYS[number], "Invalid accepted-value fields")
    for key, value in accepted.items():
        if key in ("Counsel", "Judgment", "Command", "Correction", "Reform", "Repair"):
            require((type(value) is int and value in (0, 1, 2)) or value == "IE", "Invalid accepted finding")
        elif key == "case_use":
            literal(value, "bounded_exploratory_event_example")
        elif key == "route":
            require(value in ("operational_direction", "delivered_remedy"), "Unknown accepted route")
        elif key == "comparison":
            require(value in ("proposed_substantive_tie", "added_distinction", "loss", "unresolved"), "Unknown accepted comparison")
        else:
            require(value in ("adequate", "limited", "unreliable", "IE"), "Unknown accepted integrity value")


def evaluate(root=ROOT):
    root = root.resolve()
    def read(path): return safe_path(root, path).read_bytes()
    author, register = decoded(read(AUTHOR)), decoded(read(REGISTER))
    literal(author.get("review_id"), "HIT-SOLO-002-AUTHOR-001")
    literal(author.get("original_assessment"), ORIGINAL)
    read(ORIGINAL)
    literal(author.get("original_draft_preserved"), True)
    for key in ("independent_review", "pre_model_reference", "scientific_conclusion_eligible", "release_gate_satisfied"):
        literal(author.get(key), False)
    for key in ("author", "recorded_by", "source", "review_mode", "recorded_date", "date_timezone"):
        text(author.get(key))
    decisions = author.get("decisions")
    require(isinstance(decisions, list) and all(isinstance(d, dict) for d in decisions)
            and [d.get("decision_id") for d in decisions] == [f"SOLO-002-AD{n}" for n in range(1, 8)], "Missing or duplicate author decision ID")
    for number, decision in enumerate(decisions, 1):
        require(set(decision) == {"decision_id", "disposition", "question", "verbatim_response", "accepted_values", "recorded_scope"}, "Missing decision fields")
        text(decision["question"])  # Requires the recorded question; does not authenticate it.
        status = decision["disposition"]
        require(status in ("pending", "unresolved", "accept", "revise", "reject"), "Unknown disposition")
        if status == "pending":
            require(decision["verbatim_response"] is None and decision["recorded_scope"] is None, "Pending decision contains a response")
        else:
            text(decision["verbatim_response"])
            text(decision["recorded_scope"])
        if status == "accept":
            values(number, decision["accepted_values"])
        else:
            require(decision["accepted_values"] is None, "Unaccepted decision contains accepted values")
    literal(register.get("manuscript_path"), MANUSCRIPT)
    literal(register.get("author_decision_record"), AUTHOR)
    literal(register.get("status"), "working_draft_pending_author_review")
    for key in ("register_confers_scientific_acceptance", "release_gate_satisfied"):
        literal(register.get(key), False)
    historical = register.get("historical_audit", {})
    literal(historical.get("eligibility_inherited"), False)
    read(historical.get("path"))
    for key in ("register_id", "purpose", "review_semantics"):
        text(register.get(key))
    manuscript = read(MANUSCRIPT).decode("utf-8")
    require("responsible-author review and publication approval remain pending" in manuscript[:1000], "Missing manuscript review boundary")
    claims, ids = register.get("claims"), set()
    require(isinstance(claims, list) and claims, "Missing manuscript claims")
    for claim in claims:
        require(isinstance(claim, dict), "Invalid manuscript claim")
        for key in ("id", "section", "claim", "kind", "boundary"):
            text(claim.get(key))
        require(claim["id"] not in ids, "Duplicate manuscript claim ID")
        ids.add(claim["id"])
        literal(claim.get("scientific_conclusion_eligible"), False)
        require(claim.get("author_review") in ("pending", "pending_for_current_manuscript_reuse"), "Current manuscript review is not pending")
        evidence = claim.get("evidence")
        require(isinstance(evidence, list) and evidence, "Missing manuscript evidence")
        for item in evidence:
            require(isinstance(item, dict) and set(item) == {"path", "locator"}, "Invalid evidence reference")
            text(item["locator"])
            require(item["locator"] in read(item["path"]).decode("utf-8"), "Evidence locator not found")
    read(EXTENSION)
    require(extension_check(root)["results_present"] is True, "Completed extension results required")
    return {"check_kind": "development_record_consistency_only", "author_decisions": 7, "manuscript_claims": len(claims),
            "quotation_authenticity_validated": False, "source_truth_validated": False, "scientific_acceptance_conferred": False}


if __name__ == "__main__":
    try:
        result = evaluate()
    except Exception as exc:
        raise SystemExit(f"FAIL: {type(exc).__name__}; inspect development review fields, evidence and completed extension")
    print(f"Development review consistency: PASS; {result['author_decisions']} author records; {result['manuscript_claims']} manuscript claims; no scientific acceptance conferred")
