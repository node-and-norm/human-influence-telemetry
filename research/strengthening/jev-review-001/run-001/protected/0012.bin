# Human Influence Telemetry Specification

**Status:** Released pre-1.0 normative contract  
**Version:** 0.4.0  
**Released:** 2026-07-18  
**Predecessor:** 0.1.0  
**Stable target:** 1.0.0, gated candidate  
**Author:** Mark Julius Banasihan  
**ORCID:** 0009-0001-8121-2878  
**Originating concept DOI:** 10.5281/zenodo.21204892  
**Current repository research maturity:** Level 2, Applicable

The normative body below is unchanged from release `0.4.0`. The `1.0.0` readiness program does not alter scoring semantics until a separately reviewed stable-contract promotion is completed.

## 1. Purpose

Human Influence Telemetry (HIT) is a documentary assurance method for evaluating whether formal human oversight retained practical force in an AI-mediated institutional decision process.

HIT evaluates what observable, time-bounded records establish about human access, judgment, authority, correction, repair, and reform. It does not infer unrecorded intention, evaluate model quality, certify legal compliance, determine whether an outcome was substantively correct, or enforce agent actions at runtime.

## 2. Unit of analysis

The unit of analysis is one defined decision process, within one identified institutional unit, over one bounded period or one explicitly declared event.

Before evidence review begins, the assessment must declare:

- institutional unit and decision process;
- AI-system role and stated human role;
- period or event boundary and any follow-up period;
- population or record universe;
- sampling and aggregation rules;
- material actors and authority relationships;
- known exclusions and likely selection effects.

A boundary may be revised only when the change, reason, timing, and effect are recorded.

## 3. System and terminology boundary

### 3.1 Documentary telemetry

In HIT, telemetry means observable, time-bounded documentary evidence that may reveal whether human influence existed and had practical force. It does not mean a runtime observability SDK, tracing system, event collector, agent middleware, policy engine, or enforcement layer.

### 3.2 HIT assessment record

A HIT assessment record contains six substantive findings, two Telemetry Integrity component findings, one derived overall integrity status, actor attribution, evidence propositions, assessment boundaries, limitations, and unresolved propositions.

A HIT assessment record is not a runtime policy decision, Governed Decision Record, signed receipt, compliance determination, or DEAS evidence-applicability determination.

### 3.3 Assessment-contract conformance

Structural conformance means that a record validates against the declared HIT schema version. Substantive conformance additionally requires application of this rubric, the actor-attribution rules, the sampling rule, the evidence-state sequence, the citation requirements, and the Telemetry Integrity procedure.

Structural validity does not establish substantive correctness, legal conformity, or empirical reliability.

## 4. Governing evidence states

Before assigning `0`, `1`, `2`, or `IE`, determine which evidence state is established.

### 4.1 Affirmative absence

Affirmative absence means the evidence supports the proposition that the relevant capacity, practice, authority, mechanism, or artifact did not exist during the bounded process.

It requires at least one of:

1. an explicit statement of nonexistence from a competent source responsible for the process;
2. a binding process design, system constraint, or authority instrument that made the capacity structurally unavailable;
3. a documented search across a defined and credibly complete record set that would ordinarily contain the artifact;
4. contemporaneous process evidence showing that the decision path excluded the capacity;
5. multiple mutually consistent records establishing nonexistence rather than merely omitting mention.

Documentary silence, an unanswered request, a missing file, or a generic process description does not by itself establish affirmative absence.

### 4.2 Formal presence

Formal presence means the capacity existed in the assessed process as an assigned role, required step, documented mechanism, or available channel.

It requires a process-specific artifact showing that the capacity was defined or assigned and applied to the assessed unit, decision type, and period. Generic job descriptions, enterprise policies, vendor statements, and undated authority claims are insufficient unless applicability is traceable.

### 4.3 Operational capability

Operational capability means a formally present capacity was usable in practice. It requires an applicable authority, usable mechanism, required access, workable timing, defined decision consequence, and no material barrier making use impracticable.

It may be shown by an operational test, drill, verified configuration, successful use in a comparable sampled decision, or other direct process evidence. Nominal permission alone is insufficient.

### 4.4 Observed exercise

Observed exercise means the human capacity was used in a documented instance and affected, interrupted, redirected, reconsidered, repaired, or reformed the decision path. The instance must remain attributable to the assessed actor and fall within the declared temporal and sampling boundaries.

### 4.5 Indeterminate

Indeterminate means the record cannot distinguish among affirmative absence, formal presence, operational capability, and observed exercise.

## 5. Findings

### 5.1 `0`: absent

Assign `0` only when affirmative absence is established. Do not assign `0` because records were not produced, a source is silent, the packet is incomplete, or an expected artifact was not found.

### 5.2 `1`: present but ceremonial

Assign `1` when formal presence is established and operational capability is not established, practical effect is affirmatively constrained, or the capacity operated only as ratification, intake, acknowledgment, routing, or another non-substantive form.

