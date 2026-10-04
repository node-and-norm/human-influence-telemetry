# Obermeyer documentary audit: proposed findings

HIT-SOLO-001-A. Exploratory assistant analysis under [the recorded plan](plan.md). Responsible-author adjudication is pending. No replacement scores are issued. This is a partial documentary application, not a complete assessment accepted by the conformance engine.

## Source ledger

| ID | Source and locator | Bounded source observation |
|---|---|---|
| O1a | [Obermeyer et al.](https://www.ftc.gov/system/files/documents/public_events/1548288/privacycon-2020-ziad_obermeyer.pdf), printed p.448, Data and analytic strategy; p.452, Relation to human judgment | Clinicians received contextual record and claims information and considered enrollment after algorithmic screening. |
| O1b | Same article, p.452, Relation to human judgment and Table 3 | The analysis compares observed enrollment with simulated alternatives; it does not provide individual clinical reasoning records. |
| O1c | Same article, p.453, Discussion, paragraphs beginning After completing and To resolve | The authors describe manufacturer replication and collaborative label experiments. The reported bias reduction concerns those experiments; rollout is a future goal. |
| O2 | [DFS/DOH letter](https://www.dfs.ny.gov/reports_and_publications/comment_letters/dfs-doh-joint-letter-uhgi-20191025), 25 October 2019, opening and demand paragraphs; footnote 1 | The agencies identify Impact Pro and demand investigation or cessation if nondiscrimination cannot be demonstrated. Their account of the study cites O1. |

Accessed 2026-10-04 UTC. O1a–c are passages from one paper, not independent studies. O2 independently documents a regulatory demand, not independent verification of implementation or the study's statistical results. The article does not name the manufacturer; product attribution relies on O2. Only citations and brief paraphrases are redistributed. No raw patient data were accessed and no effect estimate was recomputed.

## Matched analytical comparison

Both columns use the source ledger above. They are assistant-proposed interpretations, not independent observations. Each row retains the period and actor in the plan. Missing evidence is not affirmative evidence of absent capacity.

| Question | Capable structured review | HIT mapping | Comparison |
|---|---|---|---|
| What evidence access is documented for the studied hospital's clinicians? | O1a is positive evidence against a blanket claim that reviewer information is undescribed. Request the actual evidence packet, access conditions, and timing before claiming completeness. | Counsel / FR-04: distinguish documented contextual access from verified sufficiency of underlying evidence. No full dimension score is assigned. | Tie on the substantive distinction and next request. HIT adds a standardized category and rule reference. |
| Is independent clinical reasoning established? | O1b does not identify individual reasons or disagreements. Conversely, missing rationales do not show ceremonial review. Request reasoning and exception records. | Judgment / FR-05: neither direct independent reasoning nor the specified evidence for ceremonial review has been demonstrated here. | Tie. Both retain uncertainty without conflating it with ineffective oversight. |
| Was manufacturer reform operational by the cutoff? | O1c supports technical development; it does not establish deployment in the assessed workflow. O2 is a demand, not a completion record. Request a dated release, implementation owner, workflow change, and adoption record. | Reform / FR-09: operative change is a material unresolved predicate for a deployment-bound finding. A development-process assessment would need its own boundary and evidence. | Tie. HIT names the unresolved predicate; it does not supply the missing evidence. |

The comparison demonstrates no unique substantive advantage over this capable baseline. Machine-readable categories may aid reuse, but this application does not measure that benefit. Shared authorship, rubric familiarity, and deliberate matching favor agreement. Three rows are three questions in one known packet, not three independent cases.

## Proposed claim-audit dispositions

**SOLO-A-01, rationale correction needed.** In case-studies/obermeyer.md, the Counsel rationale says the study does not describe reviewer evidence. O1a requires a narrower account. Preserve the historical IE finding as historical, but do not reuse its rationale unchanged in a current-contract assessment. Proposed replacement explanation for a future additive correction: contextual access is described; sufficiency, completeness, and actual access conditions remain to be established. This correction does not entail Counsel 2.

**SOLO-A-02, scope qualification needed.** The historical manufacturer Reform 2 and its statement that no further record is required must not be presented as proof of deployed institutional reform. Technical development and operational deployment are different assessment objects. A development-bound interpretation may be defensible under the historical method, but that does not settle a current-contract deployment-bound claim. Preserve the original score, record this objection, and require a new bounded assessment before reuse. This audit does not establish that rollout never occurred.

**SOLO-A-03, avoid overcorrection.** Do not replace the historical deployer profile with a positive profile merely because the paper discusses doctors. The historical Judgment rationale is narrower than an assertion of no clinician involvement and need not be declared false. Role, available information, individual reasoning, override authority, and actual intervention are distinct propositions. The paper's hospital is not every deploying institution.

## Sensitivity, lineage, and ablation

The [conditional rule cases](cases.json) remove supplied evidence predicates and retain the expected distinction between IE, formal presence, and operative capacity. These are software checks, not documentary extraction tests. The generated results identify every case and its outcome.

Qualitative checks, not executed semantic experiments: substituting manufacturer evidence for hospital authority would change the actor; duplicating O1 through a regulatory citation would not add an independent implementation record. Removing actor or time fields would conceal those errors, but a capable baseline already retains those fields. No incremental benefit is established by that ablation argument alone. No conflicting primary record, paraphrase stability experiment, or blinded interpretation test was conducted.

## Review gate and next evidence

The author needs to accept, revise, or reject SOLO-A-01 through SOLO-A-03 with reasons. Authorization to perform this work is not that adjudication. Until then these are proposed audit findings, not accepted corrections or publication-ready conclusions. Historical files remain unchanged. The protected external-rater replication remains unresolved.

The next empirical step is to finish the capped feasibility inventory, select the remaining documentary applications before their assessment, and preserve unfavorable outcomes. This one application supports the value of checking HIT against its own sources. It does not validate HIT as a measurement instrument, establish novelty, or show improved institutional outcomes.
