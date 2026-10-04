# Passage test: one unresolved date judgment

Jev matched nine of ten frozen development expectations in one request. It classified P06 as contradicted where the reference label was insufficient. All ten answers were valid. The retained [analysis](jev-live-002/analysis.json), [request](jev-live-002/request.json), [response](jev-live-002/response.json), and [run record](jev-live-002/run.json) permit offline replay.

The requested and returned model was jev-1.13.0. The design was committed at d8316d928fa61d59ca9e594f7d3764b9e92e2540 before inference. The request ran on 3 October 2026 in America/New_York; the record uses UTC timestamps. The provider reported 2,201 input tokens and 451 output tokens. Measured request time was approximately 0.360 seconds. No retry occurred, and no human time or monetary saving was measured.

| Condition | Expected | Observed |
|---|---|---|
| P01: base passage | supported | supported |
| P02: remove decision evidence | insufficient | insufficient |
| P03: paraphrase | supported | supported |
| P04: reverse sentence order | supported | supported |
| P05: substitute actor | insufficient | insufficient |
| P06: substitute date | insufficient | contradicted |
| P07: add unresolved conflict | insufficient | insufficient |
| P08: duplicate passage | supported | supported |
| P09: claim completed delivery | insufficient | insufficient |
| P10: negate announced decision | contradicted | contradicted |

The three declared invariance relations, P03/P01, P04/P01, and P08/P01, held. No false-support response occurred. These counts describe constructed passages; they do not estimate accuracy on historical documents or HIT assessments.

## Interpret the disagreement before changing anything

P06 states that an announcement occurred on 18 August and asks about 17 August. The reference uses an open-world reading: an event on the 18th does not exclude another event on the 17th. The model's answer may reflect an assumption that the two dates identify the same unique event. The response contains no explanation, so that account remains an inference. Its reported confidence of 0.97 does not settle the interpretation.

Retain the mismatch and original reference. Author adjudication should decide whether the task's event identity was sufficiently explicit. A revised task that specifies uniqueness would be a new experiment, not a correction to this result. The finding supports manual review of date-based contradiction labels in this workflow; it does not establish a general model defect.

The TypeSafe skill guided isolated questions and typed response validation. The inputs were assistant-authored summaries and fictional perturbations. This experiment advances passage-level sensitivity testing; full-document extraction, source selection, HIT category inference, and human reliability remain untested by it.
