# ADR-0005: Separate stable-contract and replication-study release dependencies

**Status:** Accepted for implementation; no release authorized

**Date:** 2026-10-07, America/New_York

**Decision authority:** Mark Julius Banasihan

**Recorded by:** Codex, from the author's direction in the working conversation

## Authorization and scope

After a pressure test proposed five priorities, including explicit separation of stable release from replication-study preparation while retaining independent implementation review, the author directed: “Proceed with the priorities listed. Let's go to work. Let's always make sure to pressure test it as necessary.” This records approval to implement that bounded plan. It does not record acceptance of new documentary findings, a human source-review attestation, an audit signature, or release acceptance.

ADR-0001 remains a historical proposal with its original date and research context. This decision adopts the separation prospectively and resolves the present dependency conflict. It does not infer an earlier adoption date. ADR-0004's completed Level 2 decision and its historical evidence remain unchanged.

## Problem

The v1 plan permits semantic stability before completed current-contract replication, but its machine-readable blockers also require the study's human case selection, three frozen packets, and v0.7.0 protocol publication. This couples two different claims. The plan also calls an independent implementation reviewer preferred, while HIT-CRI-V100-001 requires an eligible person other than the author.

Passing staging validators currently means that prohibitions remain intact. It does not mean that the candidate can be audited or released. A missing migration-guide path passed those checks because declared artifact paths were not inspected.

## Decision

1. Track `HIT-STABLE-V100-001` governs the stable public assessment contract. Its remaining gates cover current-contract applications or substantiated migration exceptions, a complete implementation packet, independent clean-room review, a reviewed public v0.9.0 candidate, synchronized stable components, breaking-change review, metadata, and exact-release validation.
2. Track `HIT-EMPIRICAL-HIT040-002` retains the study-specific selection, packet-freeze, and publication obligations under `HIT-IRP-HIT040-002`. They no longer block the stable track merely because they are pending. They remain mandatory for activating that study.
3. The original human-only case selection, scoring prohibition, three-scorer/nine-submission design, submission preservation, and maturity rules remain unchanged. No solo application is an independent submission or a protected-slot selection.
4. One eligible independent human implementer remains required under `HIT-CRI-V100-001`. Author testing and AI testing prepare the packet; they cannot satisfy that eligibility rule.
5. Staging consistency, audit readiness, and release readiness must be reported separately. A candidate check cannot authorize promotion. Readiness checks fail closed while evidence or a reviewed acceptance mechanism is absent.
6. Historical assessment records, normative contract 0.4.0, engine 0.5.0, the 0.6.0 human result, released DOI metadata, and Level 2 remain unchanged.

The existing 0.7.0 and 0.8.0 labels identify planned study packages. If the stable track advances first, a later study publication needs an explicit chronological version allocation and any required prospective protocol amendment. This decision does not silently alter a protected publication condition or authorize a retrospective lower-version release.

## Application and migration threshold

The stable track retains the existing requirement for at least three compatible public applications or case-specific explanations that migration requires unavailable records. The four existing historical exceptions require review against that threshold. Missing structured fields, unfinished reassessment, or an AI-generated draft alone does not establish that source records are unavailable. Partial dossiers cannot be promoted by relabeling.

## Alternatives and pressure test

Keeping all study-preparation dependencies would preserve a coupling that does not establish stable-contract quality. Removing independent implementation review would weaken the public-implementability claim. Declaring v1 now would leave unfinished applications and packaging defects unresolved. Adding operational integrations would introduce new semantics before these obligations close.

The chosen approach narrows scheduling dependencies while preserving the evidence needed for each claim. It does not demonstrate construct validity, comparative usefulness, institutional effectiveness, or current-contract inter-rater reliability.

## Acceptance and reconsideration

Implementation requires synchronized governance, readiness documents, candidate ledgers, real-file checks, and negative tests. The stable release remains prohibited. Reconsider this decision if a completed application reveals an ungoverned semantic ambiguity, an external implementer needs private interpretation, or the separation permits an empirical claim without its declared evidence.

The [gate register](../../release/v1.0.0/gate-register.json) records current blockers. Evidence paths show work to inspect, not automatic proof that a gate passed.
