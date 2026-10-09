# Reopened comparison: candidate distinctions and losses

8 October 2026, America/New_York. Status: assistant analysis pending author review. In response to AD6, the author requested identification of a missed distinction or loss. That request accepts neither the proposed tie nor a particular scientific loss. The [author-review record](solo-002-author-review.json) records the disposition separately. The original [comparison](solo-002-complete/baseline-and-review.md) and [extension results](solo-002-extension/results.json) remain unchanged as earlier proposals.

The strongest observed limitation concerns which part of HIT a reader receives. A category-only view omits distinctions preserved in both the complete record and the capable baseline. This does not establish that the complete HIT method loses those distinctions.

## 1. Category projection omits interpretive alternatives and remedy routes

Observation: the Counsel entry has one `finding`, IE, and one `evidence_state`, indeterminate. Its rationale separately preserves the alternative of 1 if the seasonal advice route establishes applicable formal presence. The baseline's Q2 states that an advice route existed while event-specific access remains unresolved. The unresolved author decision does not accept either category. Evidence: [assessment](solo-002-complete/assessment.draft.json), `substantive_findings[0]`, especially `finding`, `unresolved_proposition` and `rationale`; [baseline](solo-002-complete/baseline-and-review.md), Q2 and the Counsel comparison row; [specification](../../SPECIFICATION.md), section 6.1.

Observation: Repair has `finding: 2`, `evidence_state: observed_exercise` and `repair_trigger: triggered`. Those fields do not distinguish delivered remedy from operationally directed remedy. Its `unresolved_proposition` is null, although the rationale, missing-artifact request and limiting claims preserve unknown individual outcomes. Baseline Q4 expressly distinguishes directed record correction from full repair. Evidence: assessment `substantive_findings[4]`; baseline Q4; specification 6.5. The [schema](../../schema/hit-assessment.schema.json), `$defs.finding`, provides rationale and evidence-reference fields but no dedicated remedy-route or alternative-category field.

The inspected comparison unit here is explicitly the projection containing `dimension`, `finding`, `evidence_state`, `repair_trigger` and `unresolved_proposition`. The preservation criterion is whether that projection itself carries the stated Counsel alternative and Repair route. It does not. This is a descriptive omission in that restricted projection, not evidence that a reader actually made an error or that the complete assessment is inferior. The full record retains the qualifications in prose and references. A proposed loss in reader comprehension would require a defined reading task, comparable presentations and observed answers; none is supplied here.

## 2. Typed evidence routes differ from unique substantive insight

Observation: the schema gives supporting, contradicting and limiting claims separate arrays. The draft uses limiting claims for appeal restrictions, excluded candidates and admissions contingencies; all six contradicting-claim arrays are empty. The baseline already retains these limits and names the corresponding evidence IDs in Q3 and Q4. Evidence: assessment `substantive_findings[2]` through `[4]`; baseline Q3–Q5; schema `$defs.finding.properties`.

HIT therefore supplies an explicit machine-readable relation structure in this artifact. The present comparison does not show that HIT discovered counterevidence the capable baseline missed. Nor does an empty contradiction array establish absence of conflicting evidence in the world. The later synthetic-conflict condition is a disclosed reasoning exercise, not a recovered historical contradiction or a test of independent analysts' detection rates. Whether typed references reduce omission or misclassification remains a hypothesis requiring observed errors under a defined task.

## 3. The baseline shares HIT's evidence infrastructure

Observation: baseline Q1–Q4 cite the draft's EC identifiers, and the comparison introduction states that the baseline was written with knowledge of the HIT draft. Its prose can express the same actor, date, source-limit and evidence-request distinctions partly through this shared catalog. The full HIT record additionally carries 23 evidence claims, six substantive finding entries, two integrity components and their derivation. Evidence: baseline introduction and Q1–Q4; assessment `evidence_claims`, `substantive_findings` and `telemetry_integrity`; schema `$defs.telemetryIntegrity`.

These artifacts show different representations of a shared analysis. Counting the baseline table alone as its whole payload would omit its linked evidence infrastructure. Counting HIT's full record against that table would compare different units. No authoring time, reading time, maintenance effort or error burden was measured. Greater record complexity may impose work; reuse and checking may offset it. Neither proposition is established by file size, field count or this same-assistant comparison.

## Disposition for the author

AD6 should remain unresolved while these candidates are reviewed. The proposed ties describe earlier same-assistant substantive answers, not accepted equivalence between independent workflows. The category-projection omission is inspectable; its practical consequences and the net burden of the complete record remain untested.

Before declaring a comparative loss or advantage, specify the unit being compared, the decision-relevant criterion, the evidence required to meet it and the permitted conclusion. For this case, the smallest concrete criterion is preservation of the Counsel alternative and Repair route in the presentation supplied to a reader. This note identifies that candidate; it records no new reader study, accepted loss, schema amendment or release credit.
