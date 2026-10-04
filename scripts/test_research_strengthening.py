"""Failure-path checks for supplementary research tooling; no network."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_jev_claim_pilot as pilot
import validate_research_strengthening as validation


class ResearchChecks(unittest.TestCase):
    def setUp(self):
        self.design = json.loads(pilot.DESIGN.read_text())
        self.response = {"model": self.design["model"], "answers": {c["id"]: {"type": "choice", "choice": c["expected"], "confidence": 1.0, "probabilities": {label: float(label == c["expected"]) for label in pilot.LABELS}} for c in self.design["cases"]}}

    def test_reference_labels_do_not_enter_request(self):
        altered = copy.deepcopy(self.design)
        for c in altered["cases"]:
            c["expected"] = "insufficient"
        self.assertEqual(pilot.prepare(self.design), pilot.prepare(altered))
        self.assertNotIn('"expected"', json.dumps(pilot.prepare(self.design)))

    def test_missing_answer_is_failure_not_insufficient(self):
        del self.response["answers"]["J01"]
        with self.assertRaises(ValueError):
            pilot.analyze(self.design, self.response)

    def test_passage_questions_are_isolated_and_reference_free(self):
        design = json.loads((pilot.ROOT / "research/strengthening/passage-cases.json").read_text())
        request = pilot.prepare(design)
        self.assertEqual(request["state"], {})
        for case in design["cases"]:
            instructions = request["questions"][case["id"]]["instructions"]
            self.assertEqual(instructions["packet"], case["packet"])
            self.assertEqual(set(instructions), {"packet", "claim", "task"})
        changed = copy.deepcopy(design)
        for case in changed["cases"]:
            case["expected"] = "supported"
        self.assertEqual(request, pilot.prepare(changed))

    def test_passage_shared_source_leak_is_rejected(self):
        design = json.loads((pilot.ROOT / "research/strengthening/passage-cases.json").read_text())
        design["source_paths"] = ["README.md"]
        with self.assertRaisesRegex(ValueError, "must not share"):
            pilot.prepare(design)

    def test_unexpected_model_is_rejected(self):
        self.response["model"] = "other"
        with self.assertRaises(ValueError):
            pilot.analyze(self.design, self.response)

    def test_nonfinite_confidence_is_rejected(self):
        self.response["answers"]["J01"]["confidence"] = float("nan")
        with self.assertRaises(ValueError):
            pilot.analyze(self.design, self.response)

    def test_false_support_is_counted(self):
        self.response["answers"]["J07"] = {"type": "choice", "choice": "supported", "confidence": 1.0, "probabilities": {"supported": 1.0, "contradicted": 0.0, "insufficient": 0.0}}
        report = pilot.analyze(self.design, self.response)
        self.assertEqual(report["matches"], 7)
        self.assertEqual(report["false_support"], 1)
        self.assertEqual(report["scheduled"], 8)

    def test_missing_locator_is_rejected(self):
        original = validation.load
        def altered(name):
            value = original(name)
            if name == "claim-audit.json":
                value["findings"][0]["locator"] = "MISSING-LOCATOR-NEGATIVE-CONTROL"
            return value
        with patch.object(validation, "load", side_effect=altered):
            with self.assertRaisesRegex(ValueError, "Unresolved locator"):
                validation.build()

    def test_wrong_expected_result_is_rejected(self):
        original = validation.load
        def altered(name):
            value = original(name)
            if name == "adversarial-cases.json":
                value["cases"][0]["expected"] = {"finding": 2}
            return value
        with patch.object(validation, "load", side_effect=altered):
            with self.assertRaisesRegex(ValueError, "A01"):
                validation.build()


if __name__ == "__main__":
    unittest.main()
