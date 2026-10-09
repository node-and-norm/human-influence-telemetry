# Human Influence Telemetry: Inspectable Documentary Judgments about Practical Human Authority

Working methods/resource draft, 8 October 2026. Prepared with AI assistance; responsible-author review and publication approval remain pending. This draft supplements the preserved [v0.6.5 manuscript](manuscript.md). Its [development claim register](development-claim-register.json) confers no publication eligibility through the historical audit.

## Abstract

An institutional record can identify a human reviewer without establishing what that person could understand, decide or change. Human Influence Telemetry (HIT) supplies an open representation for examining that distinction. Six substantive dimensions describe access to evidence, judgment, command, correction, repair and reform; separate integrity fields qualify the documentary record. Explicit findings distinguish affirmative absence, dimension-specific formal or ceremonial presence, substantive exercise and insufficient evidence. This paper describes the versioned contract, executable conformance checks and claim-publication controls. It separates a preserved two-scorer exercise, an AI-assisted documentary application with partial author adjudication, three bounded model-development runs and a synthetic evidence-update rehearsal. The human exercise records agreement on seven items in one packet under an earlier contract. The documentary comparison remains unresolved. In the rehearsal, one assistant response per representation identified four injected changes, with no scored difference between a HIT-inspired graph and a capable table. These development observations supply no independent confirmation. HIT's present contribution is an inspectable research artifact and a set of disclosed assessment problems. Comparative benefit, construct validity, current-contract reliability and operational effectiveness remain unestablished.

## 1. Problem and contribution

HIT asks what a defined documentary packet permits a researcher to say about a named authority during a specified period. Its intended object is practical influence in an AI-mediated institutional decision, not the mere presence of a signature or review step. A record may support the existence of a review channel while leaving access, reasoning or effective intervention unresolved. Conversely, missing records do not establish that authority was absent.

The contribution is a versioned assessment representation with explicit evidence rules and executable consistency checks. It makes actors, periods, evidence routes, uncertainty and disagreements inspectable. The research question is whether this representation can support defensible documentary judgments and identify their limits. The repository implements the representation; it has not established that using it improves judgments. No claim of firstness, superiority or comprehensive coverage follows from its implementation.

## 2. Related work and positioning

Green's review of 41 human-oversight policies questions assumptions about people's ability to perform the prescribed oversight. HIT cannot answer that challenge merely by documenting human involvement. Its findings must leave the justification for algorithm use and the effectiveness of oversight open. This comparison draws on the article's abstract and introduction, not a completed review of its entire argument. [Green, 2022](https://doi.org/10.1016/j.clsr.2022.105681).

Siebert and colleagues connect human responsibility with the ability and authority to act, including organizational conditions. HIT's Command and actor-attribution rules address related questions through documentary evidence. That adjacency does not establish that the rubric captures all conditions of meaningful control. [Siebert et al., 2023, §3.3](https://doi.org/10.1007/s43681-022-00167-3).

