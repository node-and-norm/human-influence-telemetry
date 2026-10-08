# Pressure test of the bounded v1 increment

Date: 7 October 2026, America/New_York. Baseline: main `3214dc9`, after PR #30. This is an AI-assisted development review, not an independent implementation audit or scientific acceptance record.

## Findings and repairs

| Finding | Repair or disposition |
|---|---|
| Replication-study preparation blocked a semantic release even though completed replication was optional | ADR-0005 prospectively separates stable and empirical dependencies; protected study files remain unchanged. |
| Independent reviewer was preferred in one document and required in another | Readiness text now follows the independent-human eligibility rule in HIT-CRI-V100-001. |
| A declared migration-guide file did not exist, but the packet check passed | Corrected the path; checks now inspect required files and reject unsafe paths, omitted files and mismatched declared hashes. |
| Cigna migration text still described the completed exercise as deferred | Corrected the informative guide while preserving the historical records and manifest. |
| Green staging checks could be mistaken for completed readiness | Labels distinguish staging consistency from readiness; audit-ready and release-ready modes return failure with unresolved requirements. Future acceptance requires reviewed validator implementation. |
| A reduced target-component map could pass | Require all five named stable components. |
| Missing canonical, migration or comparison input declarations could pass | Require the exact candidate input map and distinct comparison inputs. |
| Eligibility helper used a format different from the public submission schema | Use the same public auditor object for pre-audit declarations and submitted records. |
| README retained a single release sequence after track separation | Replaced that sequence with separate-track and chronological-allocation language. |
| Ofqual's April 2021 report page was retrieved in a version marked updated April 2024 | Added the current-version distinction without implying an authenticated original or silently rescoring. |
| One issue-report proposition was reused across four dimensions | Split the dimension-specific propositions and reasoning paths while preserving one source lineage, not four independent confirmations. |

## Validation scope

Local development checks used Python 3.14.3 in an isolated environment with requirements-dev.txt. The CI workflow uses Python 3.12; its run on the exact pushed head is a separate verification record. Local results must not be described as a completed CI run before GitHub reports that outcome.

The 27 readiness regression tests cover omitted files and inputs, path traversal and symlink escape, hash mismatch, fabricated completion, dropped empirical safeguards, premature scoring, reduced component maps, missing tasks, invalid vector substitution, model/self/contributor eligibility, incomplete submissions, and failed or blocked tasks presented as passing. These tests inspect declared structures and local bytes. They cannot authenticate a reviewer or establish scientific support.

The current repository workflow checks were run locally: historical human-result and release metadata, current-contract replication-candidate safeguards, source-audit and recruitment controls, public release status, the v0.6.5 research-integrity audit, conformance and CLI behavior, and supplementary research checks. The archived Jev runs were replayed offline; no new model API call was made. The research-integrity audit retains PASS_WITH_EXCEPTIONS and all eight negative controls.

The implementation rehearsal ran the public valid/invalid examples, non-mutating migration plan and synthetic comparison. Repeated comparison output was byte-identical. This is preparation by contributing software agents, not eligible clean-room evidence.

The complete-record draft passes executable conformance. Eight additional tests cover the valid draft and reject premature author acceptance, independent-review claims, release credit, frozen-plan edits, event-boundary expansion, missing source-ledger material and invalid claim references. The retained byte check does not validate source truth or recalculate the four within-assistant source-subset judgments. Period, conflict and formatting reanalyses remain unexecuted.

## Known historical-check limitation

An additional run of `scripts/validate_v040_release_readiness.py`, outside the current CI workflow, failed. It is a historical pre-0.4 promotion guard that still requires a README release of 0.2.1 and the superseded Cigna status `deferred_locked_protocol`. The README requirement already conflicts with the baseline's released 0.6.5 status; the corrected migration guide now also conflicts with its old text expectation. The script is preserved unchanged and must not be presented as a current readiness check. Its failure is disclosed here, not counted as a successful test.

## Research and release limits

The historical contracts, scorer submissions, protected replication materials and version-specific DOI files remain unchanged. No new source interpretation is accepted by this review. The Ofqual extension is a separate development application under a plan committed before new dimension findings. Its interpretation, matched baseline and source-subset judgments require responsible-author review.

All eight stable-release gates remain unresolved. Independent implementation review, accepted current-contract applications or substantiated exceptions, a public v0.9 candidate and explicit stable-release acceptance remain absent. No tag, Zenodo update, maturity promotion or external invitation follows from these checks.
