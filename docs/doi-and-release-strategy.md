# DOI and Release Strategy

## Decision

Human Influence Telemetry uses a separate Zenodo software record for successfully archived releases.

DOI `10.5281/zenodo.21204892` identifies the originating research concept. It is not a version DOI for this standalone software repository.

The standalone HIT software record now exists. Zenodo assigned software concept DOI `10.5281/zenodo.21446141`, version DOI `10.5281/zenodo.21446142` to `v0.6.4`, version DOI `10.5281/zenodo.21864224` to `v0.6.5`, and version DOI `10.5281/zenodo.23226713` to `v0.6.6`.

Version `0.6.6` is published on GitHub and Zenodo. The [publication receipt](../release/v0.6.6/publication-receipt.json) records its exact commit, successful CI, public archival metadata and byte-for-byte archive comparison. Updated metadata and an active repository integration alone do not prove archival publication.

## Identifier model

1. **Originating research DOI**
   - `10.5281/zenodo.21204892`
   - Identifies the originating concept and research lineage.

2. **HIT software concept DOI**
   - `10.5281/zenodo.21446141`
   - Identifies the collection of archived HIT releases.

3. **HIT version DOI**
   - Current exact release: `10.5281/zenodo.23226713` for `v0.6.6`.
   - Previous verified archive: `10.5281/zenodo.21864224` for `v0.6.5`.
   - Previous exact release: `10.5281/zenodo.21446142` for `v0.6.4`.
   - Identifies the exact released files and metadata.

A GitHub tag or release does not by itself prove that a software DOI exists.

## Relationship metadata

The software record should reference the originating research DOI as `isSupplementTo`. The public software operationalizes and supplements the research concept without replacing it.

After Zenodo assigns a new version identifier:

- add the verified exact version DOI to `CITATION.cff` in a controlled follow-up pull request, retaining the software concept DOI;
- retain the originating DOI as a clearly described related identifier;
- add a DOI badge only after the public record resolves;
- update release documentation and the changelog;
- do not move or rewrite an immutable Git tag merely to insert a DOI.

## Release sequence

1. Prepare synchronized repository, component, citation, and Zenodo metadata, explicitly identifying publication and archival status.
2. Run validation on the exact release candidate.
3. Merge the release pull request.
4. Create the Git tag and GitHub release from the exact merged commit.
5. Confirm the Zenodo repository integration state.
6. Observe the processing record for the release event.
7. Verify the new record's version, archive and concept association (`21446141`), together with its exact version DOI and metadata.
8. Record assigned identifiers in a controlled follow-up pull request.

A missing software DOI does not invalidate the GitHub release. It means archival identity remains incomplete and must be reported accurately.

While archival verification is pending, omit the top-level DOI from `CITATION.cff`; retain the concept DOI as an explicitly cross-version identifier. The release ledger uses `current_software_doi: null` and `current_software_doi_status: pending_verification`. Never copy the 0.6.5 DOI into a 0.6.6 exact-version field. A publication-status follow-up records the GitHub release even when Zenodo remains pending, and a later archival follow-up records the verified new DOI. Neither follow-up moves the original tag.

For `0.6.6`, archival verification is complete. The follow-up metadata sets `current_software_doi` to `10.5281/zenodo.23226713` and `current_software_doi_status` to `verified`. The tag retains its original preparation metadata, and the later publication receipt is outside that archive.

## Historical 0.4.0 handling

Release `0.4.0` was the first planned archival opportunity. Repository, specification, assessment schema, and dimension catalog then identified version `0.4.0`.

That release remained at Maturity Level 1. A software DOI would have identified an archived software artifact without establishing human reliability, validation, certification, legal compliance, or institutional adoption.

When the GitHub integration does not produce a record, a manual Zenodo software upload may be used after checking for duplicate-record risk. The uploaded archive must correspond exactly to the tagged release, and the resulting DOI must be added only in a later repository update.

## Metadata precedence

The repository contains both `CITATION.cff` and `.zenodo.json`. When `.zenodo.json` is present, it controls Zenodo ingestion metadata. The two files must remain semantically consistent.

Current component versions:

- repository release: 0.6.6, published on GitHub and Zenodo;
- specification: 0.4.0;
- assessment schema: 0.4.0;
- dimension catalog: 0.4.0;
- conformance engine: 0.5.0;
- human-result release: 0.6.0;
- research maturity: Level 2, Applicable.

## Non-claims

A DOI establishes persistence, citation, and archival identity. It does not establish peer review, empirical validity, certification, legal compliance, institutional adoption, or correctness of assessments.
