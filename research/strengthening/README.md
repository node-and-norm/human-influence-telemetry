# Research strengthening workbench

This supplementary workbench tests the usefulness and limits of HIT. It is development work following v0.6.5, with no new release or research-maturity decision. The submitted chapter is outside its scope.

The author approved the [bounded v1 execution priorities](v1-priorities.md) on 7 October 2026. The existing scientific decision queue remains in force. The [Ofqual complete-record extension](solo-002-complete/README.md) now includes a draft that passes executable conformance checks, a capable-baseline comparison and four qualitative source-subset/attribution reanalyses. Its plan was committed before new dimension findings. All scientific judgments remain AI-assisted proposals pending author adjudication.

Use the [evaluation-methods register](evaluation-methods.md) to distinguish software verification, documentary review, exploratory comparisons, and the independent evaluations that remain pending. Passing a software check does not validate HIT's scientific claims.

See the [five-priority disposition and author decision queue](priority-status.md) for the current completion boundary. The [passage experiment](passage-report.md) retained one disagreement across ten model judgments. The [closest-method challenge](closest-methods.md) examines overlaps with audit and assurance-case methods. These supplementary findings have no automatic publication approval under the v0.6.5 claim gates.

| Priority | Deliverable | Evidence available |
|---|---|---|
| 1. Claim audit | [Findings and dispositions](claim-audit.md), machine-readable [register](claim-audit.json) | Repository observations and proposed interpretation limits; human adjudication pending |
| 2. Closest literature | [Comparison and search record](literature-review.md) | Targeted source review; systematic coverage and independent novelty review pending |
| 3. Adversarial tests | [Protocol](adversarial-protocol.md), [cases](adversarial-cases.json), generated [results](results.json); [conditional sensitivity checks](solo-001/results.json) | Deterministic tests of supplied facts; no validated document-to-finding pipeline |
| 4. Analytical usefulness | [Primary solo evaluation](solo-evaluation.md); [first documentary application](solo-001/dossier.md); [two further applications](solo-bc.md); [deferred participant extension](utility-protocol.md) | Three partial comparisons propose ties with structured review; author adjudication and full operational assessments remain pending |
| 5. External evaluation | [Reviewer packet](external-review.md), [response template](review-response.template.json) | Optional extension; no external review claimed |

Run `python scripts/validate_research_strengthening.py --check` from the repository root. Use `--write` to regenerate the result after reviewing changes to inputs. Neither command calls an AI service. Results include hashes of inputs and the existing rubric implementation. CI verifies reproducibility and rejects unsupported promotions in this workbench.

The 0.4.0 contract, 0.5.0 conformance engine, historical applications, 0.6.0 human result, and v0.6.5 archive remain preserved. Current-contract external-rater replication under HIT-IRP-HIT040-002 remains unresolved; its recruitment and scoring gates still apply. This package does not authorize participant recruitment under that protocol.

The candidate contribution is a reproducible representation of documentary judgments about practical authority, with explicit uncertainty and actor/period boundaries. Whether this representation improves assessment is an open empirical question. High findings do not establish a fair decision, lower harm, or legitimate authority.

## First documentary application

The [five-candidate inventory and selection freeze](solo-series.md) retains three partial applications. The [Ofqual and Robodebt dossiers](solo-bc.md) extend the first audit with announcement and recommendation boundaries. Their source packets do not establish operational delivery. All comparison judgments require author adjudication; full documentary sensitivity and invariance tests remain incomplete. The [E5 writing rules](e5-writing.md) apply the author's supplied packet to this workbench.

The [Obermeyer development audit](solo-001/dossier.md) proposes two rationale qualifications and an overcorrection warning. Its matched structured-review comparison proposes a tie. Six conditional software checks accompany it; they do not validate source interpretation. Case selection is recorded; author adjudication remains pending. Run `python scripts/validate_solo_application.py --check` to replay those checks. The [plan](solo-001/plan.md) discloses prior source exposure and the exploratory staging amendment.

## Completion criteria

The workbench preserves three partial documentary applications and two model experiments, and now adds one exploratory complete-record draft with qualitative reanalysis. Its publication path still requires responsible-author adjudication, source and literature verification, and the unfinished evaluation conditions. Claims about other users require participant evidence; independent-review claims require external records. Each result must state which criterion it satisfies. Repository size, test count, and model agreement are not proxies for field validity.

## Assistance and provenance

Prepared with Codex assistance on 2026-10-03, starting from main commit `74558075da0e6a8bc0c25357dac27f4428bede9e`. The user authorized implementation of five repository priorities and reuse of the existing private Jev credential. AI assistance covered repository inspection, targeted literature retrieval, proposed judgments, code, and prose. Human scientific adjudication is pending; user authorization is not recorded as agreement with each finding. No new human ratings or institutional records were produced. Two Jev requests returned eight and ten advisory judgments after their respective designs were committed. See the [first pilot report](jev-report.md) and [passage experiment report](passage-report.md).
