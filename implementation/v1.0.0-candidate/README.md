# HIT v1.0.0 Candidate Implementation Packet

**Status:** Candidate, incomplete  
**Target release path:** `v0.9.0` clean-room release candidate, then `v1.0.0` stable contract  
**Private explanation permitted:** No

## Purpose

This directory defines the standalone public packet that a technically competent external implementer must be able to use without private author explanation.

The packet is complete only when every listed artifact is copied or referenced at an exact validated commit and the clean-room audit protocol can be executed from a fresh environment.

The [quickstart](quickstart.md) and [task catalog](task-catalog.json) prepare public implementation tasks. The [submission schema](audit-submission.schema.json) and [pending example](audit-submission.example.json) define records to review before activation. A pending example is not an audit, a signature, or an eligible reviewer record. The manifest's missing-before-activation list includes final review and freeze of these controls even when draft files exist.

The future eligibility file uses the same auditor object defined at `$defs.auditor` in the submission schema. The manifest references that file by repository-relative path and SHA-256. The human supplies the identity, competence, conflicts, prior exposure and independence declarations; a designated human must verify eligibility and the origin of those declarations. Syntax and hash checks cannot authenticate the person. No eligibility file or reviewer is supplied in this candidate.

## Required normative artifacts

- `SPECIFICATION.md`;
- `docs/application-handbook.md`;
- `schema/hit-assessment.schema.json`;
- `schema/hit-dimension-catalog.json`;
- `docs/adjacent-system-boundaries.md`;
- current compatibility manifest;
- migration guide;
- current claim register and limitations.

## Required implementation artifacts

- public package entry point;
- conformance command documentation;
- migration-plan command documentation;
- stable error-code catalog;
- one canonical valid complete assessment;
- invalid complete-assessment vectors;
- boundary fixtures;
- deterministic comparison example;
- expected output digests;
- installation and environment instructions.

## Auditor tasks

The auditor must, without private explanation:

1. install the package in a fresh environment;
2. identify the current specification, schema, catalog, handbook, and engine versions;
3. validate one complete conforming assessment;
4. run at least three invalid vectors and explain every returned error code;
5. identify the actor, evidence-claim, finding, Repair-trigger, sampling, aggregation, and Telemetry Integrity invariants;
6. generate a migration plan for one preserved `0.1.0` assessment;
7. reproduce one deterministic inter-rater comparison from public inputs;
8. distinguish HIT from runtime governance, signed-receipt verification, policy-pack harmonization, compliance automation, and evidence portability;
9. record every point where the public packet is ambiguous, incomplete, or requires private author knowledge;
10. produce a signed audit record with environment details, commands, outputs, and unresolved defects.

## Evidence boundary

A clean-room audit evaluates public implementability and documentation sufficiency. It does not establish inter-rater reliability, evidence truth, causal effectiveness, legal correctness, certification, or institutional adoption.

## Packet activation and completed audit

The packet remains incomplete and audit activation remains prohibited until:

- the current-contract application path is resolved;
- final target component versions are selected;
- exact artifact hashes are recorded;
- the comparison implementation and reproducible example are final;
- the submission schema and exact environment are reviewed and frozen;
- an eligible independent human reviewer is recorded;
- the exact packet commit passes activation validation and the maintainer authorizes the audit.

After activation, the independent reviewer must run the protocol. All release-blocking defects must be repaired and affected tasks rerun before stable release. An explicitly reasoned nonblocking classification may retain a finding; a maintainer cannot satisfy the gate by accepting an unresolved release-blocking defect.

Run `python scripts/validate_v1_implementation_packet.py` for staging consistency. Use `--mode audit-ready` to inspect unmet readiness requirements; the current candidate must fail that mode. These checks do not establish independent implementability. Future activation requires a reviewed acceptance policy, not a status edit alone.
