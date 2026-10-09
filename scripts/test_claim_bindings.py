#!/usr/bin/env python3
"""Offline file/dependency controls, not checks of human judgment or source truth."""
import copy
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import validate_claim_bindings as check


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hit-claim-binding-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        manifest = check.decoded((check.ROOT / check.BINDINGS).read_bytes())
        self.paths = {check.MAP, check.BINDINGS, *(f["path"] for f in manifest["files"])}
        self.originals = {path: (check.ROOT / path).read_bytes() for path in self.paths}
        self.untracked = set()
        for path, raw in self.originals.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        def git(_, *args):
            if args[0] == "show":
                commit, path = args[1].split(":", 1)
                if commit == check.BASE_COMMIT and path in self.originals:
                    return self.originals[path]
            elif args[0] == "ls-files" and args[-1] not in self.untracked:
                return f"100644 {'0' * 40} 0\t{args[-1]}\n".encode()
            raise subprocess.CalledProcessError(128, "mock git read")
        patcher = patch.object(check, "git", git)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.data = check.decoded(self.originals[check.MAP])

    def test_valid_fixture_claims_only_file_and_dependency_consistency(self):
        result = check.evaluate(self.root)
        self.assertEqual(result["claim_count"], 13)
        self.assertEqual(result["evidence_binding_count"], 19)
        self.assertEqual(result["check_kind"], "file_and_dependency_consistency_only")
        for field in ("human_support_review_validated", "evidence_fitness_validated", "source_truth_validated", "conclusion_eligibility_recomputed"):
            self.assertFalse(result[field])

    def test_cycles_are_checked_directly_before_map_hash(self):
        self.data["claims"][0]["dependencies"] = ["H2"]
        with self.assertRaisesRegex(ValueError, "dependency cycle"):
            check.inspect_map(self.data)
        (self.root / check.MAP).write_bytes(check.encoded(self.data))
        with self.assertRaisesRegex(ValueError, "dependency cycle"):
            check.evaluate(self.root)

    def test_self_loop_unknown_dependency_and_duplicate_ids(self):
        mutations = [lambda d: d["claims"][0].update(dependencies=["H1"]),
                     lambda d: d["claims"][0].update(dependencies=["UNKNOWN"]),
                     lambda d: d["claims"][1].update(dependencies=["H1", "H1"]),
                     lambda d: d["claims"].append(d["claims"][0]),
                     lambda d: d["claims"][1]["evidence"][0].update(evidence_id="H1-SCHEMA")]
        for mutation in mutations:
            data = copy.deepcopy(self.data)
            mutation(data)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                check.inspect_map(data)

    def test_untracked_file_cannot_pass_a_git_tracked_declaration(self):
        self.untracked.add("schema/hit-assessment.schema.json")
        with self.assertRaises(subprocess.CalledProcessError):
            check.evaluate(self.root)

    def test_changed_evidence_cannot_pass_an_updated_manifest_hash(self):
        path = "schema/hit-assessment.schema.json"
        changed = self.originals[path] + b"\n"
        (self.root / path).write_bytes(changed)
        manifest = check.decoded(self.originals[check.BINDINGS])
        next(item for item in manifest["files"] if item["path"] == path)["sha256"] = check.sha(changed)
        (self.root / check.BINDINGS).write_bytes(check.encoded(manifest))
        with self.assertRaisesRegex(ValueError, "frozen base"):
            check.evaluate(self.root)

    def test_missing_mandatory_binding_rejected(self):
        manifest = check.decoded(self.originals[check.BINDINGS])
        manifest["files"].pop()
        (self.root / check.BINDINGS).write_bytes(check.encoded(manifest))
        with self.assertRaisesRegex(ValueError, "mandatory bindings"):
            check.evaluate(self.root)

    def test_paths_cannot_escape_or_use_symlinks(self):
        for path in ("../outside", "/absolute", "schema/../schema/hit-assessment.schema.json", "schema\\file", "schema//file"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                check.safe_path(self.root, path)
        target = self.root / "schema/hit-assessment.schema.json"
        target.unlink()
        target.symlink_to(self.root / check.COMPARISON)
        with self.assertRaisesRegex(ValueError, "symlink"):
            check.evaluate(self.root)

    def test_locked_digest_and_both_preservation_records_are_checked(self):
        raw = self.originals[check.COMPARISON]
        preservation = check.decoded(self.originals[check.PRESERVATION])
        execution = check.decoded(self.originals[check.EXECUTION])
        with self.assertRaisesRegex(ValueError, "locked comparison digest"):
            check.check_locked(raw + b"\n", preservation, execution)
        altered = copy.deepcopy(preservation)
        next(item for item in altered["files"] if item["role"] == "comparison/json")["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "preservation record"):
            check.check_locked(raw, altered, execution)
        execution["outputs"]["json_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "execution record"):
            check.check_locked(raw, preservation, execution)

    def test_missing_evidence_file_and_duplicate_json_rejected(self):
        (self.root / check.COMPARISON).unlink()
        with self.assertRaisesRegex(ValueError, "missing evidence"):
            check.evaluate(self.root)
        with self.assertRaisesRegex(ValueError, "duplicate JSON"):
            check.decoded(b'{"claims": [], "claims": []}')

    def test_prepare_does_not_overwrite_existing_bindings(self):
        with self.assertRaisesRegex(ValueError, "already exist"):
            check.evaluate(self.root, prepare=True)


if __name__ == "__main__":
    unittest.main()
