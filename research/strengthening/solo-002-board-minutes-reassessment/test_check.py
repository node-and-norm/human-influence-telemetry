#!/usr/bin/env python3
"""Exercise packet-preservation and review-state boundaries without editing files."""
from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

import check as packet_guard


class PacketGuardTests(unittest.TestCase):
    def reject_json_change(self, name, mutate):
        target = packet_guard.BASE / name
        original = packet_guard.read_json
        changed = copy.deepcopy(original(target))
        mutate(changed)

        def read(path):
            return changed if path == target else original(path)

        with patch.object(packet_guard, "read_json", side_effect=read):
            with self.assertRaises(ValueError):
                packet_guard.evaluate()

    def test_current_packet_retains_separate_completion_and_failure(self):
        report = packet_guard.evaluate()
        self.assertTrue(report["guardrails_pass"])
        self.assertEqual(report["protected_files_unchanged"], 42)
        self.assertEqual(report["new_author_dispositions"], 8)
        self.assertEqual(report["pending_author_decisions"], 0)
        self.assertEqual(report["personal_source_review"], "pending")
        self.assertFalse(report["source_truth_validated"])
        self.assertFalse(report["independent_human_review"])
        result = report["assessment_conformance"]
        self.assertFalse(result["valid"])
        self.assertEqual([(item["code"], item["path"]) for item in result["issues"]],
                         [("HIT-SCHEMA", "/aggregation/predeclared")])
        self.assertEqual(result["source"],
                         "research/strengthening/solo-002-board-minutes-reassessment/assessment.draft.json")

    def test_duplicate_path_cannot_replace_a_protected_manuscript(self):
        def mutate(value):
            replacement = next(item for item in value["files"] if item["path"] == "SPECIFICATION.md")
            for index, item in enumerate(value["files"]):
                if item["path"] == "paper/manuscript.md":
                    value["files"][index] = copy.deepcopy(replacement)
                    break
            else:
                self.fail("expected protected manuscript entry is absent")

        self.reject_json_change("preservation.json", mutate)

    def test_preservation_baseline_is_pinned(self):
        self.reject_json_change("preservation.json",
                                lambda value: value.update(baseline_commit="0" * 40))

    def test_manifest_bytes_are_pinned(self):
        original = packet_guard.digest

        def digest(path):
            return "0" * 64 if path == packet_guard.BASE / "preservation.json" else original(path)

        with patch.object(packet_guard, "digest", side_effect=digest):
            with self.assertRaisesRegex(ValueError, "approved preservation manifest changed"):
                packet_guard.evaluate()

    def test_source_review_and_authority_cannot_be_promoted(self):
        mutations = [
            (["personal_source_review"], "complete"),
            (["independent_human_review"], True),
            (["assessment_conformant"], True),
            (["manuscript_revision_authorized"], True),
            (["publication_authorized"], True),
            (["scientific_conclusion_eligible"], True),
            (["release_gate_satisfied"], True),
            (["status"], "fully_reviewed"),
            (["decisions", 7, "author_receipt", "statement"], "Approved without limits."),
            (["decisions", 6, "accepted_value", "institutional_record_integrity"], "adequate"),
            (["decisions", 0, "alternatives"], []),
            (["source_qualifications", 0, "qualified_proposition"], "Completed plan approved."),
        ]
        for keys, replacement in mutations:
            with self.subTest(field=keys):
                def mutate(value):
                    node = value
                    for key in keys[:-1]:
                        node = node[key]
                    node[keys[-1]] = replacement

                self.reject_json_change("review-status.json", mutate)


if __name__ == "__main__":
    unittest.main()
