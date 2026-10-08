# v0.6.6 bounded release acceptance

Date: 7 October 2026, America/New_York. Authority: [AD-004](../../research/strengthening/author-decisions.md), the maintainer's explicit direction to commit, merge, clean up merged branches, and publish documented releases. Codex records and implements that direction. This file is a preparation record, not a substitute for the external publication receipt.

## Scope

Publish a non-breaking development and reproducibility update after v0.6.5. Include the supplementary research workbench, preserved model runs, readiness controls, candidate implementation instructions, exploratory Ofqual draft, and named evaluation procedures. The Ofqual draft and its comparison judgments remain pending author adjudication. Its publication as a development artifact does not make it an accepted finding or satisfy a v1 application gate.

Normative contract 0.4.0, conformance engine 0.5.0, historical assessments, the 0.6.0 human result, protected replication controls, Level 2, and the archived v0.6.5 claim-evidence audit remain unchanged. There is no migration or rescoring requirement. The existing unpublished v0.7.0 draft is outside this release.

## Publication checks

1. Review the release diff and confirm that protected evidence and the frozen Ofqual plan remain byte-identical to the pre-release baseline.
2. Run every current CI command and the exact-version metadata negative tests. Preserve failure output. The obsolete pre-0.4 promotion guard remains outside current CI; its known failure is disclosed in the release note.
3. Require successful hosted CI on the final release-PR revision, merge without rewriting the frozen plan's ancestry, then require CI on the exact merged commit that will be tagged.
4. Generate a source archive from that exact commit. Record its SHA-256, the commit, check results and CI link as release assets. Do not claim that a locally generated archive and GitHub's automatically generated archive have identical packaging bytes.
5. Publish tag v0.6.6 and the GitHub release only from that verified commit. Check the remote tag and public release afterward. Delete only branches whose commits are preserved in main.
6. Observe Zenodo processing. Verify the public record's version, title, software type, files and relationship to software concept 21446141. Until then, report the exact-version DOI as pending; never substitute the v0.6.5 DOI.
7. Record the observed publication and archival outcome in a follow-up commit. Do not move a published tag to insert a later-assigned DOI. Metadata checks verify consistency, not the existence of an external archive.

## Failure and recovery

A failed current check blocks this release. A failed v1 release-ready or implementation audit-ready check is expected because those separate gates remain unresolved. An unavailable Zenodo archive does not invalidate a published GitHub release, but archival completion must remain unclaimed. Investigate the existing integration before creating any manual record, to avoid duplicate versions.

If a published release has a material defect, document it and prepare a corrective release. Preserve its tag, DOI and research history. If cleanup removes a merged branch, its commits remain recoverable from main and the pull-request record.

## Remaining research work

All eight stable-release gates remain unresolved. The six Ofqual interpretation decisions, independent human implementation audit, current-contract inter-rater study, construct-validity assessment, and operational usefulness evaluation remain separate obligations. This release does not provide independent peer review, certification, legal assurance, institutional adoption, or evidence of improved outcomes.
