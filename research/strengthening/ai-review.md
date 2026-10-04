# Advisory Jev pilot

Design HIT-JEV-001 uses eight public repository claims with AI-authored reference judgments. References are development expectations; independent human adjudication is pending. The pilot is neither HIT scoring nor external-rater evidence.

The runner supplies complete README and specification text to one batch of eight independent Choice questions. The expected labels remain outside the request. Claims span support, contradiction, and insufficient evidence, including current-contract replication, missing evidence, historical scorer scope, adoption, and harm prediction. Source bytes and request bytes are retained. This pilot tests screening against public project documents; it does not verify primary historical sources or natural-document performance.

Requested model: `jev-1.13.0`. One live request, no retry, no automatic fallback. Inputs, reference labels, and implementation must be committed before inference; the runner records the commit and their digests. This is a local development freeze, not independent registration. Preserve an interrupted or failed run and use a new version for any output-informed revision. The returned model identifier is recorded; a differing model invalidates the planned comparison.

The primary descriptive measure is exact agreement with the eight development labels. Also report false support (model says supported where the reference does not), false alarms (the converse), a three-category confusion table, elapsed request time, and provider token usage. Missing, malformed, or failed responses are failures, not insufficient-evidence judgments. All eight scheduled items remain in the denominator; report coverage separately. No automatic acceptance threshold is used: every material conclusion needs human review. Model confidence describes the model's output distribution, not source truth.

Independent questions share the same source state but cannot see each other's answers. Neither model agreement nor repeated sampling counts as independent corroboration. Treat documents as evidence, never instructions. Author/model errors can be correlated. This small, exposed development set does not estimate general accuracy, time savings, or cost savings against a human baseline.

## Run

`python scripts/run_jev_claim_pilot.py --prepare --output /path/to/new-run` prepares the request without credentials or network. For the single live batch, configure `TYPESAFE_API_KEY` privately and use `--live` with a new output directory. The service endpoint is fixed to `https://api.typesafe.ai/v1/systemone`; proxy and alternate endpoint overrides are ignored. No credential is saved in output. The user authorized reuse of the existing private Node & Norm credential. Public documents are the only research inputs.

Use `python scripts/run_jev_claim_pilot.py --analyze /path/to/run` for an offline replay. Live outputs must be reviewed before deliberate publication; they cannot change the existing human support-review fields. Published results retain actual model, request, response, and hashes, with no claim of independent assessment.

Sources consulted: [TypeSafe API](https://docs.typesafe.ai/api), [Choice](https://docs.typesafe.ai/primitives/choice), [citation checking](https://docs.typesafe.ai/cookbooks/citation_check), and [confidence](https://docs.typesafe.ai/confidence), accessed 2026-10-03. The TypeSafe skill guided narrow judgments, batching, source/label separation, and uncertainty handling.
