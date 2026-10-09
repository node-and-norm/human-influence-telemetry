# Jev advisory source-scope rehearsal

Status: one live advisory batch completed on 7 October 2026, America/New_York. All fourteen responses passed structural checks and remain pending human review. Read the [results and review queue](report.md) and [retained run record](run-001/run.json). The author authorized this bounded use of Jev for [v1 priorities two and three](../v1-priorities.md); it does not produce accepted HIT findings.

Read the [protocol](PROTOCOL.md), [source record](sources.md) and [design](design.json) before interpreting a run. Four official documents supply nine attributed excerpts. The fourteen questions comprise six unchanged draft propositions, four constructed scope probes and four constructed items covering period, conflict and whitespace conditions. Every answer remains advisory. No author reference labels, accuracy statistics or confidence-based approvals are supplied.

## Use and reproduce

Use Python 3.12 or later from the repository root. Offline tests need no API key or network access:

```sh
python -W error scripts/test_jev_review.py
python scripts/run_jev_review.py --analyze research/strengthening/jev-review-001/run-001
python scripts/run_jev_review.py --prepare --output /tmp/hit-jev-review-prepared
python scripts/run_jev_review.py --analyze /tmp/hit-jev-review-prepared
```

Choose a new output directory if that example path exists. Preparation retains the inputs and request, with every item marked not run. The script never overwrites an existing bundle. The source retrieval script is separate and requires network access; it is not part of offline verification.

A live attempt additionally requires the exact design, sources, protocol, runner and protected files to be committed, authorized use of the TypeSafe account and a privately supplied `TYPESAFE_API_KEY` environment variable. Do not paste a key into a command, repository file, issue or research record.

```sh
python scripts/run_jev_review.py --live --output /tmp/hit-jev-review-run-001
python scripts/run_jev_review.py --analyze /tmp/hit-jev-review-run-001
```

The live command sends one batch to the fixed TypeSafe endpoint using `jev-1.13.0`; it does not retry. The authorized batch is already complete: these instructions document execution, not authorization for another call. A failed or interrupted attempt must be retained, not replaced. Review and document any amendment before another attempt. Request latency is recorded only as a transport observation, not a measure of researcher effort.

The bundle retains exact request and successful-response bytes, frozen input copies, protected-file copies, hashes, commit, usage and technical status. Replay reconstructs the request and derived analysis offline. Hashes and replay verify consistency of the retained record; they do not authenticate source truth or independently prove that a provider made a response. Raw HTTP error bodies and exception messages are excluded to avoid retaining credentials or private error details.

## What remains for the author

The [six existing author decisions](../solo-002-complete/baseline-and-review.md#author-decision-bundle) stay pending. This screen may inform AD2–AD5; it cannot determine AD1's case suitability or AD6's contribution judgment.

Pre-run review identified two wording questions in the unchanged natural claims: whether the described advice route warrants “informed” in N01, and whether the reported admissions contingency warrants “permits” in N06. These are review questions, not established errors. B03 and B04 have no adjudicated reference choosing between insufficient and contradicted. Keep the model response, the assistant's interpretation and the author's eventual judgment distinct.

Methodological review corrected P02 before inference. A denial of the grade-issue event does not contradict the proposition that guidance reports that event. The revised pair uses the same unqualified event proposition in P02-base and P02, with the synthetic denial added only to P02. All six original draft propositions remain unchanged.

The [source record](sources.md#locator-qualifications) also records two paragraph-number differences between this retrieval and the existing draft locators. Exact section and passage text identify the intended statements; no historical assessment file is silently corrected.

Source-subset analysis, full-record qualitative reanalysis, author adjudication, current-contract external-rater replication and stable-release gates remain separate. The original assessment, scores, review status, historical Jev pilots and published DOI metadata are protected inputs, not outputs of this workflow. This rehearsal does not demonstrate independent validation, generalization, institutional benefit or savings in review effort.

## Assistance

Codex and contributing software agents prepared the sources, questions, implementation, tests and prose on 7 October 2026, America/New_York. The TypeSafe skill informed question isolation and structured-response handling; the testing and documentation skills informed failure checks and reproducibility instructions. E5 review preserves actors, dates, attribution and uncertainty. None of those procedures constitutes scientific acceptance.
