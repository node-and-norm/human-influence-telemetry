# Changelog

## [Unreleased]

### Stable-track readiness, 7 October 2026

- Adopted ADR-0005's prospective stable/empirical track separation while preserving protected replication rules and independent human implementation review.
- Repaired the declared migration-guide path and Cigna migration status; reviewed the limits of four existing historical exceptions without accepting them for v1.
- Added an unresolved stable-gate register, actual artifact-path checks, readiness-blocker reports, and negative tests. Staging success is explicitly distinct from audit and release readiness; future promotion acceptance still requires reviewed implementation.
- Added a public implementation rehearsal, task catalog, and draft audit-submission schema with an unperformed template.
- Froze the exploratory Ofqual complete-record application plan before new dimension findings. The development application and comparison work remain subject to source-based author adjudication.
- Preserved the 0.4.0 normative contract, 0.5.0 engine, 0.6.0 human result, published release 0.6.5 and its DOI boundaries. No new release, external audit, or current-contract replication is asserted.

## [0.6.5] - 2026-08-09

### Added

- Machine-readable claim-evidence mapping for H1 through H9 and four material working-paper claims.
- Five independent gates: traceability, integrity, human support review, evidence fitness, and dependency closure.
- Claim-specific fitness judgments for directness, contemporaneity, independence, completeness, and publication authority.
- Eight negative controls, deterministic audit output, `PASS_WITH_EXCEPTIONS`, and E5 claim-boundary checks.
- Research lineage, AI-assistance disclosure, paper workspace, derived figure data, and a reproducible SVG publication figure.

### Preserved boundaries

- Normative contract and assessment schema: `0.4.0`.
- Complete-record conformance engine: `0.5.0`.
- Bounded human-result release and maturity decision: `0.6.0`, Level 2, Applicable.
- Previous exact-version DOI: `v0.6.4`, `10.5281/zenodo.21446142`.
- Exact v0.6.5 DOI: `10.5281/zenodo.21864224`.
- HIT software concept DOI: `10.5281/zenodo.21446141`.
- Originating research DOI, separate from the software lineage: `10.5281/zenodo.21204892`.
- Current-contract external-rater replication: separate, unresolved, and scoring-prohibited.

All notable changes to Human Influence Telemetry are documented here.

The project uses Semantic Versioning for the public technical artifact. Research maturity is reported separately.

## [Unreleased]

### Added

- Candidate current-contract replication architecture under protocol `HIT-IRP-HIT040-002`
- Human-governed source-audit and case-selection controls
- Recruitment-contingency rules that prohibit silent reduction of the empirical design
- Draft manual workbooks for Scorers A, B, and C, plus an unassigned master template
- Machine-readable `1.0.0` stable-contract gate ledger
- Candidate clean-room implementation packet and protocol `HIT-CRI-V100-001`
- Canonical release index distinguishing published releases from candidate release documents
- Public README status table covering `0.6.4`, `0.7.0`, `0.9.0`, and the gated `1.0.0` target

### Changed

- Public status language distinguishes the current published release from the stable-contract target
- The main README explains what `1.0.0` will and will not claim
- Project governance, contribution, security, research, provenance, and release documentation use the pre-`1.0.0` stabilization boundary
- Published-release metadata is synchronized to `0.6.4` and its software DOI
- Fixed
  - Formatted human-result metadata and normalized the concept DOI for the `v0.6.4` release; added the exact public-status sentence expected by automated validation to README.md and the release notes.

### Planned

- Complete the signed human selection of three current-contract cases
- Freeze three packet boundaries, source manifests, identifiers, and digests
- Lock and publish the `0.7.0` replication package
- Produce additional public current-contract assessments
- Conduct the clean-room implementation audit
- Prepare and publish a public release candidate in `0.9.0`
- Promote synchronized stable components to `1.0.0` only after every gate passes
- Develop a preregistered prospective validation protocol

### Research boundary

One passing frozen-packet exercise does not establish general inter-rater reliability, field effectiveness, causal validity, legal correctness, certification, or adoption.

