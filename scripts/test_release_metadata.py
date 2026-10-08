"""Negative tests for exact-version metadata, not live publication verification."""

from __future__ import annotations

import copy
import json
import unittest
from unittest.mock import patch
from pathlib import Path

import yaml

from release_metadata import (
    CURRENT_RELEASE, CURRENT_VERSION_DOI, HISTORICAL_VERSION_DOIS,
    ORIGINATING_RESEARCH_DOI, SOFTWARE_CONCEPT_DOI,
    validate_citation_guidance, validate_identity, validate_publication_receipt,
)

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


class CitationGuidanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.readme = (ROOT / "README.md").read_text()
        self.guide = (ROOT / "docs/citation.md").read_text()

    def test_current_navigation_and_version_mappings(self) -> None:
        self.assertEqual([], validate_citation_guidance(self.readme, self.guide))

    def test_missing_or_wrong_navigation_links_rejected(self) -> None:
        for target in ("docs/citation.md", "CITATION.cff"):
            with self.subTest(target=target):
                changed = self.readme.replace(f"]({target})", "](missing-file.md)")
                self.assertTrue(validate_citation_guidance(changed, self.guide))

    def test_wrong_current_citation_version_or_doi_rejected(self) -> None:
        changes = [(f"(Version {CURRENT_RELEASE})", "(Version 0.6.5)")]
        changes += [(f"](https://doi.org/{CURRENT_VERSION_DOI})", f"](https://doi.org/{doi})")
                    for doi in (*HISTORICAL_VERSION_DOIS.values(), SOFTWARE_CONCEPT_DOI, ORIGINATING_RESEARCH_DOI)]
        for before, after in changes:
            with self.subTest(after=after):
                self.assertTrue(validate_citation_guidance(self.readme.replace(before, after), self.guide))

    def test_other_dois_must_stay_out_of_readme_citation_section(self) -> None:
        for doi in (*HISTORICAL_VERSION_DOIS.values(), SOFTWARE_CONCEPT_DOI, ORIGINATING_RESEARCH_DOI):
            with self.subTest(doi=doi):
                changed = self.readme.replace("## Citation\n", f"## Citation\n\nPrevious DOI: {doi}\n")
                self.assertTrue(validate_citation_guidance(changed, self.guide))

    def test_missing_guide_and_swapped_mappings_rejected(self) -> None:
        self.assertTrue(validate_citation_guidance(self.readme, ""))
        for version, doi in {CURRENT_RELEASE: CURRENT_VERSION_DOI, **HISTORICAL_VERSION_DOIS}.items():
            with self.subTest(version=version):
                changed = self.guide.replace(f"| {version} | [{doi}]", f"| 0.0.0 | [{doi}]")
                self.assertTrue(validate_citation_guidance(self.readme, changed))
        changed = self.guide.replace("| 0.6.4 |", "| TEMP |").replace("| 0.6.5 |", "| 0.6.4 |").replace("| TEMP |", "| 0.6.5 |")
        self.assertTrue(validate_citation_guidance(self.readme, changed))

    def test_concept_and_origin_roles_cannot_be_interchanged(self) -> None:
        for label in ("software concept", "originating research"):
            with self.subTest(label=label):
                changed = self.guide.replace(f"The {label} DOI,", "The exact-version DOI,")
                self.assertTrue(validate_citation_guidance(self.readme, changed))
        changed = self.guide.replace(ORIGINATING_RESEARCH_DOI, SOFTWARE_CONCEPT_DOI)
        self.assertTrue(validate_citation_guidance(self.readme, changed))


if __name__ == "__main__":
    unittest.main()
