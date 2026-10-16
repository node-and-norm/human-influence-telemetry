# Closeout author-review worksheet

Six grouped decisions cover the sixteen claims in the [development claim register](../../paper/development-claim-register.json) and the older unresolved judgments they depend on. Mark Julius Banasihan holds the responsible-author decision. This worksheet links the additive decisions as they are recorded; it supplies no source-verification attestation or release-gate credit.

Prepared 16 October 2026 for the [bounded closeout plan](../../docs/closeout-plan.md), with a decision date of 30 October 2026. The working manuscript, historical registers, assessments and results remain unchanged. Repository closeout and a possible manuscript submission are separate decisions.

## How to record a decision

For each group, identify any exceptions by claim ID and choose: retain the exact bounded wording; narrow it with replacement wording; omit it from a later manuscript; or retain it as explicitly unresolved. Cite the passage actually reviewed and record the date, reviewer and reason. A group response must name its covered claims. Silence and authorization to update the repository supply no scientific disposition.

File inspection can establish that a record contains a number, category, decision or source link. A reproducible calculation can establish how a recorded result was obtained. Neither operation authenticates the external source or establishes that an interpretation is warranted. Record source review separately from agreement with the manuscript wording. Existing author decisions retain their original scope.

Group 1's bounded descriptions are accepted for later-draft reuse under [AD-007](author-decisions.md#ad-007-closeout-group-1-bounded-wording). Group 2A's bounded DEV-C03 description is accepted under [AD-008](author-decisions.md#ad-008-closeout-group-2a-historical-human-result); the other four Group 2 decisions and Groups 3 through 6 remain pending. The unchanged current manuscript and its descriptive register retain their pending labels; these additive decisions do not approve the whole draft. Explicitly deferring the paper remains a permitted closeout decision.

## 1. Artifact descriptions and archive identity

Decision: which descriptions of the implemented artifact should a later draft retain, and with what limits?

Disposition: accepted with the presented limits on 16 October 2026 for DEV-C01, DEV-C02, DEV-C11 and DEV-C13. [AD-007](author-decisions.md#ad-007-closeout-group-1-bounded-wording) preserves the question, exact author response, accepted descriptions and absence of an independent source-review attestation.

| Claim | Record and locator to inspect | Qualification to retain |
| :--- | :--- | :--- |
| DEV-C01 | [Specification](../../SPECIFICATION.md), sections 6 and 7: six substantive dimensions and two integrity objects. | Representing these distinctions does not establish that they adequately measure practical control. |
| DEV-C02 | [Historical audit](../../audits/v0.6.5/audit-results.json), `negative_controls`; [evaluator](../../scripts/run_research_integrity_audit.py), `evaluate`: six eligible mapped claims and eight specified corruptions. | The evaluator aggregates recorded judgments. It does not independently authenticate support or measure fitness; historical eligibility does not transfer to the development draft. |
| DEV-C11 | [0.6.6 receipt](../../release/v0.6.6/publication-receipt.json), record `23226713`; [0.6.7 receipt](../../release/v0.6.7/publication-receipt.json), `release_commit`, `zenodo` and `scope`. | The archived draft's statement about 0.6.6 remains historical. The proposed update below concerns a later draft only. Archive verification supplies no scientific approval. |
| DEV-C13 | [File bindings](../../evidence/research-integrity-bindings.json), `file_and_dependency_consistency_only`; [checker](../../scripts/validate_claim_bindings.py), `build`; [release amendment](../../release/v0.6.7/frozen-input-amendment.json). | Thirteen claim bindings and nineteen evidence references concern file identity and dependencies. The documented historical-file resolution preserves the old context; it cannot establish source truth or publication eligibility. |

ACCEPTED for a later draft, not yet applied, DEV-C11: “Version 0.6.7 has a verified exact-version software/research-artifact archive, DOI 10.5281/zenodo.23252877, bound to commit `4336b8acd16d571ef9b5ab1d8ca1ecc2ea0eb01e`. It contains the working manuscript and exhibits; later closeout records require their own revision identification.” The receipt reports all 382 tracked file bytes matching the archive. [AD-007](author-decisions.md#ad-007-closeout-group-1-bounded-wording) accepts this bounded update for later reuse; it changes neither the archived manuscript nor the current descriptive register and does not attest a fresh archive comparison.

## 2. Historical human evidence and earlier case qualifications

Decision: retain the narrow historical human observation, and give each older open interpretation a disposition without changing released scores?

Partial disposition: DEV-C03 accepted with the presented limits for later-draft reuse on 16 October 2026 under [AD-008](author-decisions.md#ad-008-closeout-group-2a-historical-human-result). This accepts no other Group 2 item and supplies no independent source-review attestation.

| Claim | Record and locator to inspect | Qualification to retain |
| :--- | :--- | :--- |
| DEV-C03 | [0.6.0 release](../../docs/releases/v0.6.0.md), “7 of 7”: two eligible independent scorers, one frozen Cigna packet, scorer contract 0.1.0. | The seven items share one case; all six substantive ratings use one category and kappa is undefined. The result supplies no population reliability estimate, source truth, construct validity or current-contract replication. Bounded later-draft wording is accepted in AD-008; the current manuscript remains unchanged. |

The following older items require their own explicit answers within this group:

- CA-01: inspect [claim audit](claim-audit.json), `CA-01`, and the [historical Dutch assessment](../../case-studies/assessments/toeslagenaffaire-harm-period.json), “The public record does not show an exercised authority.” Its historical Reform rationale concerns unobserved exercise. Any current-contract reuse requires a new bounded assessment that distinguishes absent authority, formal authority, operative change and unresolved evidence. Preserve the historical score. Decide whether to defer that new application or commission it separately under the closeout plan's scope rule.
- CA-06: inspect [claim audit](claim-audit.json), `CA-06`, and [specification](../../SPECIFICATION.md), dimension-specific rules in section 6. For each future use of a finding of 2, identify the actual evidence route, including observed exercise or qualifying capability where permitted. Review whether the draft describes each retained route accurately; this worksheet changes no finding rule.
- SOLO-A-03: inspect [Obermeyer dossier](solo-001/dossier.md), `SOLO-A-03`. Decide whether to retain its warning against inferring a positive deployer profile from clinician involvement. Role, access, reasoning, override authority and intervention are separate propositions. [AD-001](author-decisions.md#ad-001-obermeyer-qualifications) already accepts the narrower SOLO-A-01 and SOLO-A-02 qualifications; it leaves SOLO-A-03 unresolved and does not attest independent source re-reading.
- Original queue item 3: inspect the [series selection freeze](solo-series.md), “Inventory and dispositions” and “C: fixed source boundary and questions,” alongside the [original queue](priority-status.md#author-decision-queue). Whole-series selection and the scope amendment remain pending. Ofqual and Robodebt are automation-boundary applications, with no established claim that they validate AI systems. Robodebt covers recommendations 17.1 and 17.2 at the stated cutoff, without a verified publication-day snapshot or evidence of subsequent implementation. The author can accept, revise or reject that scope, or explicitly defer its review; the later bounded Ofqual decision does not adjudicate the whole series.

## 3. Ofqual use, accepted scope and unresolved comparison

Decision: is the proposed account of the existing author decisions accurate, and should Counsel and the comparison remain explicitly unresolved in a later draft?

| Claim | Record and locator to inspect | Qualification to retain |
| :--- | :--- | :--- |
| DEV-C04 | [Application plan](solo-002-complete/plan.md), “Assessment boundary”; [source ledger](solo-002-complete/source-ledger.md), “Independence and temporal checks.” | The accepted use concerns an exceptional 17 August 2020 regulatory event and an exploratory automation-boundary example. It establishes neither ordinary oversight nor general AI-governance validity. |
| DEV-C05 | [Exact author record](solo-002-author-review.json), `SOLO-002-AD1` through `SOLO-002-AD7`; [original review status](solo-002-complete/review-status.json), `draft_pending_author`. | Judgment, Command, Correction and Reform 2 retain their stated event-level limits; Repair 2 uses operational direction only. Both integrity components remain limited. Counsel has no accepted category. No universal remedy, independent source verification or manuscript approval follows. |
| DEV-C14 | [Comparison challenge](solo-002-comparison-challenge.md), sections 1 and 3; [original comparison](solo-002-complete/baseline-and-review.md), Q2 and Q4. | A selected field projection omits qualifications retained in full rationales. The baseline shares HIT evidence infrastructure. No reader errors, burden reduction, full-method loss or net benefit were measured. |

Counsel requires a separate disposition within this group. The existing response was “Leave this decision unresolved”; it accepts neither the proposed IE nor alternative 1. Keeping that uncertainty needs no invented category. Resolving it would require an explicit source-based author judgment and an additive record.

The comparison also requires its own disposition. “Identify a missed distinction or loss” requested further analysis; it accepted neither the proposed tie nor a loss. Review the actual omission in the restricted projection separately from its untested practical consequences. The [author-review supplement](solo-002-author-review.md#current-dispositions) preserves the accepted limits and open decisions.

Original queue item 4 also covers all three earlier partial dossiers: [Obermeyer's matched analytical comparison](solo-001/dossier.md#matched-analytical-comparison), [Ofqual's announcement-only comparison](solo-bc.md#b-ofqual-and-ocr-17-august-2020), and [Robodebt's recommendation-only comparison](solo-bc.md#c-royal-commission-recommendations-171-and-172). Their proposed ties remain pending, including the Obermeyer and Robodebt comparisons outside the later complete Ofqual application. Review each on its own frozen source boundary, together with the limited contribution statement in [closest methods](closest-methods.md#candidate-contribution-after-the-challenge). The author may explicitly defer any of these judgments; no later Ofqual finding supplies their acceptance or establishes comparative benefit.

## 4. Conditional analyses, exhibits and synthetic rehearsal

Decision: retain these materials as bounded development records, narrow their descriptions, or omit them from a later paper?

| Claim | Record and locator to inspect | Qualification to retain |
| :--- | :--- | :--- |
| DEV-C06 | [Original sensitivity report](solo-002-complete/sensitivity.md), “Disposition”; [extension report](solo-002-extension/report.md), S05, S06, S07 and “Comparison and author disposition”; [results](solo-002-extension/results.json), `completed_pending_author_review`. | Four earlier reanalyses and three later conditions are within-assistant reasoning. The eighteen extension ties are proposals; no replacement categories, independent rescoring or empirical equivalence follows. No additional evaluation API request occurred. |
| DEV-C15 | [Figure source data](../../figures/development-2026-10-08/data.json), `HIT-DEVELOPMENT-FIGURES-2026-10-08`; [source ledger](solo-002-complete/source-ledger.md), “Independence and temporal checks.” | The three exhibits depict structure, timing and qualification preservation. They add no empirical observations, independent historical verification or reader-performance result. |
| DEV-C16 | [Benchmark analysis](evidence-update-001/analysis.json), `affected_true_positive`; [protocol](evidence-update-001/PROTOCOL.md), “Design fixed before trial”; [report](evidence-update-001/report.md), “Execution and provenance.” | Two retained first responses each identify four injected changes with no scored difference. The highly cued eight-proposition task supplies no equivalence, comparative utility, human reliability or model-wide accuracy. Exact serving-model identity was unavailable; prose review remains pending. |

For DEV-C06, address all three later conditions explicitly: S05 changes the event boundary to 16 August; S06 introduces a synthetic conflict about one delivery event; S07 changes passage order and whitespace. Their completed execution does not accept their interpretations. Preserve the original four-condition record, frozen later inputs, assistant outputs and all disclosed dependence on prior knowledge.

## 5. Jev model observations and the preserved disagreement

Decision: retain the reported counts as development observations, with the interpretation and reference-label limits intact?

| Claim | Record and locator to inspect | Qualification to retain |
| :--- | :--- | :--- |
| DEV-C07 | [First report](jev-report.md), “All eight matched”; [analysis](jev-live-001/analysis.json), `matches`. | Eight matches concern eight exposed, assistant-authored expectations. They establish neither independently adjudicated accuracy nor time saving or HIT validation. |
| DEV-C08 | [Second report](passage-report.md), “nine of ten”; [AD-002](author-decisions.md#ad-002-p06-interpretation-disagreement). | Preserve 9/10, the frozen reference label `insufficient` and model label `contradicted`. P06 remains an event-identity interpretation disagreement; its handling decision establishes no proven model error. |
| DEV-C09 | [Ofqual advisory report](jev-review-001/report.md), “Paired conditions”; [analysis](jev-review-001/run-001/analysis.json), `scheduled`. | Fourteen valid responses, six natural propositions classified supported and paired relations observed once provide no human reference labels, pooled accuracy, full-document assessment or general robustness. Classification reservations remain. |

P06's immediate handling decision is already recorded. It needs no repeat experiment for closeout. Any future event-identity experiment would require a separate design and result while preserving the present record.

## 6. Contribution, remaining obligations and the paper decision

Decision: retain the bounded contribution and limits, then either defer the manuscript or approve a separately identified next-draft review task?

| Claim | Record and locator to inspect | Qualification to retain |
| :--- | :--- | :--- |
| DEV-C10 | [Literature review](literature-review.md), “Search record”; [closest methods](closest-methods.md), “Operational comparison”; [novelty audit](../../paper/novelty-audit.md). | Existing work addresses oversight limits, practical ability and authority, audit artifacts and claim-evidence arguments. The targeted passages provide no systematic coverage or proof of missing features in other methods. CA-05's wider novelty question and source-level author review remain open. |
| DEV-C12 | [Candidate contract freeze](../../release/v1.0.0/contract-freeze.candidate.json), `current_contract_replication`; [evaluation methods](evaluation-methods.md), “Construct validity and operational usefulness evaluation.” | Current-contract replication, independent implementation, construct validity and comparative benefit remain unresolved. Archive publication, software checks and work authorization satisfy none of these evidence requirements. |

For retained literature claims, verify the proposition at the cited primary-source passage and record the actual review coverage. A narrower prospective scope requires a recorded amendment. The [submission notes](../../paper/submission-notes.md#required-pre-submission-work) retain source, citation, declaration, venue-policy and exact-draft approval requirements. General repository authorization does not authorize a manuscript upload.

Original queue item 6 remains a pending choice: whether to seek one bounded external methodological critique using the [focused review packet](external-review.md), or explicitly defer it. That optional critique concerns a selected rule, literature proposition or documentary interpretation. It neither replaces nor waives the separate mandatory independent-human implementation audit for v1.0. The packet records no invitation or external result. Choosing a critique would still require the named task, suitable materials, reviewer arrangements and disclosure permissions; this worksheet sends no invitation and publishes no contact details.

## Completion record

Record each group response with covered claim IDs, exceptions, reviewed passages, source-review status, replacement wording where needed, reviewer and date. Carry unresolved items into the final closeout status with their missing evidence specified. Preserve original records and use an additive decision record for any new author judgment. Group 1 is recorded in AD-007 and Group 2A in AD-008; the remaining Group 2 items and Groups 3 through 6 await responses. The current manuscript's sixteen descriptive-register entries remain unchanged pending a separately identified draft revision and review; this does not erase the bounded later-draft acceptances recorded above.
