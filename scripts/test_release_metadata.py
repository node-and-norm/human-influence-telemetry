"""Negative tests for exact-version metadata, not live publication verification."""

from __future__ import annotations

import copy
import json
import unittest
from unittest.mock import patch
from pathlib import Path

import yaml

from release_metadata import (
    CURRENT_RELEASE, CURRENT_RELEASE_URL, CURRENT_VERSION_DOI, HISTORICAL_VERSION_DOIS,
    ORIGINATING_RESEARCH_DOI, SOFTWARE_CONCEPT_DOI, VERIFIED_RECEIPT_BINDINGS,
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

    def test_current_identity_and_historical_receipt_are_consistent(self) -> None:
        self.assertEqual([], self.errors())
        receipt = json.loads((ROOT / "release/v0.6.6/publication-receipt.json").read_text())
        self.assertEqual([], validate_publication_receipt(receipt, expected_release="0.6.6"))
        for section, key, value in (
            (None, "release", "0.6.5"), (None, "release_commit", None),
            (None, "tag", "v0.6.7"), (None, "tag_moved", True),
            ("zenodo", "version", "0.6.7"),
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
                self.assertTrue(validate_publication_receipt(invalid, expected_release="0.6.6"))

    def test_historical_receipt_remains_bound_when_current_version_changes(self) -> None:
        receipt = json.loads((ROOT / "release/v0.6.6/publication-receipt.json").read_text())
        with patch("release_metadata.CURRENT_RELEASE", "9.9.9"), patch("release_metadata.CURRENT_VERSION_DOI", None):
            self.assertEqual([], validate_publication_receipt(receipt, expected_release="0.6.6"))
        receipt["release_commit"] = "a" * 40
        receipt["github"]["ci_head_sha"] = "a" * 40
        self.assertTrue(validate_publication_receipt(receipt, expected_release="0.6.6"))

    def test_each_published_receipt_is_bound_to_its_own_version(self) -> None:
        for version, binding in VERIFIED_RECEIPT_BINDINGS.items():
            receipt = json.loads((ROOT / f"release/v{version}/publication-receipt.json").read_text())
            with self.subTest(version=version):
                self.assertEqual([], validate_publication_receipt(receipt, expected_release=version))
                self.assertEqual(binding["release_commit"], receipt["release_commit"])
            for other_version, other in VERIFIED_RECEIPT_BINDINGS.items():
                if other_version == version:
                    continue
                with self.subTest(version=version, wrong_binding=other_version):
                    self.assertTrue(validate_publication_receipt(receipt, expected_release=other_version))
                for section, key, value in (
                    (None, "tag", other["tag"]),
                    ("zenodo", "doi", other["doi"]),
                    (None, "release_commit", other["release_commit"]),
                ):
                    with self.subTest(version=version, section=section, key=key):
                        invalid = copy.deepcopy(receipt)
                        (invalid[section] if section else invalid)[key] = value
                        if key == "release_commit":
                            invalid["github"]["ci_head_sha"] = value
                        self.assertTrue(validate_publication_receipt(invalid, expected_release=version))

    def test_unreviewed_release_receipt_rejected(self) -> None:
        receipt = json.loads((ROOT / "release/v0.6.6/publication-receipt.json").read_text())
        receipt["release"] = "9.9.9"
        receipt["zenodo"]["version"] = "9.9.9"
        receipt["zenodo"]["doi"] = "10.5281/zenodo.99999999"
        self.assertTrue(validate_publication_receipt(receipt, expected_release="9.9.9"))

    def test_citation_rejects_other_identifiers_as_exact_doi(self) -> None:
        for value in (*HISTORICAL_VERSION_DOIS.values(),
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

    def test_pending_doi_cannot_claim_verified(self) -> None:
        self.citation.pop("doi", None)
        self.ledger["current_software_doi"] = None
        with patch("release_metadata.CURRENT_VERSION_DOI", None), patch("release_metadata.DOI_STATUS", "verified"):
            self.ledger["current_software_doi_status"] = "verified"
            self.assertTrue(self.errors())

    def test_verified_doi_requires_a_reviewed_matching_binding(self) -> None:
        test_doi = "10.5281/zenodo.99999999"
        self.citation["doi"] = test_doi
        self.ledger["current_software_doi"] = test_doi
        self.ledger["current_software_doi_status"] = "verified"
        with patch("release_metadata.CURRENT_VERSION_DOI", test_doi), patch("release_metadata.DOI_STATUS", "verified"):
            self.assertTrue(self.errors())
            with patch("release_metadata.VERIFIED_RECEIPT_BINDINGS", {CURRENT_RELEASE: {"doi": test_doi}}):
                self.assertEqual([], self.errors())

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
        current_url = CURRENT_RELEASE_URL if CURRENT_VERSION_DOI is None else f"https://doi.org/{CURRENT_VERSION_DOI}"
        changes += [(f"]({current_url})", f"](https://doi.org/{doi})")
                    for doi in (*HISTORICAL_VERSION_DOIS.values(), SOFTWARE_CONCEPT_DOI, ORIGINATING_RESEARCH_DOI)]
        changes.append((f"]({current_url})", "](https://github.com/node-and-norm/human-influence-telemetry/releases/tag/v0.6.6)"))
        for before, after in changes:
            with self.subTest(after=after):
                self.assertTrue(validate_citation_guidance(self.readme.replace(before, after), self.guide))

    def test_other_dois_must_stay_out_of_readme_citation_section(self) -> None:
        for doi in (*HISTORICAL_VERSION_DOIS.values(), SOFTWARE_CONCEPT_DOI, ORIGINATING_RESEARCH_DOI, "10.1234/invented"):
            with self.subTest(doi=doi):
                changed = self.readme.replace("## Citation\n", f"## Citation\n\nPrevious DOI: {doi}\n")
                self.assertTrue(validate_citation_guidance(changed, self.guide))

    def test_missing_guide_and_swapped_mappings_rejected(self) -> None:
        self.assertTrue(validate_citation_guidance(self.readme, ""))
        for version, doi in HISTORICAL_VERSION_DOIS.items():
            with self.subTest(version=version):
                changed = self.guide.replace(f"| {version} | [{doi}]", f"| 0.0.0 | [{doi}]")
                self.assertTrue(validate_citation_guidance(self.readme, changed))
        changed = self.guide.replace("| 0.6.4 |", "| TEMP |").replace("| 0.6.5 |", "| 0.6.4 |").replace("| TEMP |", "| 0.6.5 |")
        self.assertTrue(validate_citation_guidance(self.readme, changed))

    def test_pending_mapping_cannot_reuse_a_verified_historical_doi(self) -> None:
        before = f"| {CURRENT_RELEASE} | Pending verification |"
        readme = (
            "## Citation\n\n"
            f"> Test (Version {CURRENT_RELEASE}) [Software]. GitHub. [v{CURRENT_RELEASE}]({CURRENT_RELEASE_URL})\n\n"
            "[citation guide](docs/citation.md) [CITATION.cff](CITATION.cff)\n"
        )
        guide = "\n".join(line for line in self.guide.splitlines() if not line.startswith(f"| {CURRENT_RELEASE} |"))
        guide += f"\n{before} Test fixture |\n"
        with patch("release_metadata.CURRENT_VERSION_DOI", None):
            self.assertEqual([], validate_citation_guidance(readme, guide))
            for replacement in ("Published", "10.5281/zenodo.23226713", ""):
                with self.subTest(replacement=replacement):
                    after = f"| {CURRENT_RELEASE} | {replacement} |"
                    self.assertTrue(validate_citation_guidance(readme, guide.replace(before, after)))

    def test_readme_requires_exactly_one_citation(self) -> None:
        section = self.readme.partition("## Citation\n")[2].split("\n## ", 1)[0]
        quote = next(line for line in section.splitlines() if line.startswith("> "))
        for replacement in ("", f"{quote}\n{quote}"):
            with self.subTest(replacement=replacement):
                self.assertTrue(validate_citation_guidance(self.readme.replace(quote, replacement), self.guide))

    def test_verified_citation_branch_requires_its_exact_version_doi(self) -> None:
        # This identifier is a test value only; patching does not record publication.
        test_doi = "10.5281/zenodo.99999999"
        doi_url = f"https://doi.org/{test_doi}"
        readme = (
            "## Citation\n\n"
            f"> Test (Version {CURRENT_RELEASE}) [Software]. Zenodo. [{doi_url}]({doi_url})\n\n"
            "[citation guide](docs/citation.md) [CITATION.cff](CITATION.cff)\n"
        )
        guide = "\n".join(line for line in self.guide.splitlines() if not line.startswith(f"| {CURRENT_RELEASE} |"))
        guide += f"\n| {CURRENT_RELEASE} | [{test_doi}]({doi_url}) | Test fixture |\n"
        with patch("release_metadata.CURRENT_VERSION_DOI", test_doi):
            self.assertEqual([], validate_citation_guidance(readme, guide))
            changed = readme.replace(test_doi, HISTORICAL_VERSION_DOIS["0.6.6"])
            self.assertTrue(validate_citation_guidance(changed, guide))

    def test_concept_and_origin_roles_cannot_be_interchanged(self) -> None:
        for label in ("software concept", "originating research"):
            with self.subTest(label=label):
                changed = self.guide.replace(f"The {label} DOI,", "The exact-version DOI,")
                self.assertTrue(validate_citation_guidance(self.readme, changed))
        changed = self.guide.replace(ORIGINATING_RESEARCH_DOI, SOFTWARE_CONCEPT_DOI)
        self.assertTrue(validate_citation_guidance(self.readme, changed))


if __name__ == "__main__":
    unittest.main()
