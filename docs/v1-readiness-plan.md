# Human Influence Telemetry v1.0.0 Readiness Plan

**Updated:** 8 October 2026
**Governing decision:** `ADR-0005`, prospectively resolving `ADR-0001`'s historical proposal
**Current repository release:** `0.6.7`
**Publication state:** Prepared; GitHub publication and Zenodo archival verification pending. Latest verified published release: `0.6.6`.
**Human-result release:** `0.6.0`
**Current exact-version DOI:** pending verification for `0.6.7`
**Software concept DOI:** `10.5281/zenodo.21446141`
**Previous exact-version DOI, v0.6.6:** `10.5281/zenodo.23226713`
**Previous exact-version DOI, v0.6.5:** `10.5281/zenodo.21864224`
**Previous exact-version DOI, v0.6.4:** `10.5281/zenodo.21446142`
**Current normative contract:** specification, assessment schema, dimension catalog, and handbook `0.4.0`
**Current conformance engine:** `0.5.0`
**Current research maturity:** Level 2, Applicable
**Active empirical protocol:** `HIT-IRP-HIT040-002`, candidate, scoring prohibited

## 1. Release claim

Version `1.0.0` will mean that HIT has a stable public assessment contract that can be implemented from public artifacts, applied without private author interpretation, and checked through executable conformance tests.

Version `1.0.0` is a compatibility and implementation claim. It is not a claim of population-wide inter-rater reliability, causal effectiveness, legal correctness, certification, or institutional adoption.

Research maturity remains governed by `RESEARCH.md`. A stable `1.0.0` contract may coexist with Maturity Level 2 when the stable-contract gates pass before the three-case replication is complete.

## 2. Current evidence baseline

### Complete

- six substantive dimensions and split Telemetry Integrity;
- explicit `0`, `1`, `2`, and `IE` evidence-state rules;
- actor and authority attribution contract;
- Repair trigger;
- sampling and aggregation contract;
- contradiction and procedural-posture treatment;
- structured evidence claims and precise locators;
- normative contract `0.4.0`;
- 48 deterministic boundary fixtures;
- complete-assessment conformance engine `0.5.0`;
- one valid and fifteen invalid complete-record vectors;
- stable machine-facing error codes;
- deterministic reports and public CLI;
- protected migration planning;
- adjacent-system claim boundaries;
- first locked human exercise under the archived `0.1.0` scorer contract;
- two eligible independent scorers, two preserved submissions, 7 of 7 exact agreements, and zero critical disagreements;
- bounded H3 support and Maturity Level 2 decision;
- standalone software archive and version-specific DOI `10.5281/zenodo.21446142`;
- preserved v0.6.5 exact-version archive DOI `10.5281/zenodo.21864224`;
- candidate current-contract replication architecture;
- candidate source-audit controls;
- candidate recruitment contingency;
- draft manual workbooks for three future scorers.
- v0.6.5 claim-evidence integrity controls, paper workspace, and reproducible claim-gate figure.

The prepared 0.6.7 package records further development work: partial Ofqual author review, a comparison challenge, additional qualitative reanalysis, source-binding verification, a synthetic evidence-update rehearsal, and three manuscript exhibits. These additions preserve all eight unresolved stable gates. The same scored outcome for both assistant responses does not establish comparative advantage or human usefulness; manuscript and reanalysis interpretations remain subject to their stated review requirements.

### Pending

- signed human selection of one exercise-rich, one constraint-rich, and one evidence-limited case;
- three frozen `0.4.0` packet boundaries and source manifests;
- locked `v0.7.0` protocol package;
- three current-contract public applications;
- clean-room implementation audit;
- public `v0.9.0` stable release candidate;
- final breaking-change review and `1.0.0` contract promotion.

## 3. Separate release and empirical tracks

Stable track `HIT-STABLE-V100-001` and empirical track `HIT-EMPIRICAL-HIT040-002` have separate dependencies under [ADR-0005](decisions/ADR-0005-separate-stable-and-empirical-tracks.md). The study-specific 0.7.0 selection, packet-freeze, and publication obligations below remain in force for the empirical protocol. They do not block stable release. The [gate register](../release/v1.0.0/gate-register.json) identifies stable blockers and their current evidence surfaces.

The 0.7.0 and 0.8.0 labels are planned study-package labels, not promises about the order of future tags. If the stable track advances first, study publication requires an explicit chronological version allocation and any required prospective protocol amendment. No protected protocol is activated by this plan.