Candidate `0.7.0`, `0.9.0`, and `1.0.0` materials do not create a release, authorize scoring, or advance research maturity.

## [0.6.4] - 2026-07-19

### Added

- Version-specific Zenodo software DOI: `10.5281/zenodo.21446142`
- Standalone public software archive for release `v0.6.4`
- Synchronized citation, Zenodo, release-index, provenance, and README metadata

### Changed

- Latest published repository release advances from `0.6.0` to `0.6.4`
- Software DOI status changes from pending to published

### Unchanged

- Normative specification, schema, catalog, and handbook remain `0.4.0`
- Conformance engine remains `0.5.0`
- Human inter-rater result remains the `0.6.0` bounded exercise
- H3 remains supported for one frozen packet
- Research maturity remains Level 2, Applicable

## [0.6.0] - 2026-07-18

### Added

- Two verified independent scorer JSON submissions under locked protocol `HIT-IRP-CIGNA-001`
- Original, correction, receipt, and transcription-verification records
- Deterministic pre-adjudication comparison in JSON and Markdown
- Preservation and release-asset manifests
- No-disagreement adjudication record
- H3 and Maturity Level 2 decision
- ADR-0004
- Human-result release notes and exact-head validation rules

### Result

- Exact agreements: 7 of 7
- Exact-agreement proportion: `1.0000`
- Critical disagreements: 0
- Advancement threshold: met
- Supplementary Cohen's kappa: `null` because all six substantive ratings used one category

### Changed

- Repository version advances to `0.6.0`
- Research maturity advances to Level 2, Applicable
- H3 changes from unresolved to supported for one frozen packet
- Cigna migration disposition changes from protocol-deferred to protocol-completed historical version binding
- Conformance engine remains `0.5.0`
- Specification, schema, catalog, handbook, and scoring semantics remain `0.4.0`

### Research boundary

This release reports one exercise with two scorers, seven categorical items, one retrospective insurance case, and the preserved `0.1.0` scorer contract. It does not estimate population reliability.

## [0.5.0] - 2026-07-18

### Added

- Reusable complete-assessment conformance engine for the `0.4.0` contract
- Public CLI, stable error codes, deterministic reports, compatibility metadata, migration planning, and complete-record vectors

### Compatibility

Version `0.5.0` is implementation-compatible with the `0.4.0` normative assessment contract.

## [0.4.0] - 2026-07-18

### Added

- Evidence states, explicit finding thresholds, dimension-specific rules, Repair triggers, split Telemetry Integrity, actor-authority controls, structured evidence propositions, precise locators,[...]

### Compatibility

Version `0.4.0` is a breaking normative and data-contract release. Historical `0.1.0` assessments remain immutable.

## [0.2.1] - 2026-07-16

Added the locked inter-rater protocol, frozen scorer packet, comparison tooling, coordinator materials, recruitment package, rubric-friction review, model stress-test protocol, and archival metadata.

## [0.2.0] - 2026-07-16

Added three public retrospective case narratives and four actor-specific machine-readable assessments.

## [0.1.0] - 2026-07-16

Established the first public HIT specification, schema, catalog, handbook, fixtures, validator, governance files, and release controls.

[Unreleased]: https://github.com/mj3b/human-influence-telemetry/compare/v0.6.5...HEAD
[0.6.5]: https://github.com/mj3b/human-influence-telemetry/compare/v0.6.4...v0.6.5
[0.6.4]: https://github.com/mj3b/human-influence-telemetry/compare/v0.6.0...v0.6.4
[0.6.0]: https://github.com/mj3b/human-influence-telemetry/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/mj3b/human-influence-telemetry/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/mj3b/human-influence-telemetry/compare/v0.2.1...v0.4.0
[0.2.1]: https://github.com/mj3b/human-influence-telemetry/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/mj3b/human-influence-telemetry/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/mj3b/human-influence-telemetry/releases/tag/v0.1.0
