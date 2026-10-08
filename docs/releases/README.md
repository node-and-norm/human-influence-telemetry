# Human Influence Telemetry Release Index

This directory records published releases and prospective release candidates. The canonical publication surface is the [GitHub Releases page](https://github.com/node-and-norm/human-influence-telemetry/releases).

A document in this directory does not create a release. A version becomes public only when its release gates pass, the exact commit is validated, the tag exists, and the GitHub release is published.

## Published releases

| Version | Date | Primary change | Status |
|---|---|---|---|
| [`0.1.0`](v0.1.0.md) | 2026-07-16 | Foundation specification, schema, catalog, handbook, fixtures, and validator | Published |
| [`0.2.0`](v0.2.0.md) | 2026-07-16 | Historical public case narratives and assessments | Published |
| [`0.2.1`](v0.2.1.md) | 2026-07-16 | Evaluation, recruitment, provenance, and archival infrastructure | Published |
| [`0.4.0`](v0.4.0.md) | 2026-07-18 | Breaking normative contract stabilization | Published |
| [`0.5.0`](v0.5.0.md) | 2026-07-18 | Complete-record executable conformance | Published |
| [`0.6.0`](v0.6.0.md) | 2026-07-18 | First bounded independent human result; Maturity Level 2 | Published human-result release |
| [`0.6.4`](v0.6.4.md) | 2026-07-19 | Standalone software archive and version-specific Zenodo DOI | Published |
| [`0.6.5`](v0.6.5.md) | 2026-08-09 | Claim-evidence integrity audit and paper workspace | Published |
| [`0.6.6`](v0.6.6.md) | 2026-10-07 | Development workbench, reproducibility and release-readiness controls | Current published release; archive verified |

## Active and planned releases

| Version | State | Purpose | Publication condition |
|---|---|---|---|
| [`0.7.0`](v0.7.0-candidate.md) | Active candidate | Freeze three current-contract packets and the multi-case replication protocol | Human case selection, packet freeze, comparison tooling, locked protocol, exact-commit validation |
| `0.8.0` | Pending | Publish current-contract applications and empirical result or recruitment disposition | Application records and declared empirical outcome |
| `0.9.0` | Pending | Stable release candidate and clean-room implementation audit | Complete implementation packet, external audit, no release-blocking defect |
| [`1.0.0`](v1.0.0-candidate.md) | Gated candidate | Stable public contract and compatibility commitment | Every stable-contract gate in `docs/v1-readiness-plan.md` passes |

## Current version boundary

- Current repository release: `0.6.6`, published on GitHub and Zenodo
- Current published release: [`v0.6.6`](https://github.com/node-and-norm/human-influence-telemetry/releases/tag/v0.6.6); see the [publication receipt](../../release/v0.6.6/publication-receipt.json)
- Exact-version DOI: `10.5281/zenodo.23226713`
- Human-result release: `0.6.0`
- Concept DOI for all software versions: `10.5281/zenodo.21446141`
- Originating research DOI: `10.5281/zenodo.21204892`
- Version-specific software DOI for `v0.6.4`: `10.5281/zenodo.21446142`
- Version-specific software DOI for `v0.6.5`: `10.5281/zenodo.21864224`
- Version-specific software DOI for `v0.6.6`: `10.5281/zenodo.23226713`
- Normative assessment contract: `0.4.0`
- Conformance engine: `0.5.0`
- Research maturity: Level 2, Applicable
- Active empirical protocol: `HIT-IRP-HIT040-002`, candidate, scoring prohibited
- Stable target: `1.0.0`, release prohibited

Use the version-specific DOI for an exact release citation. Use the concept DOI when citing Human Influence Telemetry as an evolving software project across versions.

Release `0.6.5` adds research-integrity and paper controls. It does not alter the `0.4.0` contract, `0.5.0` engine, `0.6.0` human result, H3 boundary, or Level 2 maturity decision.

Version 0.6.6 collects the subsequent development record without changing those boundaries. The complete Ofqual draft remains pending author adjudication. All eight stable-release gates and current-contract replication remain unresolved; publishing the development archive does not satisfy them.

The presence of `0.7.0`, `0.9.0`, or `1.0.0` candidate materials in `main` does not authorize a tag, release, DOI archive, scorer activation, or maturity advancement.

## Release-control documents

- [`ROADMAP.md`](../../ROADMAP.md)
- [`docs/v1-readiness-plan.md`](../v1-readiness-plan.md)
- [`release/v1.0.0/contract-freeze.candidate.json`](../../release/v1.0.0/contract-freeze.candidate.json)
- [`implementation/v1.0.0-candidate/`](../../implementation/v1.0.0-candidate/)
- [`CHANGELOG.md`](../../CHANGELOG.md)
- [`CITATION.cff`](../../CITATION.cff)

## Metadata rule

`CITATION.cff` now identifies the verified `0.6.6` archive as `10.5281/zenodo.23226713`. The original tag and `.zenodo.json` publication input remain unchanged. This follow-up records publication and archival verification without moving the tag; its added receipt is outside the original archive. The prior `0.6.5` DOI continues to identify only that archive. Candidate documents may describe future versions, but they must not overwrite published-release metadata.
