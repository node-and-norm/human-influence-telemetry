# Jev claim-screening development result

On 2026-10-03 America/New_York (2026-10-04 UTC), one request to `jev-1.13.0` returned eight valid judgments. All eight matched the AI-authored development expectations: three supported, three contradicted, and two insufficient. False support and false alarms were both zero relative to those expectations. Independent human adjudication remains pending.

The observed request duration was 0.376 seconds. Provider usage was 8,462 input tokens and 362 output tokens. Preparation, development, and human review time were not measured. No dollar cost or speed advantage over a human workflow is inferred.

The design, source documents, and runner were committed at `f2b24295411936ccde7dea12714ac9edeb7c424d` before inference. The single request used that design without sending expected labels. No retries, fallback, tuning, or discarded judgments occurred. The retained records are [request](jev-live-001/request.json), [raw response](jev-live-001/response.json), [run metadata](jev-live-001/run.json), and [analysis](jev-live-001/analysis.json). The request contains public repository text; it contains no API credential.

Reproduce the analysis without an API key:

```sh
python scripts/run_jev_claim_pilot.py --analyze research/strengthening/jev-live-001
```

This is an exposed development set with direct repository statements and deliberately unsupported numerical claims. It supplies little evidence about difficult paraphrases, incomplete institutional records, multilingual sources, or adversarial instructions. The expectations and questions share AI-assisted authorship, creating correlated-error risk. Eight matches do not establish general accuracy or independent validation of HIT. The next evaluation should use separately selected source passages and human reference judgments before expanding deployment.

Every material research judgment remains subject to source inspection and human adjudication. Current-contract human replication remains unresolved.
