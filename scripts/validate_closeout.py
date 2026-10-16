#!/usr/bin/env python3
"""Check the bounded closeout record; do not accept research or activate a phase."""
from pathlib import Path
import re

from release_metadata import CURRENT_RELEASE, CURRENT_VERSION_DOI
from validate_claim_bindings import decoded, require, safe_path

ROOT = Path(__file__).resolve().parents[1]
STATUS = "research/strengthening/closeout-status.json"
REGISTER = "paper/development-claim-register.json"
GATES = "release/v1.0.0/gate-register.json"
QUEUE = "research/strengthening/closeout-author-review.md"
PLAN = "docs/closeout-plan.md"
SOURCES = "research/strengthening/closeout-source-check.md"
AUTHORITY = "research/strengthening/author-decisions.md"
CLAIM_IDS = [f"DEV-C{n:02d}" for n in range(1, 17)]
GATE_IDS = [
    "three_public_current_contract_applications_or_documented_migration_exceptions",
    "standalone_implementation_packet", "clean_room_implementation_audit",
    "public_v0.9.0_release_candidate", "stable_component_version_promotion",
    "breaking_change_review", "synchronized_release_metadata", "exact_release_commit_validation",
]
FALSE_FIELDS = (
    "decision_date_is_release_authority", "maintenance_started", "closeout_accepted",
    "scientific_acceptance_conferred", "publication_eligibility_inherited",
    "manuscript_submission_authorized", "v1_release_permitted",
    "independent_human_audit_completed", "current_contract_replication_scoring_permitted",
    "external_invitation_sent",
)
FIXED = {
    "closeout_id": "HIT-CLOSEOUT-2026-10-16",
    "recorded_date": "2026-10-16", "timezone": "America/New_York",
    "authority_record": f"{AUTHORITY}#ad-006-bounded-closeout-and-repository-updates",
    "baseline_commit": "40ff9caa8f583bc613ff37f4c29b1a6f2fb5214b",
    "current_archived_release": "0.6.7", "current_archived_doi": "10.5281/zenodo.23252877",
    "phase": "bounded_closeout_in_progress", "decision_date": "2026-10-30",
    "scope_frozen": True, "manuscript_claim_register": REGISTER,
    "manuscript_claim_ids": CLAIM_IDS, "stable_gate_register": GATES,
    "author_review_queue": QUEUE, "plan": PLAN,
    "transition_rule": "This record is a bounded plan. The date does not close the phase automatically. Maintenance, manuscript publication and v1 promotion require separate recorded decisions and applicable evidence; the current checker confers none.",
    **{key: False for key in FALSE_FIELDS},
}
EXCLUSIONS = [
    "additional_small_model_batches", "new_figures_without_a_defined_defect", "new_dimensions",
    "dashboards_and_runtime_integrations", "sector_effectiveness_claims",
    "participant_recruitment_or_scoring_without_protocol_activation",
    "manuscript_submission_without_exact_draft_approval",
]
ITEM_STATUSES = [
    {"implemented"}, {"awaiting_author_review"}, {"partial"},
    {"pending_verification", "verified_this_revision"}, {"awaiting_author_decision"},
]


def literal(value, expected, label):
    require(type(value) is type(expected) and value == expected, f"Contradictory {label}")


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "Missing closeout text")


def evaluate(root=ROOT):
    root = root.resolve()
    def read(path): return safe_path(root, path).read_bytes()
    status, register, gates = (decoded(read(path)) for path in (STATUS, REGISTER, GATES))
    require(isinstance(status, dict) and set(status) == set(FIXED) | {"work_items", "exclusions"},
            "Missing or unknown closeout fields")
    for key, expected in FIXED.items():
        literal(status[key], expected, key)
    literal(CURRENT_RELEASE, FIXED["current_archived_release"], "current release")
    literal(CURRENT_VERSION_DOI, FIXED["current_archived_doi"], "current DOI")
    literal(status["exclusions"], EXCLUSIONS, "scope exclusions")
    items = status["work_items"]
    require(isinstance(items, list) and len(items) == 5, "Missing closeout work items")
    for number, (item, allowed) in enumerate(zip(items, ITEM_STATUSES), 1):
        require(isinstance(item, dict) and set(item) == {"id", "task", "owner", "status", "completion"},
                "Missing or unknown work-item fields")
        literal(item["id"], f"CO-{number:02d}", "work-item ID")
        require(isinstance(item["status"], str) and item["status"] in allowed, "Unsupported closeout transition")
        for key in ("task", "owner", "completion"):
            text(item[key])
    # Work authorization does not complete this author's pending claim review.
    literal(items[1]["owner"], "Mark Julius Banasihan, responsible author", "claim-review owner")
    literal(items[4]["owner"], "Mark Julius Banasihan, maintainer", "phase-decision owner")
    literal(register.get("status"), "working_draft_pending_author_review", "manuscript status")
    for key in ("register_confers_scientific_acceptance", "release_gate_satisfied"):
        literal(register.get(key), False, key)
    literal(register.get("historical_audit", {}).get("eligibility_inherited"), False, "inherited eligibility")
    claims = register.get("claims")
    require(isinstance(claims, list) and all(isinstance(c, dict) for c in claims)
            and [c.get("id") for c in claims] == CLAIM_IDS, "Canonical claim coverage differs")
    for claim in claims:
        literal(claim.get("scientific_conclusion_eligible"), False, "claim eligibility")
        require(claim.get("author_review") in ("pending", "pending_for_current_manuscript_reuse"),
                "Claim review requires a separate recorded decision and reviewed controls")
    literal(gates.get("status"), "candidate_release_prohibited", "stable release status")
    entries = gates.get("gates")
    require(isinstance(entries, list) and all(isinstance(g, dict) for g in entries)
            and [g.get("gate_id") for g in entries] == GATE_IDS, "Stable gate coverage differs")
    for gate in entries:
        literal(gate.get("status"), "unresolved", "stable gate status")
    queue = read(QUEUE).decode("utf-8")
    require(set(re.findall(r"\bDEV-C\d+\b", queue)) == set(CLAIM_IDS), "Author worksheet claim coverage differs")
    authority = read(AUTHORITY).decode("utf-8")
    require(re.search(r"^## AD-006:\s+", authority, flags=re.MULTILINE), "Missing authority record")
    for path in (PLAN, SOURCES):
        text(read(path).decode("utf-8"))
    return {"check_kind": "closeout_record_consistency_only", "manuscript_claims": len(claims),
            "unresolved_stable_gates": len(entries), "scientific_acceptance_conferred": False,
            "maintenance_activated": False, "release_authorized": False}


if __name__ == "__main__":
    try:
        result = evaluate()
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        raise SystemExit(f"FAIL: {type(exc).__name__}; inspect closeout fields, claim coverage and preserved prohibitions")
    print(f"Closeout record consistency: PASS; {result['manuscript_claims']} pending manuscript claims; "
          f"{result['unresolved_stable_gates']} unresolved stable gates; no scientific acceptance, maintenance or release activated")
