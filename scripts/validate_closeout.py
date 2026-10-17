#!/usr/bin/env python3
"""Check the bounded closeout record; do not accept research or activate a phase."""
from pathlib import Path
import re
import subprocess

from release_metadata import CURRENT_RELEASE, CURRENT_VERSION_DOI
from validate_claim_bindings import decoded, git, require, safe_path

ROOT = Path(__file__).resolve().parents[1]
STATUS = "research/strengthening/closeout-status.json"
REGISTER = "paper/development-claim-register.json"
GATES = "release/v1.0.0/gate-register.json"
QUEUE = "research/strengthening/closeout-author-review.md"
PLAN = "docs/closeout-plan.md"
SOURCES = "research/strengthening/closeout-source-check.md"
AUTHORITY = "research/strengthening/author-decisions.md"
MAINTENANCE_AUTHORITY = f"{AUTHORITY}#ad-032-conditional-maintenance-authorization"
RECEIPT = "research/strengthening/maintenance-receipt.json"
REPOSITORY_URL = "https://github.com/node-and-norm/human-influence-telemetry"
CLAIM_IDS = [f"DEV-C{n:02d}" for n in range(1, 17)]
DISPOSITION_IDS = [f"AD-{n:03d}" for n in range(7, 32)]
GATE_IDS = [
    "three_public_current_contract_applications_or_documented_migration_exceptions",
    "standalone_implementation_packet", "clean_room_implementation_audit",
    "public_v0.9.0_release_candidate", "stable_component_version_promotion",
    "breaking_change_review", "synchronized_release_metadata", "exact_release_commit_validation",
]
FALSE_FIELDS = (
    "decision_date_is_release_authority",
    "scientific_acceptance_conferred", "publication_eligibility_inherited",
    "manuscript_submission_authorized", "v1_release_permitted",
    "independent_human_audit_completed", "current_contract_replication_scoring_permitted",
    "external_invitation_sent",
)
FIXED = {
    "closeout_id": "HIT-CLOSEOUT-2026-10-16",
    "recorded_date": "2026-10-16", "timezone": "America/New_York",
    "authority_record": f"{AUTHORITY}#ad-006-bounded-closeout-and-repository-updates",
    "maintenance_authority_record": MAINTENANCE_AUTHORITY,
    "baseline_commit": "40ff9caa8f583bc613ff37f4c29b1a6f2fb5214b",
    "current_archived_release": "0.6.7", "current_archived_doi": "10.5281/zenodo.23252877",
    "decision_date": "2026-10-30",
    "scope_frozen": True, "manuscript_claim_register": REGISTER,
    "manuscript_claim_ids": CLAIM_IDS, "stable_gate_register": GATES,
    "author_review_queue": QUEUE, "plan": PLAN,
    "transition_rule": "The date does not close the phase automatically. Maintenance requires AD-032 authorization and a receipt for the reviewed pull-request head and merged revision. Manuscript publication and v1 promotion retain their separate requirements. This checker validates recorded consistency, not the authenticity of human decisions or check execution.",
    **{key: False for key in FALSE_FIELDS},
}
EXCLUSIONS = [
    "additional_small_model_batches", "new_figures_without_a_defined_defect", "new_dimensions",
    "dashboards_and_runtime_integrations", "sector_effectiveness_claims",
    "participant_recruitment_or_scoring_without_protocol_activation",
    "manuscript_submission_without_exact_draft_approval",
]
ITEM_STATUSES = [
    {"implemented"}, {"bounded_dispositions_recorded"}, {"partial"},
    {"verified_this_revision"}, {"authorized_pending_verification", "maintenance_entered"},
]
LOCAL_PASS_FIELDS = (
    "workflow_commands_passed", "closeout_tests_passed", "local_links_passed",
    "protected_history_unchanged", "expected_readiness_failures_preserved",
)


def literal(value, expected, label):
    require(type(value) is type(expected) and value == expected, f"Contradictory {label}")


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "Missing closeout text")


def fields(value, keys, label):
    require(isinstance(value, dict) and set(value) == set(keys), f"Missing or unknown {label} fields")


