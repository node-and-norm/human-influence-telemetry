# Verify HIT in a disposable clone

HIT's checks require Python 3.12, pinned dependencies and full Git history. Several validators inspect preserved commits. The complete workflow also prepares development artifacts. Use a fresh clone to isolate these write effects. [Continuous integration workflow](../.github/workflows/validate.yml), [benchmark preparation](../scripts/run_evidence_update_benchmark.py).

## Prepare the environment

Run this POSIX shell block from a directory where a new `hit-verification` folder may be created. The subshell stops on the first failure. Record the printed commit with the results. Use the branch or commit under review before running the checks.

```sh
(
  set -eu
  git clone https://github.com/node-and-norm/human-influence-telemetry.git hit-verification
  cd hit-verification
  git rev-parse HEAD
  python3.12 -m venv .venv
  . .venv/bin/activate
  python -m pip install --requirement requirements-dev.txt
  python -m src conformance --all
  python scripts/run_research_integrity_audit.py --check
  python scripts/validate_claim_bindings.py --check
  python -W error scripts/test_claim_bindings.py
  python scripts/validate_public_release_status.py
  python scripts/validate_closeout.py
  python -W error scripts/test_closeout.py
  git diff --exit-code
)
```

The dependency file pins `jsonschema[format]` 4.25.1 and PyYAML 6.0.3. Figure rendering uses the separate [pinned rendering stack](../requirements-figures.txt). [Core requirements](../requirements-dev.txt).

## Expected outcomes

| Check | Expected output | Meaning |
| :--- | :--- | :--- |
| Conformance suite | Successful aggregate exit with each fixture matching its declared expectation. [Fixture manifest](../fixtures/v0.5.0-conformance/README.md) | Negative fixtures may report rejection as their expected outcome. |
| Stored research-integrity audit | Exit 0 when the recomputed audit matches the retained report. [Audit](../audits/v0.6.5/audit-report.md) | The report's state remains `PASS_WITH_EXCEPTIONS`. |
| Claim bindings | Exit 0 for stored byte and dependency checks; the negative-test suite finishes `OK`. [Verifier](../scripts/validate_claim_bindings.py), [tests](../scripts/test_claim_bindings.py) | These checks assess declared file bindings and tested corruptions. |
| Public release status | Exit 0 for consistent release and citation identities. [Validator](../scripts/validate_public_release_status.py) | This checks local metadata and retained receipts. |
| Closeout | Exit 0 for the recorded maintenance state; the negative-test suite finishes `OK`. [Validator](../scripts/validate_closeout.py), [tests](../scripts/test_closeout.py) | The record retains deferred manuscript and research work. |
| Git comparison | Exit 0 with no tracked-file changes. | A difference requires inspection before any commit. |

## Complete workflow and replay

The [CI workflow](../.github/workflows/validate.yml) lists the remaining release, replication, development and rendering checks. It uses a full-history checkout and Python 3.12. Reproduce it in this disposable clone, with both requirements files installed for rendering.

The retained Jev responses can be reanalyzed without credentials or new model requests. The historical commands are preserved in the [prior README](../README-2026-11-03.md#reproduce-the-checks). Benchmark preparation and analysis have their own [protocol](../research/strengthening/evidence-update-001/report.md). Inspect generated files locally; preserve the original research records.

Software success establishes the condition tested by each command. Source truth, human independence, construct validity and institutional effectiveness require evidence beyond these checks. [Verification limits](research-integrity-verification.md), [evaluation methods](../research/strengthening/evaluation-methods.md).