A `1` requires evidence that the form existed. Uncertainty about existence remains `IE`.

### 5.3 `2`: present and substantively exercised

Assign `2` when observed exercise affected the decision path, or when operational capability is directly demonstrated and the assessment design does not reasonably permit an observed exercise, provided that:

- a named authority could use the mechanism during the bounded period;
- the mechanism was technically and procedurally available;
- the decision consequence was identifiable;
- no material evidence shows that use was prohibitively difficult, routinely ignored, or controlled by another actor.

Mere legal authority, policy language, interface presence, or hypothetical capability does not support `2`. When evidence supports both `1` and `2`, use `1` unless the criteria for `2` are affirmatively established.

### 5.4 `IE`: insufficient evidence

Assign `IE` when the evidence cannot distinguish among the evidence states. Record the unresolved proposition, missing or conflicting artifact, search or request performed, and reason a determinate finding is unavailable.

`IE` is not ordinal and must not be averaged, converted to zero, or treated as evidence of failure.

## 6. Substantive dimensions

### 6.1 Counsel

**Question:** Did the named human authority have actual pre-decision access to relevant underlying evidence?

- `0`: the record establishes that relevant pre-decision access was unavailable.
- `1`: a formal route existed, but actual presentation or retrieval is not shown, or the human received only a compressed score, ranking, summary, or recommendation.
- `2`: records show actual, timely access to relevant underlying evidence sufficient to inform judgment.
- `IE`: permission, retrieval, timing, or scope cannot be determined.

Authorization and actual access must be recorded separately.

### 6.2 Judgment

**Question:** Did the human authority independently evaluate reasons, alternatives, uncertainty, and context?

Direct evidence includes reviewer-authored reasons, alternatives considered, disagreement, modification, questions, requests for additional evidence, or rationale not reducible to system output. Indirect indicators include review duration, adoption rate, boilerplate language, batch size, and repeated identical dispositions.

- `0`: no evaluation step existed, or the role was structurally prohibited from evaluating the merits.
- `1`: a formal review step existed, but the record shows ratification or ceremonial review. A `1` based mainly on indirect indicators requires at least two mutually reinforcing, process-specific indicators and no material contrary evidence.
- `2`: direct evidence shows independent reasoning capable of affecting the path.
- `IE`: the presence or substance of reasoning cannot be resolved.

### 6.3 Command

**Question:** Could a named human authority practically approve, reject, modify, stop, or escalate?

- `0`: no named authority could direct otherwise, or intervention was structurally unavailable.
- `1`: authority or a mechanism existed formally, but usability, timing, control, or practical consequence is not established, or material friction reduced the role to ratification.
- `2`: a named authority exercised the power, or a verified operational test shows the power could produce a specified change.
- `IE`: authority, mechanism availability, or practical control cannot be determined.

Vendor-controlled intervention must not be attributed to the assessed institution without evidence of delegation or control.

### 6.4 Correction

**Question:** Could the decision be contested, interrupted, reconsidered, modified, reversed, or appealed in practice?

Assess channel existence, accessibility, procedural use, substantive reconsideration, and practical outcome effect separately.

- `0`: no contest, appeal, interruption, or escalation channel existed.
- `1`: a channel existed, but the record shows only intake, routing, template disposition, or procedural acknowledgment.
- `2`: a documented instance or direct operational test shows substantive reconsideration and authority to alter the outcome.
- `IE`: existence, accessibility, use, or substantive effect cannot be determined.

A reversal is strong evidence but is not required when substantive reconsideration and practical authority are otherwise established.

### 6.5 Repair

**Question:** After qualifying harm, did a named actor own and deliver remediation to affected persons?

Determine the trigger before the finding:

- `triggered`: harm is established through adjudication, formal institutional acknowledgment, or specific contemporaneous evidence corroborated by an independent source or record class;
- `not_triggered`: the bounded record affirmatively establishes that no qualifying harm occurred;
- `indeterminate`: allegations or indicators exist, but qualifying harm cannot be established.

When the trigger is `indeterminate`, assign Repair `IE`.

When triggered:

- `0`: no named actor owned remediation, or repair was affirmatively excluded;
- `1`: a formal owner or process existed, but no practical remedy to affected persons is established, or only the process was corrected;
- `2`: a named actor delivered or operationally directed restitution, record correction, notification, restored access, or another remedy tied to the harm;
- `IE`: repair ownership or action cannot be determined.

When not triggered, standing capability may be evaluated only when capability testing was predeclared. Formal ownership supports at most `1`; `2` requires a tested or previously exercised mechanism. Otherwise use `IE` and state that no qualifying event occurred within the boundary.

### 6.6 Reform

**Question:** Did a named authority have and exercise power to change the decision architecture?

Later change is admissible only when a follow-up period was declared, the changed architecture is identifiable, the change is linked to the assessed failure or risk, and the implementing or authorizing actor is identified.

