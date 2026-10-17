#!/usr/bin/env python3
"""Mutation tests for the closeout record, not a test of scientific conclusions."""
import copy
import json
from pathlib import Path
import subprocess
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
        # A future active repository still exercises the authorization stage first.
        self.mutate(check.STATUS, lambda d: d.update(phase="bounded_closeout_in_progress",
                                                    maintenance_started=False, closeout_accepted=False,
                                                    maintenance_receipt=None))
        self.mutate(check.STATUS, lambda d: d["work_items"][4].update(status="authorized_pending_verification"))

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

    def git(self, *args):
        return subprocess.check_output(["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                                        "-c", "user.name=HIT test fixture", "-c", "user.email=fixture@example.invalid",
                                        *args], cwd=self.root, stderr=subprocess.DEVNULL).decode().strip()

    def activate_fixture(self):
        """Use an isolated real Git graph, never the live worktree's branch state."""
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Fixture baseline")
        self.base_commit = self.git("rev-parse", "HEAD")
        patcher = patch.dict(check.FIXED, {"baseline_commit": self.base_commit})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.git("switch", "--quiet", "-c", "review")
        self.mutate(check.STATUS, lambda d: d.update(baseline_commit=self.base_commit))
        self.git("add", check.STATUS)
        self.git("commit", "--quiet", "-m", "Fixture authorized reviewed head")
        self.head_commit = self.git("rev-parse", "HEAD")
        self.git("switch", "--quiet", "main")
        self.git("commit", "--quiet", "--allow-empty", "-m", "Fixture main advance")
        self.git("merge", "--quiet", "--no-ff", "review", "-m", "Fixture reviewed merge")
        self.merge_commit = self.git("rev-parse", "HEAD")
        revisions = [self.head_commit, self.merge_commit]
        receipt = {
            "receipt_id": "HIT-MAINTENANCE-2026-10-17", "recorded_date": "2026-10-17",
            "authority_record": check.MAINTENANCE_AUTHORITY,
            "scope": "bounded_solo_development_to_maintenance_only",
            "reviewed_pr": {"number": 42, "url": f"{check.REPOSITORY_URL}/pull/42",
                            "head_commit": self.head_commit, "merge_commit": self.merge_commit},
            "local_checks": [{"revision": revision, "uncommitted_changes_included": False,
                              **{key: True for key in check.LOCAL_PASS_FIELDS}} for revision in revisions],
            "hosted_checks": [{"revision": revision, "workflow": "HIT Validation", "event": event,
                               "run_id": number, "url": f"{check.REPOSITORY_URL}/actions/runs/{number}",
                               "status": "completed", "conclusion": "success"}
                              for number, (revision, event) in enumerate(zip(revisions, ("pull_request", "push")), 1)],
            "offline_check_authenticates_execution": False, "offline_check_authenticates_authority": False,
        }
        (self.root / check.RECEIPT).write_text(json.dumps(receipt), encoding="utf-8")
        self.mutate(check.STATUS, lambda d: d.update(phase="maintenance", maintenance_started=True,
                                                    closeout_accepted=True, maintenance_receipt=check.RECEIPT))
        self.mutate(check.STATUS, lambda d: d["work_items"][4].update(status="maintenance_entered"))

    @staticmethod
    def change_revision(receipt, index, revision):
        receipt["reviewed_pr"]["head_commit" if index == 0 else "merge_commit"] = revision
        receipt["local_checks"][index]["revision"] = revision
        receipt["hosted_checks"][index]["revision"] = revision

    def test_current_plan_is_not_acceptance_or_activation(self):
        result = check.evaluate(self.root)
        self.assertEqual(result["manuscript_claims"], 16)
        self.assertEqual(result["unresolved_stable_gates"], 8)
        for key in ("scientific_acceptance_conferred", "maintenance_activated", "release_authorized"):
            self.assertIs(result[key], False)

    def test_bounded_dispositions_do_not_approve_manuscript_or_activate_phase(self):
        result = check.evaluate(self.root)
        self.assertEqual(result["check_kind"], "closeout_record_consistency_only")
        self.assertIs(result["bounded_dispositions_recorded"], True)
        self.assertIs(result["maintenance_recorded"], False)
        for key in ("scientific_acceptance_conferred", "maintenance_activated", "release_authorized"):
            self.assertIs(result[key], False)
        self.rejected_mutations(check.STATUS, [lambda d: d["work_items"][1].update(status="awaiting_author_review")])

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

    def test_conditional_authorization_requires_recorded_local_verification(self):
        self.assertIs(check.evaluate(self.root)["release_authorized"], False)
        self.rejected_mutations(check.STATUS, [lambda d: d["work_items"][3].update(status="pending_verification")])

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
                                              lambda d: d.update(maintenance_started=True),
                                              lambda d: d.update(closeout_accepted=True),
                                              lambda d: d.update(maintenance_receipt=check.RECEIPT),
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
                                              lambda d: d["work_items"][4].update(status="awaiting_author_decision"),
                                              lambda d: d["work_items"][4].update(status="maintenance_entered"),
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

    def test_maintenance_authority_requires_unique_record_and_exact_reference(self):
        self.rejected_mutations(check.STATUS, [lambda d: d.update(maintenance_authority_record=d["authority_record"])])
        authority = self.root / check.AUTHORITY
        original = authority.read_text(encoding="utf-8")
        for value in (original.replace("## AD-032:", "## Removed decision:"),
                      original + "\n## AD-032: Conditional maintenance authorization\n"):
            authority.write_text(value, encoding="utf-8")
            with self.assertRaises(ValueError):
                check.evaluate(self.root)

    def test_active_maintenance_receipt_records_consistency_only(self):
        self.activate_fixture()
        result = check.evaluate(self.root)
        self.assertIs(result["maintenance_recorded"], True)
        self.assertEqual(result["phase"], "maintenance")
        for key in ("scientific_acceptance_conferred", "maintenance_activated", "release_authorized"):
            self.assertIs(result[key], False)

    def test_missing_receipt_and_partial_active_flags_rejected(self):
        self.activate_fixture()
        self.rejected_mutations(check.STATUS, [lambda d: d.update(maintenance_started=False),
                                              lambda d: d.update(closeout_accepted=False),
                                              lambda d: d.update(closeout_accepted=1),
                                              lambda d: d.update(maintenance_receipt=None),
                                              lambda d: d.update(phase="bounded_closeout_in_progress"),
                                              lambda d: d["work_items"][4].update(status="authorized_pending_verification"),
                                              lambda d: d["work_items"][4].update(owner="Codex")])
        (self.root / check.RECEIPT).unlink()
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_pending_state_cannot_retain_receipt(self):
        (self.root / check.RECEIPT).write_text("{}", encoding="utf-8")
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_receipt_requires_both_revision_checks_and_passes(self):
        self.activate_fixture()
        self.rejected_mutations(check.RECEIPT, [lambda d: d["local_checks"].pop(),
                                               lambda d: d["hosted_checks"].pop(),
                                               lambda d: d["local_checks"][0].update(revision=self.merge_commit),
                                               lambda d: d["hosted_checks"][1].update(revision=self.head_commit),
                                               lambda d: d["local_checks"][0].update(uncommitted_changes_included=True),
                                               lambda d: d["hosted_checks"][0].update(status="in_progress"),
                                               lambda d: d["hosted_checks"][1].update(conclusion="failure")])
        self.rejected_mutations(check.RECEIPT, [lambda d, key=key, value=value: d["local_checks"][1].update({key: value})
                                               for key in check.LOCAL_PASS_FIELDS for value in (False, 1, "true")])

    def test_receipt_rejects_wrong_pr_authority_url_run_and_authentication_claims(self):
        self.activate_fixture()
        self.rejected_mutations(check.RECEIPT, [lambda d: d.update(authority_record=check.AUTHORITY),
                                               lambda d: d.update(offline_check_authenticates_execution=True),
                                               lambda d: d.update(offline_check_authenticates_authority=True),
                                               lambda d: d.update(release_authorized=True),
                                               lambda d: d["reviewed_pr"].update(number=43),
                                               lambda d: d["reviewed_pr"].update(url=f"{check.REPOSITORY_URL}/pull/43"),
                                               lambda d: d["hosted_checks"][0].update(url=f"{check.REPOSITORY_URL}/actions/runs/999"),
                                               lambda d: d["hosted_checks"][0].update(run_id=True),
                                               lambda d: d["hosted_checks"][0].update(event="push"),
                                               lambda d: d["hosted_checks"][1].update(run_id=1, url=f"{check.REPOSITORY_URL}/actions/runs/1")])

    def test_receipt_rejects_nonexistent_malformed_and_wrong_revision(self):
        self.activate_fixture()
        self.rejected_mutations(check.RECEIPT, [lambda d: self.change_revision(d, 0, "0" * 40),
                                               lambda d: self.change_revision(d, 0, "HEAD"),
                                               lambda d: self.change_revision(d, 0, self.base_commit),
                                               lambda d: self.change_revision(d, 1, self.head_commit)])

    def test_receipt_rejects_unmerged_or_nonancestral_revision(self):
        self.activate_fixture()
        self.git("update-ref", "HEAD", self.head_commit)
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_receipt_rejects_single_parent_instead_of_reviewed_merge(self):
        self.activate_fixture()
        tree = self.git("rev-parse", f"{self.head_commit}^{{tree}}")
        commit = self.git("commit-tree", tree, "-p", self.head_commit, "-m", "Fixture false merge")
        self.git("update-ref", "HEAD", commit)
        self.mutate(check.RECEIPT, lambda d: self.change_revision(d, 1, commit))
        with self.assertRaises(ValueError):
            check.evaluate(self.root)

    def test_active_state_still_preserves_manuscript_and_gate_records(self):
        self.activate_fixture()
        self.rejected_mutations(check.REGISTER, [lambda d: d["claims"][0].update(scientific_conclusion_eligible=True),
                                                lambda d: d["claims"][0].update(author_review="accepted"),
                                                lambda d: d["claims"][0].update(claim="Changed after reviewed revision")])
        self.rejected_mutations(check.GATES, [lambda d: d["gates"][0].update(status="satisfied"),
                                             lambda d: d["gates"][0].update(limitation="Changed after reviewed revision")])
        self.rejected_mutations(check.STATUS, [lambda d, key=key: d.update({key: True}) for key in check.FALSE_FIELDS])

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
