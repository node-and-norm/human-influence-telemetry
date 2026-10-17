#!/usr/bin/env python3
"""Mutation tests for the closeout record, not a test of scientific conclusions."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import validate_closeout as check


class CloseoutTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="hit-closeout-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        for name in (check.STATUS, check.REGISTER, check.GATES, check.QUEUE, check.PLAN, check.SOURCES, check.AUTHORITY):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((check.ROOT / name).read_bytes())

    def mutate(self, path, change):
        target = self.root / path
        value = check.decoded(target.read_bytes())
        change(value)
        target.write_text(json.dumps(value), encoding="utf-8")

    def rejected_mutations(self, path, changes):
        target = self.root / path
        original = target.read_bytes()
        for number, change in enumerate(changes):
            target.write_bytes(original)
            self.mutate(path, change)
            with self.subTest(mutation=number), self.assertRaises(ValueError):
                check.evaluate(self.root)
        target.write_bytes(original)

    def test_current_plan_is_not_acceptance_or_activation(self):
        result = check.evaluate(self.root)
        self.assertEqual(result["manuscript_claims"], 16)
        self.assertEqual(result["unresolved_stable_gates"], 8)
        for key in ("scientific_acceptance_conferred", "maintenance_activated", "release_authorized"):
            self.assertIs(result[key], False)

    def test_bounded_dispositions_do_not_approve_manuscript_or_activate_phase(self):
        for state in ("awaiting_author_review", "bounded_dispositions_recorded"):
            self.mutate(check.STATUS, lambda d: d["work_items"][1].update(status=state))
            result = check.evaluate(self.root)
            self.assertEqual(result["check_kind"], "closeout_record_consistency_only")
            self.assertEqual(result["bounded_dispositions_recorded"], state == "bounded_dispositions_recorded")
            self.assertEqual(result["manuscript_claims"], 16)
            self.assertEqual(result["unresolved_stable_gates"], 8)
            for key in ("scientific_acceptance_conferred", "maintenance_activated", "release_authorized"):
                self.assertIs(result[key], False)

    def test_bounded_dispositions_require_each_record_once(self):
        self.mutate(check.STATUS, lambda d: d["work_items"][1].update(status="bounded_dispositions_recorded"))
        authority = self.root / check.AUTHORITY
        original = authority.read_text(encoding="utf-8")
        self.assertEqual(check.DISPOSITION_IDS, [f"AD-{n:03d}" for n in range(7, 32)])
        for decision_id in check.DISPOSITION_IDS:
            missing = original.replace(f"## {decision_id}:", "## Removed decision:")
            duplicate = original + f"\n## {decision_id}: Duplicate decision\n"
            for kind, changed in (("missing", missing), ("duplicate", duplicate)):
                authority.write_text(changed, encoding="utf-8")
                with self.subTest(decision=decision_id, mutation=kind), self.assertRaises(ValueError):
                    check.evaluate(self.root)
        authority.write_text(original, encoding="utf-8")

    def test_verification_status_can_advance_without_acceptance(self):
        for value in ("pending_verification", "verified_this_revision"):
            self.mutate(check.STATUS, lambda d: d["work_items"][3].update(status=value))
            self.assertIs(check.evaluate(self.root)["release_authorized"], False)

    def test_wrong_deadline_baseline_and_release_identity_rejected(self):
        changes = {"decision_date": "2026-10-31", "recorded_date": "2026-10-17", "timezone": "UTC",
                   "baseline_commit": "0" * 40, "current_archived_release": "1.0.0",
                   "current_archived_doi": "10.5281/zenodo.23226713"}
        self.rejected_mutations(check.STATUS, [lambda d, k=k, v=v: d.update({k: v}) for k, v in changes.items()])
        with patch.object(check, "CURRENT_RELEASE", "1.0.0"), self.assertRaises(ValueError):
            check.evaluate(self.root)
        with patch.object(check, "CURRENT_VERSION_DOI", "10.5281/zenodo.21446141"), self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_false_promotions_and_boolean_impostors_rejected(self):
        self.rejected_mutations(check.STATUS, [lambda d, k=k, v=v: d.update({k: v})
                                              for k in check.FALSE_FIELDS for v in (True, 0, "false")])

    def test_automatic_phase_transition_and_scope_expansion_rejected(self):
        self.rejected_mutations(check.STATUS, [lambda d: d.update(phase="maintenance"),
                                              lambda d: d.update(scope_frozen=1),
                                              lambda d: d.update(automatic_closeout=True),
                                              lambda d: d.update(transition_rule="The deadline automatically closes this phase."),
                                              lambda d: d["exclusions"].pop()])

    def test_work_item_changes_need_reviewed_controls(self):
        self.rejected_mutations(check.STATUS, [lambda d: d["work_items"].pop(),
                                              lambda d: d["work_items"][0].update(id="CO-02"),
                                              lambda d: d["work_items"][1].update(status="accepted_by_ai"),
                                              lambda d: d["work_items"][1].update(owner="Codex"),
                                              lambda d: d["work_items"][4].update(status="complete"),
                                              lambda d: d["work_items"][4].update(owner="Codex"),
                                              lambda d: d["work_items"][3].update(status="release_ready"),
                                              lambda d: d["work_items"][3].update(release_authorized=True)])

    def test_disposition_status_cannot_replace_author_review_or_owner(self):
        self.rejected_mutations(check.STATUS, [lambda d, state=state: d["work_items"][1].update(status=state)
                                              for state in ("accepted", "complete", "ai_review_complete", "verified_this_revision")])
        self.rejected_mutations(check.STATUS, [lambda d, owner=owner: d["work_items"][1].update(owner=owner)
                                              for owner in ("Codex", "AI assistant", "Maintainer or Codex")])

    def test_replication_prohibition_cannot_be_replaced_by_broad_scoring_flag(self):
        self.rejected_mutations(check.STATUS, [lambda d: d.update(current_contract_scoring_permitted=False),
                                              lambda d: d.pop("current_contract_replication_scoring_permitted")])

    def test_missing_extra_duplicate_and_retargeted_claim_references_rejected(self):
        self.rejected_mutations(check.STATUS, [lambda d: d["manuscript_claim_ids"].pop(),
                                              lambda d: d["manuscript_claim_ids"].append("DEV-C17"),
                                              lambda d: d["manuscript_claim_ids"].__setitem__(0, "DEV-C02"),
                                              lambda d: d.update(manuscript_claim_register=check.GATES)])
        self.rejected_mutations(check.REGISTER, [lambda d: d["claims"].pop(),
                                                lambda d: d["claims"].append(copy.deepcopy(d["claims"][0])),
                                                lambda d: d["claims"][0].update(id="DEV-C17")])

    def test_canonical_author_acceptance_and_inherited_eligibility_rejected(self):
        self.rejected_mutations(check.REGISTER, [lambda d: d.update(status="accepted"),
                                                lambda d: d.update(register_confers_scientific_acceptance=True),
                                                lambda d: d.update(release_gate_satisfied=True),
                                                lambda d: d["historical_audit"].update(eligibility_inherited=True),
                                                lambda d: d["claims"][0].update(author_review="accepted_by_ai"),
                                                lambda d: d["claims"][0].update(author_review="accepted"),
                                                lambda d: d["claims"][0].update(scientific_conclusion_eligible=True),
                                                lambda d: d["claims"][0].update(scientific_conclusion_eligible=0)])

    def test_stable_gate_promotions_and_missing_gates_rejected(self):
        self.rejected_mutations(check.GATES, [lambda d: d.update(status="release_ready"),
                                             lambda d: d["gates"].pop(),
                                             lambda d: d["gates"].append(copy.deepcopy(d["gates"][0])),
                                             lambda d: d["gates"][0].update(status="satisfied"),
                                             lambda d: d["gates"][0].update(gate_id="replacement_gate")])

    def test_worksheet_missing_or_unknown_claim_reference_rejected(self):
        target = self.root / check.QUEUE
        original = target.read_text(encoding="utf-8")
        for changed in (original.replace("DEV-C16", "DEV-C17"), original.replace("DEV-C16", "omitted claim")):
            target.write_text(changed, encoding="utf-8")
            with self.assertRaises(ValueError):
                check.evaluate(self.root)

    def test_missing_reference_and_authority_heading_rejected(self):
        source = self.root / check.SOURCES
        original = source.read_bytes()
        source.unlink()
        with self.assertRaises(ValueError):
            check.evaluate(self.root)
        source.write_bytes(original)
        authority = self.root / check.AUTHORITY
        authority.write_text(authority.read_text(encoding="utf-8").replace("## AD-006:", "## Removed decision:"), encoding="utf-8")
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_unknown_fields_duplicate_json_and_symlink_reference_rejected(self):
        self.rejected_mutations(check.STATUS, [lambda d: d.update(accepted_by_ai=True),
                                              lambda d: d.update(plan="../outside.md")])
        with self.assertRaises(ValueError):
            check.decoded(b'{"phase":"bounded_closeout_in_progress","phase":"maintenance"}')
        plan = self.root / check.PLAN
        plan.unlink()
        plan.symlink_to(self.root / check.QUEUE)
        with self.assertRaises(ValueError):
            check.evaluate(self.root)


if __name__ == "__main__":
    unittest.main()