- `0`: no assessed actor held reform authority, or change was structurally impossible within that role.
- `1`: formal authority or a change process existed, but no operative architecture change is established.
- `2`: a named authority implemented or operationally directed a linked architecture change.
- `IE`: authority, linkage, timing, or implementation cannot be determined.

Externally compelled change supports `2` only when a named institutional authority substantively implemented, adapted, or extended it.

## 7. Telemetry Integrity

Assess two objects separately:

1. **institutional-record integrity:** records generated or retained by the institution and governed systems;
2. **assessment-packet integrity:** provenance, completeness, transformation history, and preservation of materials supplied to the assessor.

Each component receives:

- `adequate`: traceable provenance, disclosed scope, controlled edit authority, credible retention, sufficient independence or corroboration, and no unresolved material contradiction;
- `limited`: named gaps or dependencies exist, but bounded findings remain possible;
- `unreliable`: tampering, unexplained alteration, irreconcilable contradiction, circular dependence, compromised generation, or provenance failure makes the record unsafe;
- `IE`: information about provenance, completeness, edit authority, retention, independence, or transformation is insufficient to classify the component.

Derive the overall status deterministically: `unreliable` overrides `IE`; `IE` overrides `limited`; `limited` overrides `adequate`. Component statuses must remain visible.

Missing substantive records do not automatically make integrity `IE`; they may instead make a substantive dimension `IE`.

## 8. Sampling and aggregation

Unless another rule is declared before evidence review, period-level assessments report the dominant operational pattern. One exceptional exercise does not automatically elevate a period-level finding to `2`.

Event-specific assessments may report the event finding but must not generalize it to the institution or period without additional evidence.

Every assessment must state the record universe, selection rule, period, aggregation mode, exclusions, and likely selection effects.

## 9. Actor and authority attribution

Before findings are assigned, identify each material actor, institutional identity, role, authority type, mechanisms controlled, decision stages affected, evidence basis, and relationship to other actors.

Conduct, authority, evidence, and failure must not be attributed across institutional boundaries without evidence of delegation, control, agency, shared decision rights, or another defined relationship. Vendors, deployers, regulators, courts, affiliates, and individual professionals must be separated when their authorities differ.

A combined institutional finding is permitted only when the assessment explains why the actors form one decision architecture for the dimension being evaluated.

## 10. Contradictory evidence

Evaluate conflicting evidence by directness, contemporaneity, specificity, source competence, independence, corroboration, disclosed interest, procedural posture, internal consistency, and consistency with other record classes.

No source type is automatically controlling. A determinate finding is permitted when one account is materially better supported and the assessment explains why the conflict does not alter the result. Use `IE` when unresolved conflict could reasonably change the finding or actor attribution.

HIT evaluates support for its constructs; it does not adjudicate legal liability or ultimate credibility.

## 11. Evidence reuse and citation precision

One artifact may support multiple dimensions only through a distinct proposition and reasoning path for each use. Evidence establishing one dimension does not automatically establish another.

Every material evidence claim must include:

1. source and artifact identifiers;
2. page, paragraph, section, timestamp, event identifier, record identifier, line, or another reproducible locator;
3. a bounded proposition;
4. relation: `supports`, `contradicts`, or `limits`;
5. relevant dimensions and actors;
6. provenance, independence, and transformation history.

When no stable locator exists, identify the smallest reproducible unit and explain the limitation.

## 12. Conformance and migration

A conforming `0.4.0` assessment must validate against `schema/hit-assessment.schema.json` and satisfy this specification and `docs/application-handbook.md`.

Version `0.4.0` is a breaking change from `0.1.0`. Migration is a fresh reassessment, not a version-field replacement. Historical `0.1.0` files remain valid historical artifacts and must not be overwritten or represented as `0.4.0` records without reconstruction under the new contract.

The public migration dispositions are recorded in `case-studies/migrations/v0.4.0/migration-manifest.json`.

## 13. Adjacent systems and non-claims

Runtime governors may supply enforcement and audit records. Signed-receipt systems may supply integrity evidence. Credo AI may supply policy, control, workflow, and monitoring artifacts. GDI may supply Governed Decision Records. DEAS may qualify evidence applicability under external requirements.

HIT evaluates what those records establish about human influence. It does not inherit runtime enforcement, cryptographic verification, policy-pack harmonization, compliance automation, legal sufficiency, or evidence portability from adjacent systems.

A high HIT finding does not prove that a decision was correct, lawful, fair, accurate, harmless, or morally justified. HIT does not claim human inter-rater reliability, causal validity, certification, independent adoption, or that human involvement is always preferable to automation.

## 14. Version stability and research maturity

Semantic versions communicate the stability and compatibility of the public contract. Research maturity communicates the strength of evidence supporting HIT claims.

Release `0.4.0` remains Maturity Level 1. The locked human exercise remains the entry condition for H3 and Maturity Level 2. Its original submissions and pre-adjudication result must be published, passing or failing, under the next available repository version when completed.
