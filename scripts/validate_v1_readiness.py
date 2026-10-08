#!/usr/bin/env python3
"""Validate HIT v1 readiness staging and draft manual-workbook controls."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from v1_readiness_checks import checked_path
from release_metadata import CURRENT_RELEASE, CURRENT_VERSION_DOI, DOI_STATUS

ROOT = Path(__file__).resolve().parents[1]
MANUAL_DIR = ROOT / "validation" / "v0.7.0" / "manual-workbooks"
ASSET_MANIFEST = MANUAL_DIR / "candidate-assets-manifest.json"
WORKBOOK_CONTRACT = MANUAL_DIR / "manual-workbook-contract.json"
V1_LOCK = ROOT / "release" / "v1.0.0" / "contract-freeze.candidate.json"
V1_PLAN = ROOT / "docs" / "v1-readiness-plan.md"
V1_RELEASE = ROOT / "docs" / "releases" / "v1.0.0-candidate.md"
ACTIVE_PROTOCOL = ROOT / "validation" / "v0.7.0" / "protocol-lock.candidate.json"

EXPECTED_SCORERS = ["HIT-SCORER-A", "HIT-SCORER-B", "HIT-SCORER-C"]
EXPECTED_FILENAMES = {
    "HIT-SCORER-A-HIT040-manual-workbook-draft.docx",
    "HIT-SCORER-A-HIT040-manual-workbook-draft.pdf",
    "HIT-SCORER-B-HIT040-manual-workbook-draft.docx",
    "HIT-SCORER-B-HIT040-manual-workbook-draft.pdf",
    "HIT-SCORER-C-HIT040-manual-workbook-draft.docx",
    "HIT-SCORER-C-HIT040-manual-workbook-draft.pdf",
    "HIT-IRP-HIT040-002-manual-scorer-workbook-template.docx",
    "HIT-IRP-HIT040-002-manual-scorer-workbook-template.pdf",
}
SOFTWARE_DOI = CURRENT_VERSION_DOI


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_file(path: Path, failures: list[str], root: Path = ROOT) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        failures.append(f"missing or empty file: {path.relative_to(root)}")


def validate(root: Path = ROOT, mode: str = "staging") -> list[str]:
    failures: list[str] = []
    manual_dir = root / "validation" / "v0.7.0" / "manual-workbooks"
    asset_manifest = manual_dir / "candidate-assets-manifest.json"
    workbook_contract = manual_dir / "manual-workbook-contract.json"
    v1_lock = root / "release" / "v1.0.0" / "contract-freeze.candidate.json"
    v1_plan = root / "docs" / "v1-readiness-plan.md"
    v1_release = root / "docs" / "releases" / "v1.0.0-candidate.md"
    active_protocol = root / "validation" / "v0.7.0" / "protocol-lock.candidate.json"
    gate_register = root / "release" / "v1.0.0" / "gate-register.json"

    for path in (
        manual_dir / "README.md",
        asset_manifest,
        workbook_contract,
        v1_lock,
        v1_plan,
        v1_release,
        active_protocol,
        gate_register,
    ):
        require_file(path, failures, root)

    if failures:
        return failures

    assets = load_json(asset_manifest)
    if assets.get("protocol_id") != "HIT-IRP-HIT040-002":
        failures.append("manual asset manifest protocol ID changed")
    if assets.get("status") != "draft_scoring_prohibited":
        failures.append("manual assets must remain draft and scoring prohibited")
    if assets.get("assessment_contract_version") != "0.4.0":
        failures.append("manual assets must target assessment contract 0.4.0")
    if assets.get("conformance_engine_version") != "0.5.0":
        failures.append("manual assets must identify conformance engine 0.5.0")
    if assets.get("packet_ids") != []:
        failures.append("manual assets may not assign packet IDs before human selection and freeze")
    if assets.get("rendered_page_count_per_workbook") != 31:
        failures.append("manual workbook page count must remain recorded as 31")
    if assets.get("visual_review_status") != "passed_all_pages":
        failures.append("manual workbook visual review must cover every page")
    if assets.get("activation_requires_locked_protocol") is not True:
        failures.append("manual assets must require locked protocol activation")
    if assets.get("activation_requires_three_packet_ids") is not True:
        failures.append("manual assets must require three packet IDs")
    if assets.get("activation_requires_v070_publication") is not True:
        failures.append("manual assets must require v0.7.0 publication")

    bundle = assets.get("bundle", {})
    if bundle.get("publication_status") != "candidate_asset_not_published":
        failures.append("manual workbook ZIP must remain an unpublished candidate asset")
    if not isinstance(bundle.get("size_bytes"), int) or bundle.get("size_bytes", 0) <= 0:
        failures.append("manual workbook ZIP size missing")
    if not isinstance(bundle.get("sha256"), str) or len(bundle.get("sha256", "")) != 64:
        failures.append("manual workbook ZIP hash invalid")

    files = assets.get("files", [])
    filenames = {item.get("filename") for item in files}
    if filenames != EXPECTED_FILENAMES:
        failures.append("manual asset manifest must contain exactly eight declared files")
    for item in files:
        if not isinstance(item.get("size_bytes"), int) or item.get("size_bytes", 0) <= 0:
            failures.append(f"invalid size for {item.get('filename')}")
        if not isinstance(item.get("sha256"), str) or len(item.get("sha256", "")) != 64:
            failures.append(f"invalid SHA-256 for {item.get('filename')}")

    binary_files = [
        path for path in manual_dir.iterdir()
        if path.suffix.lower() in {".docx", ".pdf", ".zip"}
    ]
    if binary_files:
        failures.append("candidate workbook binaries belong in release assets, not the repository tree")

    contract = load_json(workbook_contract)
    if contract.get("contract_id") != "HIT-MANUAL-WORKBOOK-HIT040-001":
        failures.append("manual workbook contract ID changed")
    if contract.get("status") != "candidate":
        failures.append("manual workbook contract must remain candidate")
    if contract.get("scoring_permitted") is not False:
        failures.append("manual workbook contract must not permit scoring")
    if contract.get("required_scorer_public_ids") != EXPECTED_SCORERS:
        failures.append("manual workbook contract must require scorer IDs A, B, and C")
    if contract.get("required_packet_count") != 3:
        failures.append("manual workbook contract must require three packets")
    if contract.get("required_packet_ids") != []:
        failures.append("manual workbook contract must not preassign packet IDs")
    if contract.get("generative_ai_substantive_assistance_allowed") is not False:
        failures.append("manual workbook contract must prohibit generative AI substantive assistance")
    if contract.get("original_working_record_preserved") is not True:
        failures.append("manual workbook contract must preserve original records")
    if contract.get("adjudication_may_overwrite_original") is not False:
        failures.append("adjudication may not overwrite original scorer records")

    active = load_json(active_protocol)
    if active.get("status") != "candidate":
        failures.append("active v0.7.0 protocol must remain candidate in this increment")
    if active.get("scoring_permitted") is not False:
        failures.append("active v0.7.0 protocol must continue to prohibit scoring")
    if active.get("required_scorers") != 3 or active.get("required_submissions") != 9:
        failures.append("active protocol must retain the three-scorer, nine-submission design")
    if active.get("packet_ids") != []:
        failures.append("active protocol must not assign packet IDs in this increment")

    v1 = load_json(v1_lock)
    if v1.get("target_repository_release") != "1.0.0":
        failures.append("v1 target release changed")
    if v1.get("status") != "candidate" or v1.get("release_permitted") is not False:
        failures.append("v1 contract freeze must remain a non-releasable candidate")
    if v1.get("research_maturity_is_separate") is not True:
        failures.append("v1 semantic stability must remain separate from research maturity")
    if v1.get("current_repository_release") != CURRENT_RELEASE:
        failures.append("v1 readiness baseline must identify repository release 0.6.6")
    if "current_software_doi" not in v1 or v1["current_software_doi"] != SOFTWARE_DOI:
        failures.append("v1 readiness baseline exact-version DOI mismatch")
    if v1.get("current_software_doi_status") != DOI_STATUS:
        failures.append("v1 readiness baseline must distinguish pending from verified DOI")
    if v1.get("human_result_release") != "0.6.0":
        failures.append("v1 readiness baseline must preserve the 0.6.0 human-result release")
    current = v1.get("current_component_versions", {})
    expected_current = {
        "specification": "0.4.0",
        "assessment_schema": "0.4.0",
        "dimension_catalog": "0.4.0",
        "application_handbook": "0.4.0",
        "conformance_engine": "0.5.0",
    }
    if current != expected_current:
        failures.append("v1 readiness current component map is inconsistent")
    target = v1.get("target_component_versions", {})
    if target != {key: "1.0.0" for key in expected_current}:
        failures.append("stable target must name all five component keys at version 1.0.0")
    blockers = set(v1.get("blocking_gates", []))
    required_blockers = {
        "three_public_current_contract_applications_or_documented_migration_exceptions",
        "standalone_implementation_packet",
        "clean_room_implementation_audit",
        "public_v0.9.0_release_candidate",
        "stable_component_version_promotion",
        "breaking_change_review",
        "synchronized_release_metadata",
        "exact_release_commit_validation",
    }
    if blockers != required_blockers or len(v1.get("blocking_gates", [])) != len(required_blockers):
        failures.append("stable-track blocker set must contain exactly the eight declared gates")
    if v1.get("track_id") != "HIT-STABLE-V100-001" or v1.get("governance_decision") != "ADR-0005":
        failures.append("stable track must identify HIT-STABLE-V100-001 and ADR-0005")
    if v1.get("gate_register") != "release/v1.0.0/gate-register.json":
        failures.append("stable track must reference the declared gate register")
    if v1.get("current_research_maturity") != {"level": 2, "name": "Applicable"}:
        failures.append("stable readiness work cannot change research maturity")
    if required_blockers.intersection(v1.get("completed_gates", [])):
        failures.append("unresolved stable gates cannot also be listed as completed")
    empirical = v1.get("empirical_track", {})
    if empirical.get("track_id") != "HIT-EMPIRICAL-HIT040-002":
        failures.append("empirical track identity changed")
    if empirical.get("protocol_id") != "HIT-IRP-HIT040-002":
        failures.append("empirical track must preserve the current-contract protocol")
    if empirical.get("status") != "candidate_scoring_prohibited":
        failures.append("empirical track must remain candidate and scoring prohibited")
    if empirical.get("blocks_stable_release") is not False:
        failures.append("empirical preparation must not silently become a stable-release dependency")
    if empirical.get("current_contract_replication") != "unresolved":
        failures.append("current-contract replication must remain unresolved")
    if empirical.get("protocol_rules_changed") is not False:
        failures.append("stable-track amendment must preserve empirical protocol rules")
    empirical_blockers = {
        "signed_human_case_selection", "three_frozen_current_contract_packets",
        "v0.7.0_locked_protocol_publication",
    }
    if set(empirical.get("blocking_gates", [])) != empirical_blockers or len(empirical.get("blocking_gates", [])) != len(empirical_blockers):
        failures.append("empirical track must retain all three replication-preparation safeguards")
    if v1.get("human_replication_preferred_but_not_semantic_v1_gate") is not True:
        failures.append("completed replication must remain separate from semantic stability")

    register = load_json(gate_register)
    if register.get("track_id") != "HIT-STABLE-V100-001" or register.get("governance_decision") != "ADR-0005":
        failures.append("gate register identity must match the stable track and ADR-0005")
    if register.get("status") != "candidate_release_prohibited":
        failures.append("gate register must remain candidate_release_prohibited; completion is unsupported")
    gates = register.get("gates", [])
    if not isinstance(gates, list) or any(not isinstance(item, dict) for item in gates):
        failures.append("gate register gates must be a list of objects")
        gates = []
    if {item.get("gate_id") for item in gates} != required_blockers or len(gates) != len(required_blockers):
        failures.append("gate register must cover each stable blocker exactly once")
    for item in gates:
        gate_id = item.get("gate_id")
        if item.get("status") != "unresolved":
            failures.append(f"{gate_id}: completion acceptance is unsupported; candidate gate must remain unresolved")
        paths = item.get("evidence_paths")
        if not isinstance(paths, list) or not paths:
            failures.append(f"{gate_id}: supporting evidence_paths must be a nonempty list")
            continue
        for path in paths:
            checked_path(root, path, failures, f"{gate_id} evidence path")
    # Existing paths demonstrate staging progress, not satisfaction of the gate.
    # A future acceptance policy must validate the actual evidence and its scope.

    plan = v1_plan.read_text(encoding="utf-8")
    for phrase in (
        "Current repository release:** `0.6.6`",
        "Current exact-version DOI:** pending verification" if SOFTWARE_DOI is None else f"Current exact-version DOI:** `{SOFTWARE_DOI}`",
        "Previous exact-version DOI, v0.6.4:** `10.5281/zenodo.21446142`",
        "Current research maturity:** Level 2, Applicable",
        "Version `1.0.0` is a compatibility and implementation claim",
        "Draft manual workbooks now exist",
        "Withhold `1.0.0`",
        "Publish `v0.9.0`",
    ):
        if phrase not in plan:
            failures.append(f"v1 readiness plan missing required statement: {phrase}")

    release = v1_release.read_text(encoding="utf-8")
    for phrase in (
        "Status:** Candidate outline, release prohibited",
        "Current repository release:** `0.6.6`",
        "Current normative contract:** `0.4.0`",
        "Current conformance engine:** `0.5.0`",
        "public `v0.9.0` release candidate",
        "DRAFT - SCORING PROHIBITED",
    ):
        if phrase not in release:
            failures.append(f"v1 candidate release outline missing required statement: {phrase}")

    if mode == "release-ready":
        for gate_id in sorted(required_blockers):
            failures.append(f"stable release prerequisite unresolved: {gate_id}")
        failures.append(
            "release-ready acceptance is not implemented for this candidate: release remains prohibited; "
            "a reviewed promotion policy and explicit maintainer decision are required"
        )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("staging", "release-ready"), default="staging")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (for isolated checks)")
    args = parser.parse_args()
    try:
        failures = validate(args.root.resolve(), args.mode)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        failures = [f"unreadable or malformed candidate controls: {exc}"]
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("HIT v1 staging consistency passed; not release readiness")
    print(f"- current repository release metadata: {CURRENT_RELEASE}")
    print("- human-result release: 0.6.0")
    print(f"- current exact-version DOI: {SOFTWARE_DOI or 'pending verification'}")
    print("- current normative contract: 0.4.0")
    print("- current conformance engine: 0.5.0")
    print("- manual workbooks: 3 scorer-specific plus 1 master, DOCX and PDF")
    print("- manual workbook status: draft, scoring prohibited")
    print("- v1 release permitted: no")
    print("- active protocol: candidate, 3 scorers, 9 submissions, 0 packet IDs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
