# Public implementation rehearsal

This guide prepares the clean-room audit. The packet remains a candidate: its manifest prohibits audit activation until the commit, inputs, expected outputs, and environment have been frozen and validated. A developer may rehearse these commands now. A rehearsal supplies development evidence, not an independent audit result.

Use the [audit protocol](audit-protocol.md) for eligibility, permitted coordination, and publication requirements. The [task catalog](task-catalog.json) identifies the inputs and expected behavior. Never replace a failed output with a later successful run; retain both.

## 1. Obtain a fresh checkout and record the environment

The commands below use a POSIX shell, Git, and Python 3.10 or later. Windows users may run them in a POSIX environment and must record that environment. They have not been qualified for native PowerShell. Dependency installation requires access to the package index.

```sh
git clone https://github.com/node-and-norm/human-influence-telemetry.git human-influence-telemetry-audit
cd human-influence-telemetry-audit
```

For an activated audit, check out the exact 40-character commit in the frozen manifest before continuing. A branch name or the latest release is insufficient. When the manifest's `exact_repository_commit` is null or `audit_permitted` is false, stop the formal audit and record the blocking condition. Development rehearsals must be labeled as such.

```sh
git rev-parse HEAD
git status --porcelain
python3 --version
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip freeze --all
python -c 'import platform, sys; print(platform.platform()); print(sys.version); print(sys.executable)'
```

Record the original command, working directory, exit code, stdout, stderr, elapsed time, and any warnings for each installation attempt. `requirements-dev.txt` pins the direct dependencies; `pip freeze --all` records the actual transitive environment. An unsupported or failed environment is a result to preserve.

From the repository root, create an output directory outside the checkout:

```sh
hit_audit_outputs="$(mktemp -d)"
printf '%s\n' "$hit_audit_outputs"
```

Keep this directory until the audit record and original outputs have been published. The paths below use the same shell session. Do not add these outputs to historical case or scorer directories.

## 2. Reconstruct the versions

Read `CITATION.cff`, `SPECIFICATION.md`, `schema/hit-assessment.schema.json`, `schema/hit-dimension-catalog.json`, `docs/application-handbook.md`, `compatibility/hit-compatibility-manifest.json`, and `RESEARCH.md`. Record each component version, repository release, research maturity, and supported historical contracts with its source path. A candidate directory name does not promote a component or release version.

## 3. Validate the canonical complete record

```sh
python -m src conformance --path fixtures/v0.4.0-canonical-example.json --format json --output "$hit_audit_outputs/valid-assessment.json"
```

Expected exit code: `0`. The JSON report has `valid: true` and no issues. This fixture is synthetic. Its conformance supplies no empirical finding about an institution.

The exact relative input path matters: individual reports include the supplied source path. Use the same path when reproducing a byte-level output digest.

## 4. Run and explain the invalid vectors

```sh
python -m src conformance --all --format json --output "$hit_audit_outputs/repository-conformance.json"
```

Expected exit code: `0` when the suite behaves as declared. A suite passes by rejecting its invalid records; a passing suite does not make those records conforming. Read `checks.complete_record_suite.cases` and inspect these three cases:

| Case ID | Expected assessment state | Required error code |
|---|---|---|
| `CR-CLAIM-REFERENCE-001` | `actual_valid: false` | `HIT-CLAIM-REFERENCE` |
| `CR-INTEGRITY-DERIVATION-001` | `actual_valid: false` | `HIT-INTEGRITY-DERIVATION` |
| `CR-IE-SEARCH-001` | `actual_valid: false` | `HIT-IE-SEARCH` |

The suite derives each record from `fixtures/v0.4.0-canonical-example.json` using the published mutations in `fixtures/v0.5.0-conformance/complete-record-cases.json`. Each result includes the derived record digest and the full issues. Explain every returned code with a locator in `docs/conformance-error-catalog.md`; preserve additional codes as observations. An unexplained code is a documentation defect.

For a separate CLI check of a deliberately invalid record, run:

```sh
python scripts/validate_v050_cli.py
```

This smoke test materializes the claim-reference mutation in a temporary directory and checks that the single-record command returns `1` with `HIT-CLAIM-REFERENCE`. The smoke-test process itself returns `0` when its assertions pass. See `docs/executable-conformance.md` for the distinction between CLI argument, record, and suite failures.

## 5. Explain the rules from public artifacts

