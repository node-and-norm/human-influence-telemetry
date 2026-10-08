# Project Governance

Human Influence Telemetry is an open research artifact maintained by Mark Julius Banasihan through Node & Norm.

## Decision authority

The maintainer holds final release authority during the pre-`1.0.0` research and stabilization phase. This authority covers:

- normative changes to the specification;
- schema and rubric changes;
- release acceptance;
- claim and maturity status;
- provenance and publication boundaries;
- security and responsible-disclosure decisions;
- activation of scorer, packet, and clean-room audit materials;
- stable-contract promotion and compatibility commitments.

Maintainer authority does not convert unresolved empirical questions into settled findings. Claim status advances only when the evidence conditions in `RESEARCH.md` are met.

Candidate release files, merged readiness controls, branch names, and roadmap milestones do not authorize a tag or GitHub release. Publication requires the declared gate, exact-commit validation, and an explicit maintainer decision.

## Contribution process

Substantive changes should enter through a pull request. A normative change should state:

1. the problem being corrected;
2. the affected construct, field, rubric rule, or claim;
3. supporting evidence;
4. rival interpretations;
5. backward-compatibility consequences;
6. test or fixture changes;
7. the condition under which the change should be reconsidered.

## Normative and informative material

Normative material includes:

- `SPECIFICATION.md`;
- `schema/hit-assessment.schema.json`;
- the scoring definitions in `schema/hit-dimension-catalog.json`;
- release-tagged migration notes.

Informative material includes:

- examples and fixtures;
- application guidance;
- related-work discussion;
- retrospective case studies;
- framework mappings;
- candidate release plans and readiness records.

Informative material may explain the method but cannot silently change normative behavior.

## Release approval

Every release requires:

- passing automated validation on the exact release commit;
- synchronized version values across normative artifacts and metadata;
- an updated changelog and release note;
- an accurate maturity statement;
- no unresolved security issue affecting the release;
- explicit migration guidance for breaking changes;
- release assets matching recorded hashes;
- publication through the canonical GitHub Releases page.

A `1.0.0` release additionally requires:

- a completed and reviewed `0.9.0` release candidate;
- a clean-room implementation audit;
- synchronized stable specification, schema, catalog, handbook, implementation, fixtures, and compatibility records;
- a breaking-change review;
- current public applications or documented migration exceptions;
- every gate in `docs/v1-readiness-plan.md`;
- release language that separates semantic stability from research maturity.

[ADR-0005](docs/decisions/ADR-0005-separate-stable-and-empirical-tracks.md), dated 7 October 2026, separates stable track `HIT-STABLE-V100-001` from replication-study track `HIT-EMPIRICAL-HIT040-002`. Study-specific selection, packet freeze, and protocol publication remain requirements for the empirical track; they are not prerequisites for stable release. Independent human clean-room review remains a stable-release requirement. The candidate [gate register](release/v1.0.0/gate-register.json) lists the remaining stable blockers. Passing staging checks does not establish audit or release readiness.

## Empirical protocol authority

A locked human protocol may not be weakened after results or recruitment difficulty are observed. Any reduced-rater, adaptive, or alternate design requires a prospective numbered amendment or a new protocol.

The human case-selection decision, packet freeze, scorer activation, submission opening, comparison, adjudication, and maturity decision remain separate controlled actions.

## Conflicts of interest

Contributors should disclose institutional, commercial, litigation, standards, or publication interests that could materially affect a proposed scoring rule, case interpretation, or external-framework mapping.

## Stewardship transition

Broader governance may be introduced after sustained external contribution or institutional adoption. Any transition must preserve public version history, attribution, license continuity, and the distinction between evidence and aspiration.
