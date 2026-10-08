# ADR-0001: Separate Semantic Versioning from Research Maturity

**Status:** Proposed  
**Date:** 2026-07-17  
**Decision owner:** Mark Julius Banasihan  
**Repository:** Human Influence Telemetry

Historical-status note, 7 October 2026: the original Proposed status and historical context below are preserved. [ADR-0005](ADR-0005-separate-stable-and-empirical-tracks.md) prospectively adopts separate stable and empirical tracks and governs their current dependencies. No earlier adoption date is inferred.

## Context

Human Influence Telemetry currently uses two different systems to communicate two different properties:

1. repository and component versions describe the stability and compatibility of the public technical artifact;
2. maturity levels describe the strength of the evidence supporting research claims.

The current `SPECIFICATION.md` and `ROADMAP.md` make two independent human scorers a condition for `1.0.0`. The research maturity model uses the same exercise as the entry condition for Maturity Level 2 and as the update condition for claim H3.

This duplicates one empirical gate across two governance systems. It also prevents the public contract from becoming stable when the schemas, definitions, decision rules, conformance tests, migration notes, and non-claims are complete but a qualified scorer pair is unavailable.

No scorer submissions have been collected. No empirical result exists to reinterpret. This decision is therefore made before outcome data and cannot convert a failing result into a passing claim.

## Decision

Semantic versioning will govern the stability of the public technical contract.

Research maturity will govern the strength of the evidence supporting the method.

Version `1.0.0` may be released at Maturity Level 1 when the normative contract is stable, internally consistent, independently implementable from public artifacts, and protected by executable conformance tests.

The two-human inter-rater exercise remains mandatory for:

- claim H3;
- Maturity Level 2;
- any statement that independent human reviewers can apply HIT consistently;
- any reliability statistic or human reproducibility claim.

The locked protocol `HIT-IRP-CIGNA-001` remains unchanged. Its result must still be published when two eligible scorers become available, whether the result passes or fails.

## Stable-contract conditions for 1.0.0

Version `1.0.0` requires all of the following:

1. the six substantive dimensions and Telemetry Integrity have stable normative definitions;
2. the decision rules for `0`, `1`, `2`, and `IE` govern the ambiguity classes identified in `HIT-ARFR-001`;
3. the specification, schema, dimension catalog, handbook, fixtures, examples, validator, and migration notes are synchronized;
4. structural and semantic conformance tests cover valid, invalid, boundary, and contradictory cases;
5. the three released public cases validate under the candidate contract or have documented migration records;
6. the repository publishes a breaking-change review from component version `0.1.0`;
7. an implementation package contains every artifact needed to build and validate a conforming assessment without private explanation;
8. one public release candidate is published and no release-blocking defect remains open;
9. citation, provenance, archival, limitations, claim status, and non-claim metadata are current;
10. repository validation passes on the exact release commit.

## Research conditions that remain unresolved at 1.0.0

A stable contract does not establish:

- human inter-rater reliability;
- Maturity Level 2;
- causal validity;
- prospective institutional effectiveness;
- legal compliance or standards conformity;
- certification;
- independent institutional adoption.

The README, release notes, citation metadata, and research register must display the current maturity level and unresolved H3 status beside the version number.

## Version consequences

After `1.0.0`:

- backward-compatible clarifications, new examples, and new research results use minor or patch releases;
- a later human inter-rater result may be released in the `1.x` series when it does not break the stable assessment contract;
- normative changes that break the `1.0.0` contract require `2.0.0`;
- research maturity may advance without a major version change;
- a major version change does not imply maturity advancement.

## Risks

### Perception of lowered standards

Moving the scorer exercise out of the semantic-version gate may look like a response to recruitment difficulty.

The public record addresses that concern through four facts:

1. no scorer result exists;
2. the locked protocol remains intact;
3. H3 and Level 2 remain unresolved;
4. the stable-contract gates become more explicit and more executable.

### Stable syntax with unstable interpretation

A schema can be stable while scorers still disagree about meaning.

The `1.0.0` gate therefore requires normative decision rules for the known friction classes, boundary test vectors, and a published implementation package. Human reliability remains a separate empirical question.

### Version pressure from archival tooling

A DOI or integration behavior must not determine research claims. The archive identifies the released artifact. The repository version communicates compatibility. The maturity model communicates evidence strength.

## Rejected alternatives

### Keep human scoring as a 1.0.0 gate

This preserves the current roadmap but leaves technical stability blocked by scorer availability. It also duplicates the Level 2 evidence gate.

### Declare 1.0.0 immediately

The current rubric-friction review identifies unresolved normative ambiguity. A direct jump would freeze known interpretive defects into the public contract.

### Count model runs as independent human scorers

Model stress tests can expose ambiguity. They do not satisfy H3 or the locked human protocol.

## Update conditions

Revisit this decision when:

- external standards practice shows that version stability should include a specific empirical threshold;
- the stable contract cannot be implemented without unresolved author interpretation;
- a future human exercise reveals a breaking defect in the `1.0.0` semantics;
- the maturity model no longer communicates evidence strength accurately.
