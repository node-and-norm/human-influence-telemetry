#!/usr/bin/env python3
"""Negative checks for development records; never authenticate author statements."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import validate_development_review as check


class DevelopmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hit-development-review-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        register = check.decoded((check.ROOT / check.REGISTER).read_bytes())
        paths = {check.AUTHOR, check.ORIGINAL, check.REGISTER, check.MANUSCRIPT, check.EXTENSION, register["historical_audit"]["path"]}
        paths.update(item["path"] for claim in register["claims"] for item in claim["evidence"])
        for name in paths:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((check.ROOT / name).read_bytes())
        patcher = patch.object(check, "extension_check", return_value={"results_present": True})
        patcher.start()
        self.addCleanup(patcher.stop)

    def mutate(self, path, change):
        target = self.root / path
        value = check.decoded(target.read_bytes())
        change(value)
        target.write_text(json.dumps(value))

    def test_current_records_are_consistent_without_semantic_acceptance(self):
        self.assertFalse(check.evaluate(self.root)["scientific_acceptance_conferred"])

    def test_author_false_promotions_and_boolean_impostors(self):
        original = (self.root / check.AUTHOR).read_bytes()
        for key in ("independent_review", "pre_model_reference", "scientific_conclusion_eligible", "release_gate_satisfied"):
            for value in (True, 0, "false"):
                (self.root / check.AUTHOR).write_bytes(original)
                self.mutate(check.AUTHOR, lambda d: d.update({key: value}))
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    check.evaluate(self.root)

    def test_unresolved_cannot_retain_accepted_values(self):
        self.mutate(check.AUTHOR, lambda d: d["decisions"][2].update(disposition="unresolved"))
        with self.assertRaises(ValueError): check.evaluate(self.root)

    def test_accepted_record_needs_question_response_scope_and_typed_value(self):
        original = (self.root / check.AUTHOR).read_bytes()
        for change in ({"question": ""}, {"verbatim_response": None}, {"recorded_scope": ""}, {"accepted_values": {"Judgment": True}}):
            (self.root / check.AUTHOR).write_bytes(original)
            self.mutate(check.AUTHOR, lambda d: d["decisions"][2].update(change))
            with self.subTest(change=change), self.assertRaises(ValueError): check.evaluate(self.root)

    def test_later_legitimate_reply_is_not_frozen_out(self):
        self.mutate(check.AUTHOR, lambda d: d["decisions"][1].update(disposition="accept", verbatim_response="Fixture reply only", recorded_scope="Fixture scope only", accepted_values={"Counsel": "IE"}))
        self.assertEqual(check.evaluate(self.root)["author_decisions"], 7)

    def test_missing_author_decision_and_duplicate_manuscript_id(self):
        original = (self.root / check.AUTHOR).read_bytes()
        self.mutate(check.AUTHOR, lambda d: d["decisions"].pop())
        with self.assertRaises(ValueError): check.evaluate(self.root)
        (self.root / check.AUTHOR).write_bytes(original)
        self.mutate(check.REGISTER, lambda d: d["claims"].append(copy.deepcopy(d["claims"][0])))
        with self.assertRaises(ValueError): check.evaluate(self.root)

    def test_invalid_or_missing_evidence_and_false_manuscript_acceptance(self):
        original = (self.root / check.REGISTER).read_bytes()
        changes = [lambda d: d["claims"][0].update(scientific_conclusion_eligible=0), lambda d: d["claims"][0].update(author_review="accepted"), lambda d: d["claims"][0].update(evidence=[]), lambda d: d["claims"][0]["evidence"][0].update(locator="NONEXISTENT-LOCATOR"), lambda d: d["claims"][0]["evidence"][0].update(path="../outside")]
        for change in changes:
            (self.root / check.REGISTER).write_bytes(original)
            self.mutate(check.REGISTER, change)
            with self.subTest(change=change), self.assertRaises(ValueError): check.evaluate(self.root)

    def test_missing_extension_or_duplicate_json_key_rejected(self):
        (self.root / check.EXTENSION).unlink()
        with self.assertRaises(ValueError): check.evaluate(self.root)
        with self.assertRaises(ValueError): check.decoded(b'{"decisions":[],"decisions":[]}')


if __name__ == "__main__":
    unittest.main()
