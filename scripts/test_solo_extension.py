#!/usr/bin/env python3
"""Offline consistency tests; narrative fixtures are not research results."""
import copy
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import validate_solo_extension as check


class ExtensionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hit-extension-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.originals = {path: check.read(check.ROOT, path) for path in (*check.PROTECTED, *check.INPUTS)}
        for path, raw in self.originals.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        self.freeze = "f" * 40
        def committed(_, commit, path):
            if (commit == check.BASE_COMMIT and path in check.PROTECTED) or (commit == self.freeze and path in check.INPUTS):
                return self.originals[path]
            raise subprocess.CalledProcessError(128, "mock git show")
        self.patcher = patch.object(check, "committed", committed)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

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
