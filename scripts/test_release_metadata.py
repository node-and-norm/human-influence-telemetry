"""Negative tests for exact-version metadata, not live publication verification."""

from __future__ import annotations

import copy
import json
import unittest
from unittest.mock import patch
from pathlib import Path

import yaml

from release_metadata import validate_identity, validate_publication_receipt

ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.citation = yaml.safe_load((ROOT / "CITATION.cff").read_text())
        self.zenodo = json.loads((ROOT / ".zenodo.json").read_text())
        self.ledger = json.loads((ROOT / "release/v1.0.0/contract-freeze.candidate.json").read_text())

    def errors(self) -> list[str]:
        return validate_identity(self.citation, self.zenodo, self.ledger)

    def test_current_identity_and_receipt_are_consistent(self) -> None:
        self.assertEqual([], self.errors())
        receipt = json.loads((ROOT / "release/v0.6.6/publication-receipt.json").read_text())
        self.assertEqual([], validate_publication_receipt(receipt))
        for section, key, value in (
            (None, "release", "0.6.5"), (None, "release_commit", None),
            ("zenodo", "doi", "10.5281/zenodo.21864224"),
            ("zenodo", "all_tracked_file_bytes_match", False),
            ("zenodo", "extra_files", ["untracked.txt"]),
            ("zenodo", "missing_files", None),
            ("zenodo", "archive_files", 0),
            ("zenodo", "git_tracked_blobs", 1),
            ("github", "ci_head_sha", None),
            ("github", "ci_conclusion", "failure"),
            ("github", "draft", True),
            ("github", "remote_tag_commit_verified", False),
        ):
            with self.subTest(section=section, key=key):
                invalid = copy.deepcopy(receipt)
                (invalid[section] if section else invalid)[key] = value
                self.assertTrue(validate_publication_receipt(invalid))

    def test_citation_rejects_other_identifiers_as_exact_doi(self) -> None:
        for value in ("10.5281/zenodo.21864224", "10.5281/zenodo.21446142",
                      "10.5281/zenodo.21446141", "10.5281/zenodo.21204892",
                      "10.5281/zenodo.99999999", "pending", 123, []):
            with self.subTest(value=value):
                self.citation["doi"] = value
                self.assertTrue(self.errors())

    def test_pending_citation_requires_absent_field_not_null(self) -> None:
        self.citation.pop("doi", None)
        self.ledger["current_software_doi"] = None
        self.ledger["current_software_doi_status"] = "pending_verification"
        with patch("release_metadata.CURRENT_VERSION_DOI", None), patch("release_metadata.DOI_STATUS", "pending_verification"):
            self.assertEqual([], self.errors())
            self.citation["doi"] = None
            self.assertTrue(self.errors())

    def test_zenodo_must_not_reuse_exact_doi(self) -> None:
        for value in (None, "10.5281/zenodo.21864224", "10.5281/zenodo.99999999"):
            with self.subTest(value=value):
                self.zenodo["doi"] = value
                self.assertTrue(self.errors())

    def test_missing_ledger_doi_is_not_explicit_pending(self) -> None:
        del self.ledger["current_software_doi"]
        self.assertTrue(self.errors())

    def test_wrong_ledger_doi_rejected(self) -> None:
        self.ledger["current_software_doi"] = "10.5281/zenodo.21864224"
        self.assertTrue(self.errors())

    def test_unsupported_archive_confirmation_rejected(self) -> None:
        self.ledger["current_software_doi_status"] = "published"
        self.assertTrue(self.errors())

    def test_missing_archive_status_rejected(self) -> None:
        del self.ledger["current_software_doi_status"]
        self.assertTrue(self.errors())

    def test_stale_citation_version_rejected(self) -> None:
        self.citation["version"] = "0.6.5"
        self.assertTrue(self.errors())

    def test_stale_citation_date_rejected(self) -> None:
        self.citation["date-released"] = "2026-08-09"
        self.assertTrue(self.errors())

    def test_stale_zenodo_identity_rejected(self) -> None:
        original = copy.deepcopy(self.zenodo)
        for key, value in (("version", "0.6.5"), ("publication_date", "2026-08-09"), ("upload_type", "dataset")):
            with self.subTest(key=key):
                self.zenodo = copy.deepcopy(original)
                self.zenodo[key] = value
                self.assertTrue(self.errors())

    def test_stale_candidate_baseline_rejected(self) -> None:
        self.ledger["current_repository_release"] = "0.6.5"
        self.assertTrue(self.errors())

    def test_software_concept_must_not_be_replaced_with_research(self) -> None:
        self.citation["identifiers"] = [{"type": "doi", "value": "10.5281/zenodo.21204892"}]
        self.assertTrue(self.errors())

    def test_origin_relationship_must_be_preserved(self) -> None:
        self.zenodo["related_identifiers"] = []
        self.assertTrue(self.errors())


if __name__ == "__main__":
    unittest.main()
