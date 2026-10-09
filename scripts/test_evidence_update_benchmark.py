#!/usr/bin/env python3
"""Software fixtures test the scorer; they are never observed trial responses."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import run_evidence_update_benchmark as run


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hit-evidence-update-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.originals = {p: run.raw(run.ROOT, p) for p in (*run.FROZEN, f"{run.BASE}/design.json")}
        for path, content in self.originals.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.freeze = "a" * 40
        self.patcher = patch.object(run, "committed", side_effect=self.committed)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def committed(self, root, commit, path):
        if commit != self.freeze:
            raise ValueError("unknown test freeze")
        return self.originals[path]

    def write(self, name, data):
        target = self.root / run.BASE / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(run.encoded(data))

    def refresh_manifest(self):
        data = run.load(self.root, "design.json")
        data["frozen_sha256"] = run.manifest(self.root)
        self.write("design.json", data)

    def response_fixture(self, method):
        """Oracle-derived data are permissible only as labeled unit-test fixtures."""
        oracle = run.load(self.root, "inputs/oracle.json")["scenarios"]
        rows = []
        for expected in oracle:
            claims = []
            for cid in run.CLAIMS:
                statement = "UNIT TEST FIXTURE ONLY; no research observation."
                if expected["id"] == "U02" and cid == "P01":
                    statement += " Direction issued 18 August 2040."
                if expected["id"] == "U04" and cid == "P05":
                    statement += " Recipients A01, A02, A03, A04 and A05 only."
                claims.append({"id": cid, "action": "revise" if cid in expected["affected_claims"] else "retain",
                               "status": expected["claim_states"][cid], "updated_statement": statement,
                               "evidence_refs": [], "rationale": "Unit-test fixture only."})
            rows.append({"id": expected["id"], "claims": claims,
                         "qualifications": [{"id": qid, "state": expected["qualification_states"][qid],
                                             "rationale": "Unit-test fixture only."} for qid in run.QUALS]})
        return {"study_id": run.STUDY, "method_id": method, "protocol_commit": self.freeze,
                "input_sha256": {p: run.sha(run.raw(self.root, p)) for p in run.permitted(method)},
                "executor": "ai_assistant", "independent_review": False, "author_review": "pending",
                "access_declaration": "Unit-test fixture; not an actual execution declaration.", "scenarios": rows}

    def inspect(self, response, method="hit_graph"):
        dossier, updates, oracle = run.prepare(self.root)
        return run.inspect_response(self.root, method, response, dossier, updates), oracle

    def test_preparation_requires_no_trial_and_semantic_equivalence(self):
        run.prepare(self.root)
        self.assertFalse((self.root / run.BASE / "responses").exists())

    def test_unequal_evidence_relationships_rejected_even_after_rehash(self):
        table = run.load(self.root, "inputs/structured_table.json")
        table["review_rows"][0]["evidence_refs"] = ["S02"]
        self.write("inputs/structured_table.json", table)
        self.refresh_manifest()
        with self.assertRaisesRegex(ValueError, "unequal semantic"):
            run.prepare(self.root)

    def test_changed_input_rejected_before_scoring(self):
        self.write("inputs/dossier.json", {"synthetic": False})
        with self.assertRaisesRegex(ValueError, "manifest"):
            run.prepare(self.root)

    def test_postfreeze_change_rejected_even_after_manifest_update(self):
        path = self.root / run.BASE / "PROTOCOL.md"
        path.write_bytes(path.read_bytes() + b"\nChanged after freeze.\n")
        self.refresh_manifest()
        with self.assertRaisesRegex(ValueError, "post-freeze"):
            self.inspect(self.response_fixture("hit_graph"))

    def test_complete_software_fixture_counts_are_separate(self):
        rows, oracle = self.inspect(self.response_fixture("hit_graph"))
        report = run.score(rows, oracle)
        self.assertEqual(report["counts"]["affected_true_positive"], 4)
        self.assertEqual(report["counts"]["unaffected_correctly_retained"], 36)
        self.assertEqual(report["counts"]["claim_state_matches"], 40)
        self.assertEqual(report["counts"]["qualification_state_matches"], 35)
        self.assertEqual(report["counts"]["content_token_matches"], 2)

    def test_wrong_but_valid_states_are_observed_errors_not_dropped(self):
        response = self.response_fixture("hit_graph")
        response["scenarios"][3]["claims"][3]["status"] = "supported"
        response["scenarios"][3]["claims"][3]["action"] = "retain"
        rows, oracle = self.inspect(response)
        result = run.score(rows, oracle)
        self.assertEqual(result["counts"]["affected_missed"], 1)
        self.assertEqual(result["counts"]["claim_state_matches"], 39)

    def test_all_qualification_ids_cannot_mask_wrong_scope_enum(self):
        response = self.response_fixture("hit_graph")
        response["scenarios"][4]["qualifications"][3]["state"] = "all_candidates_received"
        rows, oracle = self.inspect(response)
        self.assertEqual(run.score(rows, oracle)["counts"]["qualification_state_matches"], 34)

    def test_narrow_content_checks_do_not_infer_prose_semantics(self):
        response = self.response_fixture("hit_graph")
        response["scenarios"][2]["claims"][0]["updated_statement"] = "The date changed."
        response["scenarios"][4]["claims"][4]["updated_statement"] = "Some recipients received records."
        rows, oracle = self.inspect(response)
        self.assertEqual(run.score(rows, oracle)["counts"]["content_token_matches"], 0)

    def test_control_records_false_positive(self):
        response = self.response_fixture("hit_graph")
        response["scenarios"][0]["claims"][0]["action"] = "revise"
        rows, oracle = self.inspect(response)
        self.assertEqual(run.score(rows, oracle)["counts"]["unaffected_false_positive"], 1)

    def test_incomplete_duplicate_unknown_and_promoted_records_fail(self):
        mutations = [
            lambda r: r["scenarios"].pop(),
            lambda r: r["scenarios"][0]["claims"].pop(),
            lambda r: r["scenarios"][0]["claims"][0].update(id="P02"),
            lambda r: r["scenarios"][0]["claims"][0].update(evidence_refs=["S06"]),
            lambda r: r["scenarios"][0]["claims"][0].update(score=2),
            lambda r: r["scenarios"][0]["qualifications"][0].update(state="unknown"),
            lambda r: r.update(independent_review=True),
            lambda r: r.update(independent_review=0),
            lambda r: r.update(author_review="accepted"),
            lambda r: r.update(access_declaration=" "),
            lambda r: r.update(input_sha256={}),
            lambda r: r.update(protocol_commit="bad"),
        ]
        for mutation in mutations:
            response = self.response_fixture("hit_graph")
            mutation(response)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.inspect(response)

    def test_duplicate_json_keys_nonfinite_and_symlink_fail(self):
        for value in (b'{"x": 1, "x": 2}', b'{"x": NaN}'):
            with self.assertRaises(ValueError):
                run.decoded(value)
        link = self.root / "linked-input"
        link.symlink_to(self.root / run.BASE / "PROTOCOL.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            run.raw(self.root, "linked-input")

    def test_analysis_requires_two_actual_files_and_never_creates_them(self):
        with self.assertRaisesRegex(ValueError, "missing input"):
            run.analyze(self.root)
        self.assertFalse((self.root / run.BASE / "responses").exists())

    def test_analysis_preserves_limits_and_response_hashes(self):
        for method in run.METHODS:
            self.write(f"responses/{method}.json", self.response_fixture(method))
        report = run.analyze(self.root)
        for key in ("independent_review", "semantic_prose_validated", "historical_truth_validated",
                    "comparative_utility_established", "release_gate_satisfied", "scientific_conclusion_eligible"):
            self.assertIs(report[key], False)
        self.assertEqual(report["status"], "completed_pending_author_review")
        self.assertEqual(len(report["response_sha256"]), 2)


if __name__ == "__main__":
    unittest.main()
