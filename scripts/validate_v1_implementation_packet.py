#!/usr/bin/env python3
"""Validate the candidate HIT v1 clean-room implementation packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from v1_readiness_checks import check_artifacts, check_eligibility_record, checked_path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "implementation" / "v1.0.0-candidate"
README = BASE / "README.md"
PROTOCOL = BASE / "audit-protocol.md"
MANIFEST = BASE / "manifest.candidate.json"


def check_task_catalog(root: Path, base: Path, tasks: set[str], failures: list[str]) -> None:
    path = base / "task-catalog.json"
    if not path.is_file():
        failures.append("missing implementation task catalog")
        return
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog.get("status") != "candidate_unfrozen" or catalog.get("audit_permitted") is not False:
        failures.append("task catalog must remain unfrozen and audit prohibited")
    if catalog.get("exact_repository_commit") is not None or catalog.get("expected_output_hashes") is not None:
        failures.append("task catalog must not claim frozen inputs or outputs")
    if catalog.get("audit_protocol_id") != "HIT-CRI-V100-001":
        failures.append("task catalog protocol identity changed")
    expected_inputs = {
        "canonical_valid": "fixtures/v0.4.0-canonical-example.json",
        "complete_record_suite": "fixtures/v0.5.0-conformance/complete-record-cases.json",
        "migration_source": "case-studies/assessments/toeslagenaffaire-harm-period.json",
        "comparison_sources": ["validation/test-vectors/rater-a.json", "validation/test-vectors/rater-b.json"],
    }
    if catalog.get("inputs") != expected_inputs:
        failures.append("task catalog must retain the exact four declared input keys and source paths")
    entries = catalog.get("tasks", [])
    if not isinstance(entries, list) or any(not isinstance(item, dict) for item in entries):
        failures.append("task catalog entries must be objects")
        return
    if {item.get("task_id") for item in entries} != tasks or len(entries) != len(tasks):
        failures.append("task catalog must contain every required task exactly once")
    checked_path(root, catalog.get("guide"), failures, "task catalog guide")
    for name, references in catalog.get("inputs", {}).items():
        for reference in references if isinstance(references, list) else [references]:
            checked_path(root, reference, failures, f"task catalog input {name}")
    for entry in entries:
        references = entry.get("public_references")
        if not isinstance(references, list) or not references:
            failures.append(f"task {entry.get('task_id')} requires public references")
            continue
        for reference in references:
            checked_path(root, reference, failures, f"task {entry.get('task_id')} reference")
    suite_path = checked_path(root, catalog.get("inputs", {}).get("complete_record_suite"), failures, "task vector suite")
    if suite_path is not None:
        suite = json.loads(suite_path.read_text(encoding="utf-8"))
        cases = {item["case_id"]: item for item in suite["cases"]}
        selected = catalog.get("selected_invalid_vectors", [])
        if len(selected) < 3 or len({item.get("case_id") for item in selected}) != len(selected):
            failures.append("task catalog requires at least three distinct invalid vectors")
        for item in selected:
            case = cases.get(item.get("case_id"))
            if case is None or case.get("expected_valid") is not False or item.get("expected_valid") is not False:
                failures.append(f"task catalog invalid-vector selection is invalid: {item.get('case_id')}")
            elif not item.get("required_error_codes") or not set(item["required_error_codes"]).issubset(case.get("expected_error_codes", [])):
                failures.append(f"task catalog error codes disagree with vector: {item.get('case_id')}")


def validate(root: Path = ROOT, mode: str = "staging") -> list[str]:
    failures: list[str] = []
    base = root / "implementation" / "v1.0.0-candidate"
    readme_path = base / "README.md"
    protocol_path = base / "audit-protocol.md"
    manifest_path = base / "manifest.candidate.json"

    for path in (readme_path, protocol_path, manifest_path):
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty file: {path.relative_to(root)}")

    if failures:
        return failures

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("packet_id") != "HIT-IMPLEMENTATION-V100-CANDIDATE-001":
        failures.append("implementation packet ID changed")
    if manifest.get("status") != "candidate_incomplete":
        failures.append("implementation packet must remain candidate_incomplete")
    if manifest.get("audit_protocol_id") != "HIT-CRI-V100-001":
        failures.append("implementation packet audit protocol ID changed")
    if manifest.get("audit_permitted") is not False:
        failures.append("clean-room audit must remain prohibited")
    if manifest.get("target_release") != "0.9.0":
        failures.append("implementation packet must target v0.9.0")
    if manifest.get("target_stable_release") != "1.0.0":
        failures.append("implementation packet stable target must remain 1.0.0")
    if manifest.get("exact_repository_commit") is not None:
        failures.append("candidate implementation packet must not claim a frozen commit")
    if manifest.get("packet_digest") is not None:
        failures.append("candidate implementation packet must not claim a final digest")
    if manifest.get("private_author_explanation_allowed") is not False:
        failures.append("private author explanation must be prohibited")
    if manifest.get("model_audit_counts_as_human_reliability_evidence") is not False:
        failures.append("model audit must not count as human reliability evidence")
    if manifest.get("failed_audit_must_be_published") is not True:
        failures.append("failed clean-room audits must be publishable evidence")
    if manifest.get("independent_human_auditor_required") is not True:
        failures.append("candidate audit must require an independent human auditor")
    artifacts = manifest.get("required_artifacts")
    check_artifacts(root, artifacts, failures)
    required_paths = {
        "SPECIFICATION.md", "docs/application-handbook.md",
        "schema/hit-assessment.schema.json", "schema/hit-dimension-catalog.json",
        "docs/adjacent-system-boundaries.md", "compatibility/hit-compatibility-manifest.json",
        "docs/migration-guide-v0.1.0-to-v0.4.0.md", "docs/conformance-error-catalog.md",
        "fixtures/v0.5.0-conformance/complete-record-cases.json", "RESEARCH.md", "LIMITATIONS.md",
        "implementation/v1.0.0-candidate/audit-protocol.md",
        "implementation/v1.0.0-candidate/quickstart.md", "implementation/v1.0.0-candidate/task-catalog.json",
        "implementation/v1.0.0-candidate/audit-submission.schema.json",
        "implementation/v1.0.0-candidate/audit-submission.example.json",
    }
    present_paths = {item.get("path") for item in artifacts if isinstance(item, dict)} if isinstance(artifacts, list) else set()
    if not required_paths.issubset(present_paths):
        failures.append("implementation manifest omits required public artifacts")
    eligibility = manifest.get("independent_auditor_eligibility_record")
    if eligibility is not None:
        check_eligibility_record(root, eligibility, failures)

    required_tasks = {
        "fresh_install",
        "version_reconstruction",
        "valid_assessment_validation",
        "invalid_vector_error_explanation",
        "rule_reconstruction",
        "migration_plan_generation",
        "comparison_reproduction",
        "adjacent_system_boundary_explanation",
        "private_knowledge_register",
        "audit_disposition",
    }
    if set(manifest.get("required_runtime_tasks", [])) != required_tasks:
        failures.append("clean-room task set changed")
    check_task_catalog(root, base, required_tasks, failures)

    missing = set(manifest.get("missing_before_activation", []))
    required_missing = {
        "exact_repository_commit",
        "packet_digest",
        "dependency_lock_or_exact_environment_record",
        "expected_output_hashes",
        "audit_submission_schema",
        "independent_auditor_eligibility_record",
        "exact_commit_validation",
    }
    if not required_missing.issubset(missing):
        failures.append("implementation packet is missing required activation blockers")

    readme = readme_path.read_text(encoding="utf-8")
    for phrase in (
        "Status:** Candidate, incomplete",
        "Private explanation permitted:** No",
        "install the package in a fresh environment",
        "record every point where the public packet is ambiguous",
        "does not establish inter-rater reliability",
    ):
        if phrase not in readme:
            failures.append(f"implementation README missing control text: {phrase}")

    protocol = protocol_path.read_text(encoding="utf-8")
    for phrase in (
        "Protocol ID:** `HIT-CRI-V100-001`",
        "Status:** Candidate, audit prohibited",
        "Can a technically competent external reviewer install, operate, and explain",
        "private author explanation",
        "fail_release_blocking_defect",
        "blocks `v0.9.0` promotion and `v1.0.0` release",
    ):
        if phrase not in protocol:
            failures.append(f"audit protocol missing control text: {phrase}")

    schema_path = base / "audit-submission.schema.json"
    example_path = base / "audit-submission.example.json"
    for path in (schema_path, example_path):
        if not path.is_file():
            failures.append(f"missing audit submission control: {path.relative_to(root)}")
    if schema_path.is_file() and example_path.is_file():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        example = json.loads(example_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        for error in Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).iter_errors(example):
            failures.append(f"audit submission example: {error.json_path}: {error.message}")
        if example.get("record_state") != "template":
            failures.append("candidate audit submission example must remain a template")

    if mode == "audit-ready":
        check_artifacts(root, manifest.get("required_artifacts"), failures, hashes_required=True)
        for item in sorted(missing):
            failures.append(f"audit activation prerequisite unresolved: {item}")
        if eligibility is None:
            failures.append("independent human auditor eligibility evidence is absent")
        failures.append(
            "audit-ready acceptance is not implemented for this candidate: audit remains prohibited; "
            "a reviewed activation policy and maintainer decision are required"
        )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("staging", "audit-ready"), default="staging")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (for isolated checks)")
    args = parser.parse_args()
    try:
        failures = validate(args.root.resolve(), args.mode)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, SchemaError) as exc:
        failures = [f"unreadable or malformed candidate controls: {exc}"]
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("HIT v1 implementation packet staging consistency passed; not audit readiness")
    print("- packet status: candidate_incomplete")
    print("- audit permitted: no")
    print("- target release: 0.9.0")
    print("- stable target: 1.0.0")
    print("- private author explanation: prohibited")
    return 0


if __name__ == "__main__":
    sys.exit(main())