def mode(status):
    require(status.get("phase") in ("bounded_closeout_in_progress", "maintenance"), "Unsupported phase")
    active = status["phase"] == "maintenance"
    for key in ("maintenance_started", "closeout_accepted"):
        literal(status.get(key), active, key)
    literal(status.get("maintenance_receipt"), RECEIPT if active else None, "maintenance receipt")
    return active


def git_checked(root, *args):
    try:
        return git(root, *args)
    except (OSError, subprocess.CalledProcessError):
        raise ValueError("Required maintenance commit, content or ancestry is unavailable") from None


def check_receipt(root, current_register, current_gates):
    """Check a recorded observation against local Git; authenticate no remote action."""
    receipt = decoded(safe_path(root, RECEIPT).read_bytes())
    fields(receipt, {"receipt_id", "recorded_date", "authority_record", "scope", "reviewed_pr",
                     "local_checks", "hosted_checks", "offline_check_authenticates_execution",
                     "offline_check_authenticates_authority"}, "maintenance receipt")
    for key, value in {
        "receipt_id": "HIT-MAINTENANCE-2026-10-17", "recorded_date": "2026-10-17",
        "authority_record": MAINTENANCE_AUTHORITY, "scope": "bounded_solo_development_to_maintenance_only",
        "offline_check_authenticates_execution": False, "offline_check_authenticates_authority": False,
    }.items():
        literal(receipt[key], value, key)
    pr = receipt["reviewed_pr"]
    fields(pr, {"number", "url", "head_commit", "merge_commit"}, "reviewed PR")
    literal(pr["number"], 42, "reviewed PR number")
    literal(pr["url"], f"{REPOSITORY_URL}/pull/42", "reviewed PR URL")
    revisions = [pr["head_commit"], pr["merge_commit"]]
    require(all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) for value in revisions),
            "Invalid reviewed revision")
    require(revisions[0] != revisions[1], "Reviewed head and merge must differ")
    for key in ("local_checks", "hosted_checks"):
        require(isinstance(receipt[key], list) and len(receipt[key]) == 2, "Both reviewed revisions need checks")
    run_ids = []
    for revision, event, local, hosted in zip(revisions, ("pull_request", "push"), receipt["local_checks"], receipt["hosted_checks"]):
        fields(local, {"revision", "uncommitted_changes_included", *LOCAL_PASS_FIELDS}, "local checks")
        literal(local["revision"], revision, "local checked revision")
        literal(local["uncommitted_changes_included"], False, "local uncommitted changes")
        for key in LOCAL_PASS_FIELDS:
            literal(local[key], True, key)
        fields(hosted, {"revision", "workflow", "event", "run_id", "url", "status", "conclusion"}, "hosted checks")
        for key, value in {"revision": revision, "workflow": "HIT Validation", "event": event,
                           "status": "completed", "conclusion": "success"}.items():
            literal(hosted[key], value, key)
        run_id = hosted["run_id"]
        require(type(run_id) is int and run_id > 0, "Invalid hosted run ID")
        literal(hosted["url"], f"{REPOSITORY_URL}/actions/runs/{run_id}", "hosted run URL")
        run_ids.append(run_id)
    require(len(set(run_ids)) == 2, "Head and merge require separate hosted runs")
    head, merge = revisions
    for revision in revisions:
        literal(git_checked(root, "rev-parse", "--verify", f"{revision}^{{commit}}").decode().strip(), revision, "local commit identity")
        frozen_status = decoded(git_checked(root, "show", f"{revision}:{STATUS}"))
        for key, value in FIXED.items():
            literal(frozen_status.get(key), value, f"reviewed {key}")
        literal(mode(frozen_status), False, "reviewed pending phase")
        frozen_items = frozen_status.get("work_items", [])
        require(len(frozen_items) == 5, "Reviewed work items missing")
        literal(frozen_items[1].get("status"), "bounded_dispositions_recorded", "reviewed dispositions")
        literal(frozen_items[3].get("status"), "verified_this_revision", "reviewed verification")
        literal(frozen_items[4].get("status"), "authorized_pending_verification", "reviewed maintenance authorization")
        authority = git_checked(root, "show", f"{revision}:{AUTHORITY}").decode("utf-8")
        require(len(re.findall(r"^## AD-032: Conditional maintenance authorization$", authority, re.MULTILINE)) == 1,
                "Reviewed revision lacks unique maintenance authority record")
        for path, current in ((REGISTER, current_register), (GATES, current_gates)):
            literal(git_checked(root, "show", f"{revision}:{path}"), current, "protected reviewed record")
    parents = git_checked(root, "rev-list", "--parents", "-n", "1", merge).decode().split()[1:]
    require(len(parents) >= 2 and head in parents, "Merge must preserve the exact reviewed head as a parent")
    for ancestor, descendant in ((FIXED["baseline_commit"], head), (head, merge), (merge, "HEAD")):
        git_checked(root, "merge-base", "--is-ancestor", ancestor, descendant)


