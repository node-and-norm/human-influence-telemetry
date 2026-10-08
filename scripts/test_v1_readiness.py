#!/usr/bin/env python3
"""Negative tests for candidate checks. No readiness or human review is asserted."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from validate_v1_implementation_packet import validate as validate_packet
from validate_v1_readiness import validate as validate_release
from v1_readiness_checks import check_artifacts, check_eligibility_record


ROOT = Path(__file__).resolve().parents[1]
PACKET = Path("implementation/v1.0.0-candidate/manifest.candidate.json")
LOCK = Path("release/v1.0.0/contract-freeze.candidate.json")
REGISTER = Path("release/v1.0.0/gate-register.json")


class CandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="hit-readiness-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))

    def load(self, relative: Path) -> dict:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def save(self, relative: Path, value: dict) -> None:
        (self.root / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def test_current_controls_pass_only_staging(self) -> None:
        self.assertEqual([], validate_packet(self.root))
        self.assertEqual([], validate_release(self.root))
        self.assertTrue(validate_packet(self.root, "audit-ready"))
        self.assertTrue(validate_release(self.root, "release-ready"))

    def test_readiness_commands_return_nonzero(self) -> None:
        for script, mode in (
            ("validate_v1_implementation_packet.py", "audit-ready"),
            ("validate_v1_readiness.py", "release-ready"),
        ):
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / script), "--root", str(self.root), "--mode", mode],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn("remains prohibited", result.stdout)

    def test_missing_declared_artifact_fails(self) -> None:
        (self.root / "docs/migration-guide-v0.1.0-to-v0.4.0.md").unlink()
        self.assertTrue(validate_packet(self.root))

    def test_omitted_required_artifact_fails(self) -> None:
        manifest = self.load(PACKET)
        manifest["required_artifacts"] = [item for item in manifest["required_artifacts"] if item["path"] != "SPECIFICATION.md"]
        self.save(PACKET, manifest)
        self.assertIn("implementation manifest omits required public artifacts", validate_packet(self.root))

    def test_path_traversal_fails(self) -> None:
        manifest = self.load(PACKET)
        manifest["required_artifacts"][0]["path"] = "../outside.txt"
        self.save(PACKET, manifest)
        self.assertTrue(any("unsafe" in item for item in validate_packet(self.root)))

    def test_absolute_path_fails(self) -> None:
        failures = []
        check_artifacts(self.root, [{"path": str(self.root / "README.md")}], failures)
        self.assertTrue(failures)

    def test_symlink_escape_fails(self) -> None:
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("outside evidence", encoding="utf-8")
        (self.root / "escape.txt").symlink_to(outside)
        failures = []
        check_artifacts(self.root, [{"path": "escape.txt"}], failures)
        self.assertTrue(any("escapes" in item for item in failures))

    def test_hash_is_checked_against_bytes(self) -> None:
        manifest = self.load(PACKET)
        manifest["required_artifacts"][0]["sha256"] = "0" * 64
        self.save(PACKET, manifest)
        self.assertTrue(any("SHA-256 mismatch" in item for item in validate_packet(self.root)))
        item = manifest["required_artifacts"][0]
        item["sha256"] = hashlib.sha256((self.root / item["path"]).read_bytes()).hexdigest()
        self.save(PACKET, manifest)
        self.assertEqual([], validate_packet(self.root))

    def test_fabricated_completion_cannot_pass(self) -> None:
        manifest = self.load(PACKET)
        manifest.update(status="audit_ready", audit_permitted=True, exact_repository_commit="a" * 40, packet_digest="b" * 64, missing_before_activation=[])
        for item in manifest["required_artifacts"]:
            item["sha256"] = hashlib.sha256((self.root / item["path"]).read_bytes()).hexdigest()
        self.save(PACKET, manifest)
        self.assertTrue(validate_packet(self.root, "audit-ready"))
        lock = self.load(LOCK)
        lock.update(status="complete", release_permitted=True)
        self.save(LOCK, lock)
        register = self.load(REGISTER)
        register["status"] = "complete"
        for item in register["gates"]:
            item["status"] = "satisfied"
        self.save(REGISTER, register)
        self.assertTrue(validate_release(self.root, "release-ready"))

    def test_dropped_replication_safeguard_fails(self) -> None:
        lock = self.load(LOCK)
        lock["empirical_track"]["blocking_gates"].pop()
        self.save(LOCK, lock)
        self.assertTrue(any("replication-preparation safeguards" in item for item in validate_release(self.root)))

    def test_empirical_state_and_separation_cannot_drift(self) -> None:
        baseline = self.load(LOCK)
        for field, value in (("status", "completed"), ("blocks_stable_release", True),
                             ("current_contract_replication", "supported"), ("protocol_rules_changed", True)):
            lock = copy.deepcopy(baseline)
            lock["empirical_track"][field] = value
            self.save(LOCK, lock)
            self.assertTrue(validate_release(self.root), field)

    def test_target_component_keys_and_gate_register_cannot_drift(self) -> None:
        baseline = self.load(LOCK)
        lock = copy.deepcopy(baseline)
        lock["target_component_versions"] = {"unknown_component": "1.0.0"}
        self.save(LOCK, lock)
        self.assertTrue(any("five component keys" in item for item in validate_release(self.root)))
        lock = copy.deepcopy(baseline)
        lock["gate_register"] = "release/v1.0.0/unverified-register.json"
        self.save(LOCK, lock)
        self.assertTrue(any("declared gate register" in item for item in validate_release(self.root)))

    def test_malformed_json_returns_nonzero(self) -> None:
        (self.root / PACKET).write_text("{malformed", encoding="utf-8")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_v1_implementation_packet.py"),
                                 "--root", str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(1, result.returncode)
        self.assertIn("malformed candidate controls", result.stdout)

    def test_premature_scoring_fails(self) -> None:
        path = Path("validation/v0.7.0/protocol-lock.candidate.json")
        protocol = self.load(path)
        protocol["scoring_permitted"] = True
        self.save(path, protocol)
        self.assertTrue(any("prohibit scoring" in item for item in validate_release(self.root)))

    def test_gate_evidence_path_is_checked(self) -> None:
        register = self.load(REGISTER)
        register["gates"][0]["evidence_paths"] = ["missing-evidence.json"]
        self.save(REGISTER, register)
        self.assertTrue(any("missing artifact" in item for item in validate_release(self.root)))

    def test_task_catalog_cannot_drop_tasks(self) -> None:
        path = Path("implementation/v1.0.0-candidate/task-catalog.json")
        catalog = self.load(path)
        catalog["tasks"].pop()
        self.save(path, catalog)
        self.assertTrue(any("every required task" in item for item in validate_packet(self.root)))

    def test_task_catalog_cannot_substitute_valid_vector(self) -> None:
        path = Path("implementation/v1.0.0-candidate/task-catalog.json")
        catalog = self.load(path)
        catalog["selected_invalid_vectors"][0]["case_id"] = "CR-VALID-001"
        self.save(path, catalog)
        self.assertTrue(any("invalid-vector selection" in item for item in validate_packet(self.root)))

    def test_task_catalog_inputs_cannot_be_dropped_or_substituted(self) -> None:
        path = Path("implementation/v1.0.0-candidate/task-catalog.json")
        baseline = self.load(path)
        for field in baseline["inputs"]:
            catalog = copy.deepcopy(baseline)
            del catalog["inputs"][field]
            self.save(path, catalog)
            self.assertTrue(any("exact four declared input" in item for item in validate_packet(self.root)), field)
        catalog = copy.deepcopy(baseline)
        catalog["inputs"]["canonical_valid"] = "README.md"
        self.save(path, catalog)
        self.assertTrue(any("exact four declared input" in item for item in validate_packet(self.root)))
        catalog = copy.deepcopy(baseline)
        catalog["inputs"]["comparison_sources"] = ["validation/test-vectors/rater-a.json"] * 2
        self.save(path, catalog)
        self.assertTrue(any("exact four declared input" in item for item in validate_packet(self.root)))

    def eligibility(self, **changes: object) -> list[str]:
        record = {
            "identity": "TEST-REVIEWER-NOT-A-REAL-PERSON",
            "human_supplied_declarations": True, "is_human": True, "not_hit_author": True,
            "no_material_packet_contribution": True, "used_public_material_only": True,
            "competence": "Synthetic declaration for software test only",
            "conflicts": "Synthetic declaration for software test only",
            "prior_exposure": "Synthetic declaration for software test only",
        }
        record.update(changes)
        path = self.root / "test-eligibility.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        reference = {"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        failures: list[str] = []
        check_eligibility_record(self.root, reference, failures)
        return failures

    def test_model_cannot_be_independent_human(self) -> None:
        self.assertTrue(self.eligibility(is_human=False, identity="Codex"))

    def test_self_review_is_ineligible(self) -> None:
        self.assertTrue(self.eligibility(not_hit_author=False))
        self.assertTrue(self.eligibility(identity="Mark Julius Banasihan"))

    def test_material_contributor_is_ineligible(self) -> None:
        self.assertTrue(self.eligibility(no_material_packet_contribution=False))

    def test_missing_competence_or_disclosure_fails(self) -> None:
        for field in ("identity", "competence", "conflicts", "prior_exposure"):
            self.assertTrue(self.eligibility(**{field: ""}))

    def test_public_auditor_shape_is_used_for_eligibility(self) -> None:
        self.assertEqual([], self.eligibility())
        for field in ("human_supplied_declarations", "is_human", "not_hit_author",
                      "no_material_packet_contribution", "used_public_material_only"):
            self.assertTrue(self.eligibility(**{field: False}), field)
        self.assertTrue(self.eligibility(undocumented_eligibility_field=True))

    def test_submission_template_is_not_a_submission(self) -> None:
        base = self.root / "implementation/v1.0.0-candidate"
        schema = json.loads((base / "audit-submission.schema.json").read_text(encoding="utf-8"))
        template = json.loads((base / "audit-submission.example.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        self.assertFalse(list(validator.iter_errors(template)))
        submitted = copy.deepcopy(template)
        submitted["record_state"] = "submitted"
        self.assertTrue(list(validator.iter_errors(submitted)))

    def synthetic_submission(self) -> tuple[Draft202012Validator, dict]:
        """Structural test data only. No person, signature, or audit is asserted."""
        base = self.root / "implementation/v1.0.0-candidate"
        schema = json.loads((base / "audit-submission.schema.json").read_text(encoding="utf-8"))
        record = json.loads((base / "audit-submission.example.json").read_text(encoding="utf-8"))
        file_ref = {"path": "SYNTHETIC-TEST-NOT-EVIDENCE.txt", "sha256": "0" * 64, "digest_method": "file_bytes"}
        text = "Synthetic software test only; no human declaration or real event"
        record.update(
            record_state="submitted", audit_id="SYNTHETIC-TEST-NOT-AN-AUDIT",
            auditor={"identity": text, "human_supplied_declarations": True, "is_human": True,
                     "not_hit_author": True, "no_material_packet_contribution": True,
                     "used_public_material_only": True, "competence": text, "conflicts": text, "prior_exposure": text},
            frozen_packet={"repository_commit": "0" * 40, "packet_digest_sha256": "0" * 64,
                           "activation_record": file_ref, "input_hashes": [file_ref], "expected_output_hashes": [file_ref]},
            environment={"operating_system": text, "python_version": text, "shell": text,
                         "dependency_inventory": file_ref, "checkout_clean_before_install": True},
            audit_disposition="pass_no_release_blocker",
            signature={"signed_by": text, "signed_at": "2000-01-01T00:00:00Z", "attestation": text, "signature_record": file_ref},
        )
        for task in record["tasks"].values():
            task.update(outcome="pass", summary=text, public_references=[text], evidence_files=[file_ref],
                        commands=[{"command": text, "working_directory": text, "exit_code": 0,
                                   "stdout": file_ref, "stderr": file_ref, "elapsed_seconds": 0}])
        return Draft202012Validator(schema), record

    def test_submission_failure_cannot_have_passing_disposition(self) -> None:
        validator, record = self.synthetic_submission()
        self.assertFalse(list(validator.iter_errors(record)))
        for outcome in (None, "fail", "blocked"):
            changed = copy.deepcopy(record)
            changed["tasks"]["rule_reconstruction"]["outcome"] = outcome
            self.assertTrue(list(validator.iter_errors(changed)))

    def test_submission_ineligible_auditor_cannot_pass(self) -> None:
        validator, record = self.synthetic_submission()
        for field in ("is_human", "not_hit_author", "no_material_packet_contribution", "used_public_material_only"):
            changed = copy.deepcopy(record)
            changed["auditor"][field] = False
            self.assertTrue(list(validator.iter_errors(changed)), field)

    def test_submission_cannot_omit_task_or_hide_open_blocker(self) -> None:
        validator, record = self.synthetic_submission()
        changed = copy.deepcopy(record)
        del changed["tasks"]["private_knowledge_register"]
        self.assertTrue(list(validator.iter_errors(changed)))
        record["findings"] = [{"finding_id": "SYNTHETIC-TEST", "task_id": "rule_reconstruction",
                               "kind": "ambiguous_rule", "description": "Synthetic test only",
                               "severity": "release_blocking", "status": "open", "evidence_references": ["Synthetic test only"]}]
        self.assertTrue(list(validator.iter_errors(record)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
