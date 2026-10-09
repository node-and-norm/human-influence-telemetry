# Advisory documentary-scope screening

Design: HIT-JEV-REVIEW-001. Prepared 7 October 2026, America/New_York, from repository commit `7544ce870307d74a84e745903a90461fc699b161`. The author authorized Jev assistance for bounded v1 priorities two and three. This amendment permits the development rehearsal below; it does not replace the frozen Ofqual plan or accept any scientific interpretation.

## Purpose and status

Use Jev to propose source-support classifications for six existing Ofqual evidence propositions and eight explicitly constructed scope or robustness items. The practical output is a review queue with source passages, unresolved questions, and model responses. Every item requires human review, including a confident supported answer. The run cannot assign HIT findings, change an assessment, accept an author decision, or satisfy a release gate.

The Ofqual case, draft propositions and outstanding objections are already exposed to the contributing assistant. Codex selects the extracts and questions with that knowledge. Model training exposure is unknown. This is an advisory development rehearsal, not a held-out test, independent assessment, accuracy study or inter-rater reliability study. There are no author reference labels for this run. Neither model agreement nor the number of probes met establishes accuracy or useful performance.

## Inputs and selection

The [source packet](sources.json) contains attributed extracts from four GOV.UK documents already in the six-document Ofqual inventory. The [source record](sources.md) states retrieval and transformation details, source dates, shared institutional lineage, withdrawal and update limitations, and the Open Government Licence basis for reuse. The OCR announcement and public code repository are outside this screening subset. Their exclusion does not amend the original assessment packet. Selected extracts do not become a full-document extraction evaluation.

The six natural claims are copied exactly from the existing draft: EC-ADVICE, EC-REASONS, EC-REISSUE-REQUIREMENT, EC-ISSUE-CORRECTION, EC-EXTERNAL-LIMIT and EC-ADMISSIONS-LIMIT. They address advice access, public reasons, implementation direction, reported issue and remaining remedy limits relevant to author decisions AD2 through AD5. They are selected for those open questions, not as a representative sample or because an outcome is known. AD1's suitability judgment and AD6's comparative-contribution judgment are outside Jev's authority.

Four additional constructed probes ask whether the excerpts establish event-specific access, internal deliberation, direct regulator operation, or universal remedy. They are deliberately broader than the draft propositions. They are not errors discovered in the manuscript, quotations from the historical sources, or evidence that the author made those claims.

Three paired conditions address period, conflicting evidence and faithful formatting. Period and formatting use EC-ISSUE-CORRECTION as their base. The conflict condition has a separate constructed event-level baseline, P02-base, with the same evidence; P02 adds only the synthetic denial to that baseline. These four constructed items inspect bounded model behavior on supplied text; they do not complete the original full-record qualitative reanalysis or rescore HIT dimensions.

| Probe | Transformation | Declared relation to inspect |
| :--- | :--- | :--- |
| P01 | Attribute the same replacement-grade issue event to 12 August instead of 19 August 2020 | The source's explicit date should prevent support for the backdated claim. The claim names the same event to avoid ambiguity about a second announcement. |
| P02, paired with P02-base | Add an explicitly synthetic, unresolved denial of the same issue event to an unqualified event-level proposition | The model should retain the internal conflict in the constructed scenario. The invented statement is never represented as a recovered historical document. |
| P03 | Change only whitespace in the original issue passage | The substantive support classification should remain the same as the base claim. Offline construction tests check that the normalized wording is unchanged. |

These expectations are assistant-authored design judgments, not human-adjudicated ground truth. Report each relation separately, including any violation or ambiguity; do not pool natural claims and constructed probes into an accuracy percentage. Pre-run methodological review caught an attribution error in the initial P02 proposal: denying an event does not contradict the proposition that guidance reports that event. The separate event-level pair repairs this design defect before inference; N04's original attributed proposition remains unchanged.

## Execution and handling

Use pinned model `jev-1.13.0` and the documented TypeSafe HTTP endpoint. Submit one batch of fourteen independent Choice questions, with empty shared state and each item's selected source passages in its own question. Question IDs, author-decision links, original assessment scores, reference labels and these expected relations must not supply answers to the model. The request presents source material as evidence, never as instructions. Synthetic evidence is labelled as part of a constructed scenario.

The four advisory options are supported, contradicted, insufficient and conflicting. These describe the supplied claim/excerpt relationship; they are not HIT finding states. The conflicting option preserves incompatible assertions when the supplied scenario does not resolve them. Missing or malformed provider responses are technical failures, not insufficient-evidence findings.

Before live inference, commit the design, protocol, sources, runner and protected input files. Preserve the exact request bytes, response bytes, model identity, source and input hashes, commit, timestamps, provider usage, failures and elapsed request time. Retained hashes identify bytes, not historical truth. The runner uses a private environment credential, refuses overwrite, disables redirects and proxies, and makes no automatic retry or fallback request. A failed or interrupted attempt remains visible; any revised attempt requires a new recorded amendment and run directory.

No confidence threshold permits acceptance, rejection, score changes or removal from the queue. Preserve input order and every scheduled item. Retain all probabilities and confidence values; distribution concentration does not establish source truth. The code may check identifiers, hashes, declared dates and response structure. It must not manufacture an author judgment to calculate agreement statistics.

## Reporting and next study

Separate natural claims, scope probes and paired robustness probes. Record what Jev returned, what a contributing assistant proposes about it, and what remains for the author. Preserve both disagreements and a finding that the screen added no useful issue beyond the existing queue. No study of human effort, user benefit, cost savings, institutional effects or comparative superiority is conducted here. Request latency is not researcher time saved.

The six Ofqual author decisions remain pending. Once the author sees this screen, later Ofqual decisions cannot serve as pre-model reference labels for evaluating this run. A later evaluated application requires a separately frozen source/claim selection and author judgments recorded before model-output exposure. Unresolved references remain unresolved. Author references would support an explicitly author-referenced comparison, not independent ground truth. An operational-benefit claim additionally needs recorded human review effort and errors under an appropriate design.

## Sources and assistance

The TypeSafe skill informed isolated questions, deterministic input checks, explicit uncertainty and separation of model output from workflow authority. Its [API](https://docs.typesafe.ai/api), [Choice](https://docs.typesafe.ai/primitives/choice), [state](https://docs.typesafe.ai/concepts/state), [confidence](https://docs.typesafe.ai/confidence), [model](https://docs.typesafe.ai/models) and [citation-checking](https://docs.typesafe.ai/cookbooks/citation_check) documentation was consulted on 7 October 2026. Cookbook auto-accept thresholds and the equation of an unlocated quote with fabrication are not adopted.

Codex and contributing software agents prepared and reviewed this amendment, source extraction, implementation and tests. This is development assistance, not independent peer review. Prior Jev runs, the Ofqual assessment and plan, published DOI metadata, normative contract 0.4.0, engine 0.5.0, historical human results, current-contract replication restrictions and stable-release gates remain unchanged.