### `0.7.0`: frozen current-contract replication package

Required:

- signed human case-selection decision;
- exactly three immutable packet IDs and versions;
- three frozen decision boundaries;
- three frozen source manifests and source archives or stable identifiers;
- final scorer and coordinator instructions;
- locked manual scorer workbooks;
- deterministic three-scorer comparison implementation;
- synthetic pass, fail, critical-disagreement, hash, identity, and boundary-deviation vectors;
- exact-commit validation;
- protocol status `locked` and `scoring_permitted: true`.

`0.7.0` publishes the study design and packet materials. It does not publish findings.

### `0.8.0`: current-contract application and replication result

Preferred result package:

- three eligible independent scorers;
- nine preserved submissions;
- pre-adjudication comparison;
- disagreement classification;
- adjudication record that preserves original scores;
- H3 replication decision;
- Maturity Level 3 decision under predeclared rules.

Recruitment failure does not authorize a silent downgrade. A reduced design requires a numbered pre-scoring amendment or new protocol. With zero viable independent scorers, H3 replication remains unresolved and Level 3 remains pending.

The application track may still publish three current-contract author or coordinator applications when their provenance is explicit and they are not relabeled as inter-rater evidence.

### `0.9.0`: stable release candidate and clean-room audit

Required:

- candidate contract versions frozen;
- specification, schema, catalog, handbook, implementation, fixtures, examples, validator, and CLI synchronized;
- current-contract application surface documented;
- migration and historical-version boundaries current;
- standalone implementation packet containing only public artifacts;
- clean-room auditor receives no private explanation;
- auditor installs the package, validates a complete assessment, explains error codes, generates a migration plan, and reproduces one comparison;
- every point requiring private author knowledge is recorded;
- release-blocking documentation or conformance defects corrected;
- original audit records preserved;
- public `v0.9.0` release candidate published;
- no release-blocking defect remains open.

A technically competent independent human reviewer is required for the clean-room audit under HIT-CRI-V100-001. The reviewer must be someone other than the author and must have made no material contribution to the packet. Model implementation audits may supplement this work, but model outputs remain development evidence and do not satisfy auditor eligibility or count as human reliability evidence.

### `1.0.0`: stable public contract

The stable release promotes the reviewed contract to version `1.0.0` only when the release gates below pass.

## 4. Stable-contract gates

### A. Normative completeness

- all six substantive dimensions have stable definitions;
- Telemetry Integrity remains split into institutional-record and assessment-packet components;
- `0`, `1`, `2`, and `IE` govern every known ambiguity class;
- actor, authority, temporal, Repair, contradiction, sampling, aggregation, and locator rules are explicit;
- no known ambiguity can systematically change a finding without a governing rule.

### B. Contract synchronization

- `SPECIFICATION.md` version `1.0.0`;
- application handbook version `1.0.0`;
- assessment schema version `1.0.0`;
- dimension catalog version `1.0.0`;
- canonical examples version-compatible with the stable contract;
- conformance implementation and error catalog synchronized;
- compatibility manifest defines supported historical versions and migration boundaries.

### C. Executable conformance

- positive, negative, and boundary fixtures pass deterministically;
- complete-record mutation cases cover known invalid states;
- actor and evidence-claim references are validated;
- finding and evidence-state invariants are validated;
- Repair-trigger and Telemetry Integrity derivation are validated;
- sampling, aggregation, citation, and version invariants are validated;
- public CLI commands pass;
- reports are byte-stable where declared;
- one-command exact-commit validation passes.

### D. Public implementability

- implementation packet contains every artifact required to apply the method;
- clean-room audit requires no private author explanation for a valid application;
- technical-help boundaries distinguish access and schema assistance from substantive coaching;
- public terminology distinguishes documentary telemetry from runtime observability, policy enforcement, signed-receipt verification, and evidence portability.

### E. Application and migration evidence

- at least three public applications under a compatible current contract exist, or the release record explains why specific historical cases cannot be migrated without unavailable records;
- every current application states its author, boundary, source surface, and independence status;
- author-scored applications are not represented as independent replication;
- historical `0.1.0` records remain immutable;
- automatic migration remains prohibited when fresh judgment is required.

The four historical migration exceptions already exist. Their adequacy for this gate remains unresolved: absent structured fields or unfinished source review does not by itself establish unavailable records. A new assistant-prepared record remains pending until responsible-author interpretation review. Neither three partial dossiers nor structural validation alone satisfies this gate.

