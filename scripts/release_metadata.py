"""Version-bound metadata checks, not evidence that an external archive exists."""

from __future__ import annotations

import re

CURRENT_RELEASE = "0.6.7"
CURRENT_RELEASE_DATE = "2026-10-08"
CURRENT_RELEASE_TITLE = "Author review, evidence-update rehearsal and manuscript exhibits"
CURRENT_RELEASE_URL = f"https://github.com/node-and-norm/human-influence-telemetry/releases/tag/v{CURRENT_RELEASE}"
CURRENT_VERSION_DOI = "10.5281/zenodo.23252877"
DOI_STATUS = "verified"
SOFTWARE_CONCEPT_DOI = "10.5281/zenodo.21446141"
ORIGINATING_RESEARCH_DOI = "10.5281/zenodo.21204892"
HISTORICAL_VERSION_DOIS = {
    "0.6.4": "10.5281/zenodo.21446142",
    "0.6.5": "10.5281/zenodo.21864224",
    "0.6.6": "10.5281/zenodo.23226713",
}

# These bindings record reviewed publication observations. A new repository
# version cannot retarget a historical receipt through the current constants.
VERIFIED_RECEIPT_BINDINGS = {
    "0.6.6": {
        "doi": "10.5281/zenodo.23226713",
        "tag": "v0.6.6",
        "release_commit": "6745873a990554cf40303e217865895122494696",
    },
    "0.6.7": {
        "doi": "10.5281/zenodo.23252877",
        "tag": "v0.6.7",
        "release_commit": "4336b8acd16d571ef9b5ab1d8ca1ecc2ea0eb01e",
    },
}


def validate_citation_guidance(readme: str, guide: str) -> list[str]:
    """Check citation navigation and DOI mappings, not external publication."""
    failures = []
    section = readme.partition("## Citation\n")[2].split("\n## ", 1)[0]
    for link in ("[citation guide](docs/citation.md)", "[CITATION.cff](CITATION.cff)"):
        if link not in section:
            failures.append(f"README citation section must retain {link}")
    if CURRENT_VERSION_DOI is None:
        citation_suffix = f"(Version {CURRENT_RELEASE}) [Software]. GitHub. [v{CURRENT_RELEASE}]({CURRENT_RELEASE_URL})"
        allowed_dois = set()
        current_mapping = f"| {CURRENT_RELEASE} | Pending verification |"
    else:
        doi_url = f"https://doi.org/{CURRENT_VERSION_DOI}"
        citation_suffix = f"(Version {CURRENT_RELEASE}) [Software]. Zenodo. [{doi_url}]({doi_url})"
        allowed_dois = {CURRENT_VERSION_DOI}
        current_mapping = f"| {CURRENT_RELEASE} | [{CURRENT_VERSION_DOI}]({doi_url}) |"
    quotes = [line for line in section.splitlines() if line.startswith("> ")]
    if len(quotes) != 1 or citation_suffix not in quotes[0]:
        failures.append("README must provide one current-version citation with its verified DOI or pending-archive GitHub tag")
    if set(re.findall(r"10\.\d{4,9}/[^\s<>()\]`]+", section)) != allowed_dois:
        failures.append("README citation section must direct other DOI choices to the guide")
    if current_mapping not in guide:
        failures.append(f"citation guide current-version mapping missing or incorrect: {CURRENT_RELEASE}")
    for version, doi in HISTORICAL_VERSION_DOIS.items():
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
    if DOI_STATUS != ("pending_verification" if CURRENT_VERSION_DOI is None else "verified"):
        failures.append("current DOI and verification-status constants are inconsistent")
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
    if CURRENT_VERSION_DOI is not None and VERIFIED_RECEIPT_BINDINGS.get(CURRENT_RELEASE, {}).get("doi") != CURRENT_VERSION_DOI:
        failures.append("current DOI requires a matching reviewed publication receipt binding")
    citation_dois = {item.get("value") for item in citation.get("identifiers", []) if item.get("type") == "doi"}
    if citation_dois != {SOFTWARE_CONCEPT_DOI}:
        failures.append("citation additional DOI must remain the software concept DOI")
    origin = {"identifier": ORIGINATING_RESEARCH_DOI, "relation": "isSupplementTo", "resource_type": "dataset"}
    if origin not in zenodo.get("related_identifiers", []):
        failures.append("originating research relationship must remain separate")
    return failures


def validate_publication_receipt(receipt: dict, *, expected_release: str) -> list[str]:
    """Check internal consistency of recorded observations, not live publication."""
    archive, github = receipt.get("zenodo", {}), receipt.get("github", {})
    failures = []
    binding = VERIFIED_RECEIPT_BINDINGS.get(expected_release)
    if binding is None:
        return [f"publication receipt has no reviewed version binding: {expected_release}"]
    if receipt.get("release") != expected_release or archive.get("version") != expected_release:
        failures.append("publication receipt release version mismatch")
    if archive.get("doi") != binding["doi"] or archive.get("software_concept_doi") != SOFTWARE_CONCEPT_DOI:
        failures.append("publication receipt DOI identity mismatch")
    if receipt.get("tag") != binding["tag"] or receipt.get("tag_moved") is not False:
        failures.append("publication receipt must preserve its verified tag")
    if archive.get("all_tracked_file_bytes_match") is not True or any(archive.get(key) != [] for key in ("missing_files", "extra_files", "byte_mismatches")):
        failures.append("publication receipt does not retain an exact archive comparison")
    count = archive.get("archive_files")
    if type(count) is not int or count <= 0 or archive.get("git_tracked_blobs") != count:
        failures.append("publication receipt archive counts are inconsistent")
    commit = receipt.get("release_commit")
    if commit != binding["release_commit"]:
        failures.append("publication receipt must preserve its verified release commit")
    if not isinstance(commit, str) or len(commit) != 40 or any(char not in "0123456789abcdef" for char in commit):
        failures.append("publication receipt requires an exact Git commit")
    if github.get("ci_head_sha") != commit or github.get("ci_conclusion") != "success":
        failures.append("publication receipt CI must pass on the release commit")
    if github.get("draft") is not False or github.get("remote_tag_commit_verified") is not True:
        failures.append("publication receipt must distinguish published and verified from draft")
    return failures
