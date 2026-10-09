#!/usr/bin/env python3
"""Offline consistency tests; narrative fixtures are not research results."""
import copy
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import validate_solo_extension as check
import frozen_release_context as context


class ExtensionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hit-extension-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.originals = {path: check.read(check.ROOT, path) for path in (*check.PROTECTED, *check.INPUTS)}
        for path in (context.AMENDMENT_PATH, *(item[0] for item in context.SNAPSHOTS.values())):
            self.originals[path] = check.read(check.ROOT, path)
        self.base_originals = {**self.originals,
                               **{path: self.originals[snapshot] for path, (snapshot, _) in context.SNAPSHOTS.items()}}
        self.untracked = set()
        for path, raw in self.originals.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        self.freeze = "f" * 40
        def committed(_, commit, path):
            if (commit == check.BASE_COMMIT and path in check.PROTECTED) or (commit == self.freeze and path in check.INPUTS):
                return self.base_originals[path] if commit == check.BASE_COMMIT else self.originals[path]
            raise subprocess.CalledProcessError(128, "mock git show")
        self.patcher = patch.object(check, "committed", committed)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        def git(_, *args):
            if args[0] == "show":
                commit, path = args[1].split(":", 1)
                if commit == check.BASE_COMMIT and path in self.base_originals:
                    return self.base_originals[path]
            elif args[0] == "ls-files" and args[-1] not in self.untracked:
                return f"100644 {'0' * 40} 0\t{args[-1]}\n".encode()
            raise subprocess.CalledProcessError(128, "mock git read")
        patcher = patch.object(context, "git", git)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, name, value):
        (self.root / check.BASE / name).write_bytes(check.encoded(value))

    def fixture_results(self):
        prose = "Software-test fixture only; no scientific interpretation is asserted."
        return {"study_id": check.STUDY, "protocol_commit": self.freeze, "assessor_type": "ai_assistant",
                "status": "completed_pending_author_review", "independent_review": False,
                "release_gate_satisfied": False, "author_adjudication": "pending_for_extension",
                "scientific_conclusion_eligible": False,
                "conditions": [{"id": name, "questions": [
                    {"id": f"Q{n}", "baseline_answer": prose, "hit_answer": prose, "comparison": "unresolved",
                     "reason": prose, "evidence_refs": ["EC-PACKET"]} for n in range(1, 7)],
                    "impacts": [{"dimension": dimension, "disposition": "unresolved", "reason": prose,
                                 "evidence_refs": ["EC-PACKET"]} for dimension in check.DIMENSIONS],
                    "overall_interpretation": prose, "limitations": [prose]} for name in ("S05", "S06", "S07")]}

    def with_results(self, data=None):
        self.write("results.json", self.fixture_results() if data is None else data)
        (self.root / check.BASE / "report.md").write_text("Software-test fixture only.\n")

    def test_prepared_inputs_cannot_claim_results_or_acceptance(self):
        report = check.evaluate(self.root)
        self.assertFalse(report["results_present"])
        self.assertFalse(report["source_truth_validated"])
        self.assertFalse(report["interpretations_recomputed"])
        self.assertFalse(report["release_gate_satisfied"])
        self.assertEqual(report["historical_snapshot_paths"], [".zenodo.json", "CITATION.cff"])
        self.assertFalse(report["current_release_metadata_validated_here"])

    def test_current_metadata_updates_leave_original_extension_design_unchanged(self):
        before = (self.root / check.BASE / "design.json").read_bytes()
        for path in ("CITATION.cff", ".zenodo.json"):
            (self.root / path).write_bytes(b"Current release metadata, checked separately.\n")
        self.assertFalse(check.evaluate(self.root)["current_release_metadata_validated_here"])
        self.assertEqual(before, (self.root / check.BASE / "design.json").read_bytes())

    def test_snapshot_failure_is_not_hidden_by_current_metadata(self):
        snapshot = context.SNAPSHOTS["CITATION.cff"][0]
        (self.root / snapshot).write_bytes(b"Altered snapshot")
        with self.assertRaisesRegex(ValueError, "snapshot digest"):
            check.evaluate(self.root)

    def test_normative_and_other_protected_paths_remain_strict(self):
        for path in ("SPECIFICATION.md", "evidence/claim-evidence-map.json", "release/v1.0.0/gate-register.json"):
            with self.subTest(path=path):
                target = self.root / path
                target.write_bytes(self.originals[path] + b"\n")
                with self.assertRaisesRegex(ValueError, "Protected base input changed"):
                    check.evaluate(self.root)
                target.write_bytes(self.originals[path])

    def test_complete_fixture_retains_pending_review(self):
        self.with_results()
        report = check.evaluate(self.root)
        self.assertTrue(report["results_present"])
        self.assertEqual(report["author_adjudication"], "pending_for_extension")

    def test_missing_duplicate_unknown_or_reordered_rows_rejected(self):
        mutations = [lambda r: r["conditions"].pop(),
                     lambda r: r["conditions"][0].update(id="S06"),
                     lambda r: r["conditions"][0]["questions"].pop(),
                     lambda r: r["conditions"][0]["questions"][0].update(id="Q9"),
                     lambda r: r["conditions"][0]["impacts"].pop(),
                     lambda r: r["conditions"][0]["impacts"].reverse()]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                result = self.fixture_results()
                mutation(result)
                self.with_results(result)
                with self.assertRaises(ValueError):
                    check.evaluate(self.root)

    def test_unsupported_promotions_and_scalar_score_fields_rejected(self):
        mutations = [lambda r: r.update(independent_review=True), lambda r: r.update(independent_review=0),
                     lambda r: r.update(release_gate_satisfied=True), lambda r: r.update(author_adjudication="accepted"),
                     lambda r: r.update(scientific_conclusion_eligible=True),
                     lambda r: r["conditions"][0]["impacts"][0].update(score=2)]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                result = self.fixture_results()
                mutation(result)
                self.with_results(result)
                with self.assertRaises(ValueError):
                    check.evaluate(self.root)

    def test_missing_narrative_bad_references_and_unknown_comparisons_rejected(self):
        mutations = [lambda r: r["conditions"][0]["questions"][0].update(reason=" "),
                     lambda r: r["conditions"][0]["questions"][0].update(evidence_refs=["MISSING"]),
                     lambda r: r["conditions"][0]["questions"][0].update(evidence_refs=["EC-PACKET", "EC-PACKET"]),
                     lambda r: r["conditions"][0]["questions"][0].update(comparison="superior"),
                     lambda r: r["conditions"][0].update(limitations=[])]
        for mutation in mutations:
            result = self.fixture_results()
            mutation(result)
            self.with_results(result)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                check.evaluate(self.root)

    def test_missing_required_hash_and_changed_historical_input_rejected(self):
        design_path = self.root / check.BASE / "design.json"
        design = check.load(design_path)
        design["protected_sha256"].pop(check.PROTECTED[0])
        self.write("design.json", design)
        with self.assertRaises(ValueError):
            check.evaluate(self.root)
        design_path.write_bytes(self.originals[f"{check.BASE}/design.json"])
        (self.root / check.PROTECTED[0]).write_bytes(b"changed historical plan")
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_non_whitespace_change_cannot_be_hidden_by_hash_update(self):
        transformed = check.load(self.root / check.BASE / "formatting.json")
        transformed["passages"][0]["text"] += " Altered claim."
        self.write("formatting.json", transformed)
        design = check.load(self.root / check.BASE / "design.json")
        design["formatting_sha256"] = check.sha(check.encoded(transformed))
        self.write("design.json", design)
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_protocol_commit_must_bind_inputs(self):
        self.with_results()
        protocol = self.root / check.BASE / "PROTOCOL.md"
        protocol.write_bytes(protocol.read_bytes() + b"\nChanged after freeze.\n")
        design = check.expected_design(self.root, check.formatting(self.root))
        self.write("design.json", design)
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_result_cannot_name_base_commit_before_inputs_existed(self):
        result = self.fixture_results()
        result["protocol_commit"] = check.BASE_COMMIT
        self.with_results(result)
        with self.assertRaises(subprocess.CalledProcessError):
            check.evaluate(self.root)

    def test_prepare_refuses_overwrite(self):
        with self.assertRaises(ValueError):
            check.evaluate(self.root, prepare=True)

    def test_actual_formatting_preserves_source_words_and_attribution(self):
        packet = check.load(self.root / check.JEV / "sources.json")
        original = [(source, passage) for source in packet["sources"] for passage in source["passages"]]
        transformed = check.formatting(self.root)["passages"]
        for actual, (source, passage) in zip(transformed, reversed(original)):
            self.assertEqual(actual["id"], passage["id"])
            self.assertEqual(actual["text"].split(), passage["text"].split())
            self.assertEqual(actual["locator"], passage["locator"])
            self.assertEqual(actual["source"], {k: v for k, v in source.items() if k != "passages"})


if __name__ == "__main__":
    unittest.main()