### F. Release integrity

- breaking-change review complete;
- limitations and claim register current;
- adjacent-system claim audit passes;
- README, roadmap, research register, provenance, citation, changelog, and archival metadata synchronized;
- release notes identify exact component versions and research maturity;
- exact release commit passes CI;
- release assets match recorded SHA-256 hashes;
- no release-blocking issue remains open.

## 5. Required `1.0.0` artifacts

- stable specification `1.0.0`;
- stable assessment schema `1.0.0`;
- stable dimension catalog `1.0.0`;
- stable application handbook `1.0.0`;
- terminology and adjacent-system boundary contract;
- conformance implementation, fixtures, and report format;
- compatibility manifest and migration guide;
- breaking-change review;
- clean-room implementation packet;
- clean-room audit record;
- current public applications or documented migration exceptions;
- current claim register, maturity statement, limitations, and non-claims;
- release notes, citation metadata, provenance, and archival metadata;
- exact release commit with passing validation.

## 6. Manual-workbook readiness

Draft manual workbooks now exist for `HIT-SCORER-A`, `HIT-SCORER-B`, and `HIT-SCORER-C`, plus an unassigned master template. Each workbook contains three full assessment sections and mirrors the `0.4.0` assessment contract.

The workbooks remain candidate assets. They cannot be activated until `v0.7.0` locks the three packet IDs, boundaries, source manifests, and study instructions. Their current hashes are recorded under `validation/v0.7.0/manual-workbooks/`.

This work closes a procedural readiness gap. It does not advance H3 or research maturity.

## 7. Mandatory release language

The `1.0.0` release must state the research maturity supported at publication time and must distinguish semantic stability from empirical validation.

At minimum, the release must state:

- HIT is a documentary assurance method;
- the stable contract does not establish legal compliance, causal effectiveness, certification, truthful reasoning, or institutional adoption;
- HIT is not a runtime governor, signed-receipt protocol, policy-pack platform, compliance engine, or evidence-portability mechanism;
- author applications and model audits are not inter-rater evidence;
- H3 and Level 3 claims are limited to the exact independent human evidence available at release time;
- incomplete recruitment is reported as incomplete recruitment.

## 8. Stop conditions

Withhold `1.0.0` when any condition remains true:

- a known ambiguity can change a finding without a governing rule;
- schema, catalog, handbook, fixtures, implementation, examples, or validator disagree;
- the implementation packet requires private author explanation;
- no public `v0.9.0` release candidate has completed clean-room review;
- public applications or migration exceptions are absent;
- overloaded terminology can collapse HIT into an adjacent governance layer;
- release metadata overstates reliability, validation, certification, adoption, or legal status;
- a release-blocking defect remains open;
- exact-release validation fails.

## 9. Immediate execution order

1. Reconcile stable-track controls and test missing-artifact and premature-promotion failures.
2. Complete a full current-contract documentary application with explicit source and author/AI provenance; finish the selected series or disclose incompleteness. Resolve the application-or-migration-exception gate separately.
3. Compare identical evidence with a capable structured review; preserve ties, losses, and full-document sensitivity failures.
4. Assemble and freeze the standalone implementation packet, environment, expected results, submission schema, and eligible reviewer record.
5. Run the independent human clean-room implementation audit; preserve failures and public amendments.
6. Publish `v0.9.0` and correct release-blocking defects.
7. Promote synchronized stable components to `1.0.0` only after every stable gate passes and the maintainer explicitly accepts the release.

On the separate empirical track, complete human case selection, freeze three packets, lock materials, publish the approved protocol package, and run the original three-scorer design or report recruitment failure. Current-contract H3 replication and Level 3 remain unresolved. No AI-generated source selection may enter the protected slots.

## 10. Readiness checks and scope control

The default v1 validators check staging consistency and must report release/audit prohibition. Explicit `--mode audit-ready` and `--mode release-ready` checks fail while required evidence or a reviewed promotion policy is absent. A green staging run is not evidence of completed readiness.

The [execution record](../research/strengthening/v1-priorities.md) tracks owners, dependencies, and remaining decisions. Operational dashboards, runtime integrations, new dimensions, multi-sector effectiveness claims, and additional small model batches are outside the v1 critical path. An informative findings-and-actions template may be tested without changing the normative contract.
