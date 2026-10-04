# Repository audit and cleanup

The post-merge audit found stale navigation and status prose while the existing executable checks passed. The audit inspected main at c962d4d9604965917ce2d2066df6cb1ce0a2e8fd, containing 265 tracked files and 128 Markdown files. Codex performed the audit on 3 October 2026 at the author's request.

## Checks and dispositions

| Area | Evidence and disposition |
|---|---|
| Merge safety | PR #28 was mergeable, its validation check passed, and the worktree was clean. Merge matched the inspected head 40faddacc4ab37bfdc6887e02b1a9690db4eaae0. |
| Branch cleanup | The publication-strengthening branch was deleted locally and remotely after merge. Older release branches match the exact heads of merged PRs #26 and #27 and have trees identical to their merge commits. Their work remains available through those PRs. |
| Release and contracts | Release/status validators, historical result checks, and complete-record conformance passed. Published version remains 0.6.5; specification remains 0.4.0; engine remains 0.5.0. |
| Research controls | The existing integrity audit remains PASS_WITH_EXCEPTIONS. Candidate replication and implementation gates remain closed. No new human acceptance was generated. |
| Supplementary checks | Sixteen adversarial rule cases, six conditional cases, nine failure-path/isolation tests, and both retained model replays passed their checks. The second replay retains its 9/10 label agreement; a successful replay does not erase the disagreement. |
| Documentation | Four literal truncation markers in the root README were repaired. The current ADR index link was repaired. Workbench status now distinguishes three partial applications and two model runs. |
| Installation guidance | Root quick start now names Python 3.12, the CI version, and an active virtual environment. A new independent clean-room installation was not performed. |
| Relative links | A scan of inline Markdown relative file targets found two missing targets. One current ADR link was repaired. The missing archive/v0.1.0/validation/inter-rater-protocol.md target is recorded as a historical exception; frozen archive content remains unchanged. |

The link scan checks file existence, not anchors, external availability, reference-style links, or citation validity. This audit is not an exhaustive security audit, dependency-vulnerability assessment, legal review, or independent scientific review. Passing software checks cannot establish source truth.

## Remaining research work

The [author decision queue](../research/strengthening/priority-status.md) remains the controlling list for scientific dispositions. [AD-001](../research/strengthening/author-decisions.md) records the author's explicit acceptance of two Obermeyer qualifications while preserving historical scores. Wider literature coverage, source completeness, full-document evaluation, and external review remain open. The submitted chapter and footnote remain outside this work.

Historical archives, frozen requests, raw model responses, and released assessments retain their original bytes, including obsolete prose inside retained experimental inputs. Those inputs document what the model actually received. Correcting current documentation must not rewrite that record.

No release or Zenodo publication follows from this maintenance audit. The cleanup improves repository navigation and status accuracy without expanding the eligible research claims.