def evaluate(root=ROOT):
    root = root.resolve()
    def read(path): return safe_path(root, path).read_bytes()
    status_raw, register_raw, gates_raw = (read(path) for path in (STATUS, REGISTER, GATES))
    status, register, gates = (decoded(raw) for raw in (status_raw, register_raw, gates_raw))
    require(isinstance(status, dict) and set(status) == set(FIXED) | {"work_items", "exclusions", "phase", "maintenance_started", "closeout_accepted", "maintenance_receipt"},
            "Missing or unknown closeout fields")
    for key, expected in FIXED.items():
        literal(status[key], expected, key)
    literal(CURRENT_RELEASE, FIXED["current_archived_release"], "current release")
    literal(CURRENT_VERSION_DOI, FIXED["current_archived_doi"], "current DOI")
    literal(status["exclusions"], EXCLUSIONS, "scope exclusions")
    active = mode(status)
    items = status["work_items"]
    require(isinstance(items, list) and len(items) == 5, "Missing closeout work items")
    for number, (item, allowed) in enumerate(zip(items, ITEM_STATUSES), 1):
        require(isinstance(item, dict) and set(item) == {"id", "task", "owner", "status", "completion"},
                "Missing or unknown work-item fields")
        literal(item["id"], f"CO-{number:02d}", "work-item ID")
        require(isinstance(item["status"], str) and item["status"] in allowed, "Unsupported closeout transition")
        for key in ("task", "owner", "completion"):
            text(item[key])
    # Recorded dispositions do not approve the unchanged manuscript or activate a phase.
    literal(items[1]["owner"], "Mark Julius Banasihan, responsible author", "claim-review owner")
    literal(items[4]["owner"], "Mark Julius Banasihan, maintainer", "phase-decision owner")
    literal(items[4]["status"], "maintenance_entered" if active else "authorized_pending_verification", "maintenance work-item state")
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
    require(len(re.findall(r"^## AD-032: Conditional maintenance authorization$", authority, re.MULTILINE)) == 1,
            "Missing or duplicate maintenance authority record")
    dispositions_recorded = items[1]["status"] == "bounded_dispositions_recorded"
    if dispositions_recorded:
        # Presence and uniqueness only: this cannot authenticate human acceptance or support.
        for decision_id in DISPOSITION_IDS:
            matches = re.findall(rf"^## {re.escape(decision_id)}:[ \t]+[^\n]+$", authority, flags=re.MULTILINE)
            require(len(matches) == 1, f"Missing or duplicate bounded disposition: {decision_id}")
    for path in (PLAN, SOURCES):
        text(read(path).decode("utf-8"))
    if active:
        check_receipt(root, register_raw, gates_raw)
    else:
        require(not (root / RECEIPT).exists() and not (root / RECEIPT).is_symlink(), "Pending phase must not retain a maintenance receipt")
    return {"check_kind": "closeout_record_consistency_only", "manuscript_claims": len(claims),
            "unresolved_stable_gates": len(entries), "bounded_dispositions_recorded": dispositions_recorded,
            "phase": status["phase"], "maintenance_recorded": active,
            "scientific_acceptance_conferred": False,
            "maintenance_activated": False, "release_authorized": False}


if __name__ == "__main__":
    try:
        result = evaluate()
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        raise SystemExit(f"FAIL: {type(exc).__name__}; inspect closeout fields, claim coverage and preserved prohibitions")
    print(f"Closeout record consistency: PASS; {result['manuscript_claims']} pending manuscript claims; "
          f"{result['unresolved_stable_gates']} unresolved stable gates; phase {result['phase']}; "
          "no scientific acceptance or release authorization conferred")
