"""Version-bound metadata checks, not evidence that an external archive exists."""

from __future__ import annotations

import re

CURRENT_RELEASE = "0.6.6"
CURRENT_RELEASE_DATE = "2026-10-07"
CURRENT_VERSION_DOI = "10.5281/zenodo.23226713"
DOI_STATUS = "verified"
SOFTWARE_CONCEPT_DOI = "10.5281/zenodo.21446141"
ORIGINATING_RESEARCH_DOI = "10.5281/zenodo.21204892"
HISTORICAL_VERSION_DOIS = {
    "0.6.4": "10.5281/zenodo.21446142",
    "0.6.5": "10.5281/zenodo.21864224",
}


def validate_citation_guidance(readme: str, guide: str) -> list[str]:
    """Check citation navigation and DOI mappings, not external publication."""
    failures = []
    section = readme.partition("## Citation\n")[2].split("\n## ", 1)[0]
    for link in ("[citation guide](docs/citation.md)", "[CITATION.cff](CITATION.cff)"):
        if link not in section:
            failures.append(f"README citation section must retain {link}")
    doi_url = f"https://doi.org/{CURRENT_VERSION_DOI}"
    citation_suffix = f"(Version {CURRENT_RELEASE}) [Software]. Zenodo. [{doi_url}]({doi_url})"
    quotes = [line for line in section.splitlines() if line.startswith("> ")]
    if len(quotes) != 1 or citation_suffix not in quotes[0]:
        failures.append("README must provide one current-version citation with its exact DOI link")
    if set(re.findall(r"10\.5281/zenodo\.\d+", section)) != {CURRENT_VERSION_DOI}:
        failures.append("README citation section must direct other DOI choices to the guide")
    for version, doi in {CURRENT_RELEASE: CURRENT_VERSION_DOI, **HISTORICAL_VERSION_DOIS}.items():
        if f"| {version} | [{doi}](https://doi.org/{doi}) |" not in guide:
            failures.append(f"citation guide exact-version mapping missing or incorrect: {version}")
    for label, doi in (("software concept", SOFTWARE_CONCEPT_DOI), ("originating research", ORIGINATING_RESEARCH_DOI)):
        if f"The {label} DOI, [{doi}](https://doi.org/{doi})," not in guide:
            failures.append(f"citation guide {label} DOI missing or incorrect")
    return failures


def validate_identity(citation: dict, zenodo: dict, ledger: dict) -> list[str]:
    """Reject stale or invented identifiers, including an old DOI on a new version.

    A verified DOI requires a reviewed code/metadata update after observation of
    the public record. Passing this function never performs that observation.
    """
    failures = []
    if citation.get("version") != CURRENT_RELEASE or citation.get("date-released") != CURRENT_RELEASE_DATE:
        failures.append("citation release identity or date mismatch")
    if zenodo.get("version") != CURRENT_RELEASE or zenodo.get("publication_date") != CURRENT_RELEASE_DATE:
        failures.append("Zenodo release identity or date mismatch")
    if zenodo.get("upload_type") != "software":
        failures.append("Zenodo upload must remain software")
    # Automatic ingestion must mint a new version rather than reuse any DOI.
    if "doi" in zenodo:
        failures.append("Zenodo ingestion metadata must not supply an existing DOI")
    if CURRENT_VERSION_DOI is None:
        if "doi" in citation:
            failures.append("pending archive must omit the top-level citation DOI")
    elif citation.get("doi") != CURRENT_VERSION_DOI:
        failures.append("citation exact-version DOI mismatch")
    if ledger.get("current_repository_release") != CURRENT_RELEASE:
        failures.append("candidate ledger release baseline mismatch")
    if "current_software_doi" not in ledger or ledger["current_software_doi"] != CURRENT_VERSION_DOI:
        failures.append("candidate ledger exact-version DOI mismatch")
    if ledger.get("current_software_doi_status") != DOI_STATUS:
        failures.append("candidate ledger DOI verification status mismatch")
    if CURRENT_VERSION_DOI in {*HISTORICAL_VERSION_DOIS.values(), SOFTWARE_CONCEPT_DOI, ORIGINATING_RESEARCH_DOI}:
        failures.append("current version cannot reuse a historical, concept or research DOI")
    citation_dois = {item.get("value") for item in citation.get("identifiers", []) if item.get("type") == "doi"}
    if citation_dois != {SOFTWARE_CONCEPT_DOI}:
        failures.append("citation additional DOI must remain the software concept DOI")
    origin = {"identifier": ORIGINATING_RESEARCH_DOI, "relation": "isSupplementTo", "resource_type": "dataset"}
    if origin not in zenodo.get("related_identifiers", []):
        failures.append("originating research relationship must remain separate")
    return failures


def validate_publication_receipt(receipt: dict) -> list[str]:
    """Check internal consistency of recorded observations, not live publication."""
    archive, github = receipt.get("zenodo", {}), receipt.get("github", {})
    failures = []
    if receipt.get("release") != CURRENT_RELEASE or archive.get("version") != CURRENT_RELEASE:
        failures.append("publication receipt release version mismatch")
    if archive.get("doi") != CURRENT_VERSION_DOI or archive.get("software_concept_doi") != SOFTWARE_CONCEPT_DOI:
        failures.append("publication receipt DOI identity mismatch")
    if archive.get("all_tracked_file_bytes_match") is not True or any(archive.get(key) != [] for key in ("missing_files", "extra_files", "byte_mismatches")):
        failures.append("publication receipt does not retain an exact archive comparison")
    count = archive.get("archive_files")
    if type(count) is not int or count <= 0 or archive.get("git_tracked_blobs") != count:
        failures.append("publication receipt archive counts are inconsistent")
    commit = receipt.get("release_commit")
    if not isinstance(commit, str) or len(commit) != 40 or any(char not in "0123456789abcdef" for char in commit):
        failures.append("publication receipt requires an exact Git commit")
    if github.get("ci_head_sha") != commit or github.get("ci_conclusion") != "success":
        failures.append("publication receipt CI must pass on the release commit")
    if github.get("draft") is not False or github.get("remote_tag_commit_verified") is not True:
        failures.append("publication receipt must distinguish published and verified from draft")
    return failures