SMACTR already organizes internal algorithmic auditing through stages, stakeholders and documentary artifacts. Argument-based assurance already links contextual claims, arguments, evidence and subordinate claims. HIT therefore does not claim novelty for documentation or claim graphs alone. Its narrower candidate contribution is the particular practical-authority record and its testable finding boundaries. The ICO source is used for its conceptual account; its under-review notice precludes treating it as an unchanged legal rule. [Raji et al., 2020, §§4.1–4.6](https://arxiv.org/html/2001.00973v1); [ICO, Annexe 5](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/explaining-decisions-made-with-artificial-intelligence/annexe-5-argument-based-assurance-cases/).

These are purposive comparisons, not a systematic literature review. The [search record](literature-search-log.md) and [source-level comparison](../research/strengthening/literature-review.md) distinguish selected passages from pending full-text work. Wider review may narrow the contribution further; absence of a matched feature in the reviewed passages is not evidence that another method lacks it.

## 3. Method and implementation

### 3.1 Assessment object and findings

An assessment specifies its institutional unit, actor, decision process, system role, period, source packet and contract version before interpreting the evidence. The [0.4.0 specification](../SPECIFICATION.md) governs the six substantive dimensions:

| Dimension | Documentary question |
| :--- | :--- |
| Counsel | Did the named human authority have actual pre-decision access to relevant underlying evidence? |
| Judgment | What supports substantive evaluation rather than formal endorsement? |
| Command | What operational authority could alter, halt or override the process? |
| Correction | What substantive reconsideration of a decision is evidenced? |
| Repair | What qualifying response to acknowledged harm is evidenced? |
| Reform | What change to the decision architecture is evidenced? |

These questions summarize the contract; its dimension-specific requirements control. Findings are `0` for affirmative absence, `1` for applicable formal or ceremonial presence under the dimension's rule, `2` for substantive exercise or qualifying operational capability, and `IE` for insufficient evidence. For example, Counsel permits `1` for an applicable formal route without demonstrated retrieval; that does not prove ceremonial conduct. A lack of documents cannot by itself justify `0`. `IE` is neither a zero nor a value to average into a total. Telemetry Integrity separately assesses institutional-record integrity and assessment-packet integrity; it is not a seventh substantive dimension.

The assessor links each proposition to an attributable source and locator, identifies contrary material, and explains the inference to the finding. Actor and period restrictions prevent borrowing authority from another institution or backdating later action. Conflicting evidence must remain visible. Reusing one passage for several propositions requires distinct reasoning, not a claim that several independent observations exist.

The 0.5.0 engine checks complete records against the declared contract. It can reject missing fields and prohibited combinations. It cannot determine whether an institutional statement is true, whether a packet is complete, or whether an interpretation is persuasive. A structurally valid record can contain a disputable judgment.

![Conceptual architecture separates assessor interpretation, the complete six-dimension and two-integrity record, and software consistency checks.](../figures/development-2026-10-08/assessment-architecture.png)

Figure 1. The implemented assessment structure separates substantive interpretation from executable checks. The diagram is conceptual; it adds no evidence that HIT measures practical authority accurately. [Vector figure, data and source bindings](../figures/development-2026-10-08/README.md).

### 3.2 Publication controls

The v0.6.5 claim map covers H1–H9 and four paper claims. Its five gates concern traceability, integrity, human support review, evidence fitness and dependency closure. Fitness separates directness, contemporaneity, independence, completeness and publication authority. The [historical audit](../audits/v0.6.5/audit-results.json) reports six conclusion-eligible claims and eight detected prespecified corruptions under `PASS_WITH_EXCEPTIONS`.

The audit software resolves text locators, checks recorded integrity and support-review states, aggregates declared fitness judgments, and propagates dependency eligibility. Those operations do not independently authenticate the judgments or measure the five fitness dimensions. In particular, accepting a recorded `git_tracked` or `locked_digest` label is not itself a fresh verification of tracking or a digest. Separate byte checks must be identified where used. New development claims do not inherit the historical audit's eligibility.

An additive [file-binding check](../evidence/research-integrity-bindings.json) now covers the historical map's 13 claims and 19 evidence references. It checks actual tracked regular files, contained non-symlink paths, byte identity against its pinned Git revision, the locked comparison digest and acyclic dependencies. It preserves the historical evaluator and output. It does not validate human review, fitness or source truth, and does not recompute conclusion eligibility.

## 4. Evidence and observations

### 4.1 Preserved human exercise

The [0.6.0 release](../docs/releases/v0.6.0.md) reports two eligible independent scorers applying the earlier 0.1.0 scorer contract to one frozen Cigna packet. They agreed on all seven items, with zero critical disagreements. Both assigned `1` to six substantive dimensions and `limited` to Telemetry Integrity. The six substantive ratings lack category variance, so Cohen's kappa is undefined.

This is a descriptive result for the named scorers, packet and contract. Raw agreement does not correct for chance or establish construct validity; reporting must respect the design and statistic. [Hallgren, 2012, “Using percentages of agreement”](https://pmc.ncbi.nlm.nih.gov/articles/PMC3402032/). The result is neither a population reliability estimate nor replication of the current 0.4.0 contract. The latter protocol remains candidate and scoring-prohibited.

### 4.2 Exploratory documentary application

The Ofqual development application examines the 17 August 2020 change to England's summer grading rule, with a declared 18–20 August follow-up. Six public documents were selected in a [plan committed before the new findings](../research/strengthening/solo-002-complete/plan.md). Prior exposure and the enlargement of an earlier announcement-only packet are disclosed. This is an exploratory automation-boundary case: statistical standardisation is not represented as established machine learning. The author accepted its use as a bounded example; that scope decision does not accept the proposed scores.

The [Chair's statement](https://www.gov.uk/government/news/statement-from-roger-taylor-chair-ofqual) announces the change and states reasons. Later [Ofqual reporting, §2.3](https://www.gov.uk/government/publications/ofquals-regulatory-burden-statement/regulatory-burden-statement-april-2021) describes requirements imposed on exam boards. [Withdrawn government guidance](https://www.gov.uk/government/publications/coronavirus-covid-19-cancellation-of-gcses-as-and-a-levels-in-2020/coronavirus-covid-19-cancellation-of-gcses-as-and-a-levels-in-2020) reports replacement results while retaining exclusions and progression constraints. The [ledger](../research/strengthening/solo-002-complete/source-ledger.md) records current-copy dates, later updates, source dependence and missing internal records. These materials report institutional actions; they do not independently verify each candidate's receipt of a remedy.

The [additive author record](../research/strengthening/solo-002-author-review.json) accepts Judgment `2` on the public account, Command, Correction and Reform `2` for the bounded regulatory act and reported follow-through, and Repair `2` through operationally directed record correction. Both institutional-record integrity and assessment-packet integrity are accepted as `limited`. These collaborative, AI-assisted decisions retain missing internal deliberation, actor boundaries, exclusions and unknown individual outcomes. They do not attest independent source re-reading or grant publication eligibility. Counsel remains unresolved between the original draft's `IE` and a formal-route interpretation of `1`; unresolved adjudication is not an accepted `IE` finding. The decisions concern the defined intervention, not the original system's merits or universal repair.

![Separate lanes distinguish the 17 August Ofqual intervention and reported 19–20 August issue from the dates of institutional publications and updates. Counsel remains unresolved; Repair concerns operational direction.](../figures/development-2026-10-08/ofqual-actor-time.png)

Figure 2. Event timing and source timing are separate. The accounts report institutional follow-through, without independently establishing each recipient's outcome. Equal spacing indicates sequence, not elapsed time. [Vector figure and source-qualified data](../figures/development-2026-10-08/README.md).

A capable structured-review baseline uses the same sources and questions, including actor, period, counterevidence and uncertainty. The same assistant prepared both outputs with knowledge of the HIT draft. The [comparison](../research/strengthening/solo-002-complete/baseline-and-review.md) proposes ties; the author requested examination of a missed distinction or loss rather than accepting that outcome. The comparison remains unresolved, with no demonstrated equivalence, comparative accuracy or measured effort benefit. Four retained qualitative source-subset and attribution conditions inspect source dependence; they are within-assistant analyses, not independent rescoring or a statistical sensitivity study.

The [comparison challenge](../research/strengthening/solo-002-comparison-challenge.md) identifies a category-only projection that omits Counsel's `IE`/`1` alternative and Repair's direction-versus-delivery route, although the full rationales retain both. This is a restricted-summary omission, not demonstrated inferiority of the full method. The baseline also reuses HIT's evidence catalog; comparative burden remains unmeasured.

![A matrix shows that a specified five-field projection omits the Counsel alternative and Repair route. The full record retains them; the baseline retains the underlying distinctions in prose.](../figures/development-2026-10-08/qualification-preservation.png)

Figure 3. Qualification preservation depends on the representation supplied to the reader. Baseline Q2 retains the formal-route/access distinction but does not itself assign a HIT category. This is an inspection of two qualifications, not a reader-performance result or an accepted overall comparison. [Vector figure, exact projection and locators](../figures/development-2026-10-08/README.md).

A separately frozen [extension](../research/strengthening/solo-002-extension/report.md) records the three remaining argument reanalyses. The earlier-date condition withholds later exercise from 16 August while retaining the possibility of retrospective evidence about earlier harm. A synthetic denial leaves one AS/A delivery event unresolved without negating regulatory direction or the distinct GCSE account. Reordering and reformatting nine retained passages produced no identified substantive change while the original 23-claim, six-source argument remained available. All eighteen paired answers are proposed ties pending author review. No replacement scores, new institutional facts or independent robustness result follow. No new evaluation API or Jev request occurred; the analyses were nevertheless AI-assistant reasoning. They remain separate from the earlier model probes and preserved four-condition report.

### 4.3 Model-development records

Three single-request runs used `jev-1.13.0`. Their committed designs, inputs, responses and replay outputs remain separate:

| Run | Recorded observation | Inference limit |
| :--- | :--- | :--- |
| [Repository claim screen](../research/strengthening/jev-report.md) | Eight of eight classifications matched assistant-authored expectations. | Exposed development statements; no independent reference judgments. |
| [Constructed passage experiment](../research/strengthening/passage-report.md) | Nine of ten matched; one date interpretation remains disputed. | Frozen mismatch retained, not declared a proven model error. |
| [Ofqual advisory screen](../research/strengthening/jev-review-001/report.md) | Fourteen valid responses; six existing propositions classified supported; three paired conditions showed their declared relations. | No human reference labels or pooled accuracy estimate; scope-probe interpretations remain contestable. |

The last run used extracts from four of the six Ofqual sources. It classified broader access and deliberation claims as insufficient, and direct-operation and universal-remedy claims as contradicted. The contributing assistant retains reservations about the latter classifications. The model supplied choices, not explanatory rationales. No run changed a HIT finding, measured human effort, supplied independent evidence or established general robustness. Later author judgments cannot serve as pre-model labels after exposure to these results.

### 4.4 Controlled evidence-update representation rehearsal

The [HIT-EU-001 protocol and report](../research/strengthening/evidence-update-001/report.md) test explicitly constructed evidence changes, not historical HIT findings. A HIT-inspired typed graph and a capable structured table contain the same eight propositions and evidence/qualification links. Five noncumulative scenarios supply an unchanged control, source withdrawal, a corrected event date, an equally admissible contrary account and receipts for five named candidates. All actors, sources and 2040 dates are synthetic. The design, oracle and scorer were committed and pushed before two fresh assistant contexts received one packet each. Neither was intentionally supplied the oracle or other response; access restrictions were voluntary, not guaranteed blinding.

Each retained first response identified all four affected propositions and made no unnecessary substantive revisions among 36 unchanged opportunities. Each matched 40 of 40 documentary-state labels, 35 of 35 qualification enums and both narrow date/recipient-token checks. No scored outcome distinguished the representations. These counts describe dependent decisions within one small packet, not independent observations or an accuracy estimate for institutional use. One pass per representation cannot demonstrate equivalence or isolate a representation effect.

The task explicitly states its changes and supplies the relevant relationships. Full agreement may reflect an easy task. It supports neither graph superiority nor reduced effort; accompanying prose still requires author review. The reusable output is a frozen comparison task with actual first responses and offline replay. It adds no new Ofqual evidence, normative finding or human performance result, and does not settle the earlier documentary comparison. No exact serving-model identifier was exposed to the executors, which further limits model-specific reproducibility claims.

## 5. Reproducibility and research governance

The [v0.6.6 software archive](https://doi.org/10.5281/zenodo.23226713) identifies a released artifact; later advisory records and this draft require their own Git revision. Archival publication does not accept a scientific interpretation. The normative contract, conformance engine, historical human result and current development work retain separate versions.

Readers can check the historical audit, draft-record boundaries and advisory replay without making a new model request:

```sh
python scripts/run_research_integrity_audit.py --check
python scripts/validate_claim_bindings.py --check
python scripts/validate_solo_complete.py --check
python scripts/run_jev_review.py --analyze research/strengthening/jev-review-001/run-001
python scripts/run_evidence_update_benchmark.py --analyze
python scripts/render_development_figures.py --check
```

The [workflow](../.github/workflows/validate.yml) pins the validation environment and lists further checks. The [development exhibits](../figures/development-2026-10-08/README.md) retain their figure data, source bindings, vector outputs and previews. The artifact check verifies retained bytes; the separate rendering check regenerates the SVGs. The v0.6.5 claim-gate figure remains historical and does not depict approval of this draft. Deterministic replay reconstructs outputs from retained inputs; it is not a fresh inference or an independent reproduction. Hashes identify bytes, not historical authenticity or evidential truth. No private API credential is required to inspect the published record.

## 6. Limits and next evaluation

Public-source selection, institutional self-reporting, retrospective publication and missing internal records constrain the documentary example. Shared authorship, rubric familiarity and model-output exposure constrain its comparison. The six dimensions remain proposed operational constructs; neither their necessity nor their sufficiency has been demonstrated. A high finding does not establish fairness, legitimacy, legal conformity or reduced harm.

The next useful test should ask whether HIT changes a consequential assessment decision beyond a capable baseline. The synthetic rehearsal in §4.4 does not answer that question; repeating its highly cued task would not supply the missing user evidence. A prospective design would specify sources, questions, reference judgments and treatment of disagreements before model exposure, then retain all outcomes, including ties and losses. Author judgments would be author-referenced evidence, not independent ground truth. Claims about other users, institutions or comparative effort require evidence from those settings. Current-contract human replication and the independent implementation audit remain separate unresolved obligations. No U.S. or EU regulatory testing-programme participation is documented for this work.

## 7. Declarations and conclusion

Codex assisted with retrieval, code, proposed interpretations, methodological critique and prose; Jev supplied the recorded classifications. Neither system is an author or independent reviewer. The responsible author must verify substantive claims and approve the exact draft before preprint publication or submission. Availability of this working repository draft is not that approval. Funding, competing interests, author contributions and venue-specific ethics statements remain for explicit confirmation; this draft supplies no invented attestation. The documentary work uses public institutional material and adds no new participant recruitment; it does not claim an ethics exemption.

HIT presently contributes an open, executable representation that makes documentary judgments and their limits available for inspection. The bounded human result and development records show what has been done, while the unresolved comparisons identify what has not been established. That distinction permits a methods/resource contribution without claiming validated measurement, superior assessment or operational effectiveness.