Use `SPECIFICATION.md` and `docs/application-handbook.md` to describe actor attribution, evidence references and states, finding assignment, Repair triggers, sampling, aggregation, split Telemetry Integrity, citation precision, and compatibility. Give section or field locators for the explanation. Record any conflict between public documents. The task assesses whether the rules can be reconstructed; it does not ask the implementer to certify their normative correctness.

## 6. Generate a non-mutating migration plan

```sh
python -m src migration-plan --path case-studies/assessments/toeslagenaffaire-harm-period.json --format json --output "$hit_audit_outputs/migration-plan.json"
```

Expected exit code: `0`, with `valid_plan: true`, `automatic_migration: false`, `source_preserved: true`, and `disposition: fresh_reassessment_required`. Check the source file digest before and after the run. Explain the required reassessment using `docs/migration-guide-v0.1.0-to-v0.4.0.md`. This command does not create a current-contract assessment or alter the historical findings.

## 7. Reproduce a synthetic comparison

```sh
python scripts/validate_scorer_submission.py validation/test-vectors/rater-a.json
python scripts/validate_scorer_submission.py validation/test-vectors/rater-b.json
python scripts/compare_raters.py validation/test-vectors/rater-a.json validation/test-vectors/rater-b.json --format json --output "$hit_audit_outputs/synthetic-comparison.json"
python scripts/compare_raters.py validation/test-vectors/rater-a.json validation/test-vectors/rater-b.json --format json --output "$hit_audit_outputs/synthetic-comparison-repeat.json"
```

Expected exit code for each command: `0`. The comparison reports 6 agreements across 7 items, proportion `0.8571`, no critical disagreement, and substantive-dimension kappa `0.76`. These are synthetic software expectations, not human results. The two generated comparison files must have identical bytes.

## 8. Preserve digests and source boundaries

Python's standard-library `hashlib.file_digest` requires Python 3.11, so the following helper uses the Python 3.10-compatible interface. It hashes file bytes and prints the supplied path:

```sh
python -c 'import hashlib, pathlib, sys; [(print(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest(), p)) for p in sys.argv[1:]]' fixtures/v0.4.0-canonical-example.json fixtures/v0.5.0-conformance/complete-record-cases.json case-studies/assessments/toeslagenaffaire-harm-period.json validation/test-vectors/rater-a.json validation/test-vectors/rater-b.json "$hit_audit_outputs/valid-assessment.json" "$hit_audit_outputs/repository-conformance.json" "$hit_audit_outputs/migration-plan.json" "$hit_audit_outputs/synthetic-comparison.json" "$hit_audit_outputs/synthetic-comparison-repeat.json"
```

Byte hashes for input files are distinct from the suite's canonical-JSON hashes for derived records. Record the digest method and compare like with like. A formal audit must compare outputs with the frozen expected hashes; rerunning a command twice establishes repeatability only. Candidate expectations in this guide cannot substitute for the frozen reference outputs.

Explain the boundary in `docs/adjacent-system-boundaries.md`: HIT does not itself provide runtime enforcement, signed-receipt verification, policy-pack harmonization, compliance automation, or evidence portability.

## 9. Preserve failures and submit the human record

Copy `audit-submission.example.json` to a new audit record only after activation. Its null values represent unanswered questions and unperformed tasks. The example is a template, not a completed audit. The auditor supplies identity, independence and competence declarations, environment, exact commit, hashes, task results, original output references, coordination exchanges, and signature. Set `record_state` to `submitted` only when those fields are complete.

Use `pass`, `fail`, or `blocked` for each submitted task. A blocked task still needs a factual explanation and the available evidence; missing evidence must never be replaced by an invented successful run. Log every apparent need for private author knowledge, including missing artifacts and ambiguous rules. Publish failed and invalid audits as required by the protocol. Apply privacy review before publication and identify any necessary redaction without erasing the observed failure.

Validate the record's structure, substituting its actual path:

```sh
python -c 'import json, sys; from jsonschema import Draft202012Validator, FormatChecker; schema=json.load(open(sys.argv[1])); record=json.load(open(sys.argv[2])); Draft202012Validator.check_schema(schema); Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)' implementation/v1.0.0-candidate/audit-submission.schema.json implementation/v1.0.0-candidate/audit-submission.example.json
```

The command above checks the supplied template as a template. Schema validity cannot verify a person's identity, eligibility, truthful reporting, signature authenticity, or the contents of linked evidence. A designated human reviewer must inspect those facts and the frozen manifest before accepting an audit disposition. No schema pass activates an audit or authorizes a release.
