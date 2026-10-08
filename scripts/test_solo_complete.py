#!/usr/bin/env python3
"""Boundary tests for a proposed documentary record, not tests of source truth."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_solo_complete import BASE, ROOT, evaluate


class DraftRecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hit-solo-complete-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))

    def mutate(self, name, change):
        path = self.root / BASE / name
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_current_draft_is_conforming_but_unaccepted(self):
        result = evaluate(self.root)
        self.assertTrue(result["conformance_valid"])
        self.assertFalse(result["source_truth_validated"])
        self.assertFalse(result["scientific_conclusion_eligible"])
        self.assertFalse(result["source_subset_judgments_recomputed"])

    def test_premature_acceptance_is_rejected(self):
        self.mutate("review-status.json", lambda data: data.update(author_adjudication="accepted"))
        with self.assertRaisesRegex(ValueError, "unsupported promotion"):
            evaluate(self.root)

    def test_false_independence_is_rejected(self):
        self.mutate("review-status.json", lambda data: data.update(independent_review=True))
        with self.assertRaisesRegex(ValueError, "unsupported promotion"):
            evaluate(self.root)

    def test_premature_release_credit_is_rejected(self):
        self.mutate("review-status.json", lambda data: data.update(release_gate_satisfied=True))
        with self.assertRaisesRegex(ValueError, "unsupported promotion"):
            evaluate(self.root)

    def test_frozen_plan_cannot_be_rewritten(self):
        path = self.root / BASE / "plan.md"
        path.write_text(path.read_text() + "\nChanged after findings.\n")
        with self.assertRaisesRegex(ValueError, "frozen plan bytes changed"):
            evaluate(self.root)

    def test_expanding_event_to_period_is_rejected(self):
        self.mutate("assessment.draft.json", lambda data: data["period"].update(start="2020-01-01"))
        with self.assertRaisesRegex(ValueError, "event boundary"):
            evaluate(self.root)

    def test_broken_claim_reference_is_rejected(self):
        self.mutate("assessment.draft.json", lambda data: data["substantive_findings"][1]["supporting_claim_ids"].append("MISSING"))
        with self.assertRaisesRegex(ValueError, "does not conform"):
            evaluate(self.root)

    def test_missing_source_ledger_is_rejected(self):
        (self.root / BASE / "source-ledger.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing or empty"):
            evaluate(self.root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
