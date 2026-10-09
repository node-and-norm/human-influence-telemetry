# v0.6.7 bounded release acceptance

8 October 2026, America/New_York. Codex prepares this release under the maintainer's existing [AD-004 publication authority](../../research/strengthening/author-decisions.md) and current request to keep Releases updated. Permission concerns publication of the development artifact, not scientific approval of its pending interpretations.

## Release scope

Package the completed development increment through PR #37, with synchronized current-version metadata and a concise account of what changed. Publish a nonbreaking v0.6.7 release without promoting the 0.4.0 contract, 0.5.0 engine, 0.6.0 human result, Level 2 maturity or any v1 gate. The working manuscript remains subject to responsible-author review and separate submission approval.

## Required checks

1. Review the diff from the preceding release and the narrower release-preparation diff. Preserve historical evidence and the v0.6.6 tag, assets, release document and receipt.
2. Run every current CI-equivalent command and exact-version metadata tests. Distinguish expected candidate-readiness rejection from failing release checks. Keep the previously disclosed obsolete pre-0.4 guard outside the current passing-check count.
3. Require hosted CI success on the reviewed PR head and the exact merged commit to be tagged. Merge without rewriting the frozen benchmark and qualitative-extension commits.
4. Generate the source archive from that exact commit. Record its SHA-256, commit, local verification results and exact-commit CI URL as release assets. Source-only archives do not include Git history; historical replay requires the documented full clone.
5. Publish tag v0.6.7 and its GitHub release, then verify the remote tag, public release and asset digest. Delete only the merged feature branch whose commits remain in main.
6. Observe the existing Zenodo integration before attempting any manual archive. Verify the new record's version, software type, concept relationship and archive checksum. Compare all archived tracked files with the tagged Git tree; reject unsafe or duplicate paths without extracting them.
7. Record observed publication and archival results in a follow-up commit. Add the new DOI only after verifying it. Do not move the tag to include its later-assigned DOI or reuse the v0.6.6 DOI.

## Failure and recovery

### Explicit historical-input amendment

The earlier file-binding and qualitative-extension checks compared release-facing files with their historical base. This release changes the current research-summary and citation metadata legitimately. The additive frozen-input amendment resolves only `RESEARCH.md`, `CITATION.cff` and `.zenodo.json` to tracked, byte-exact historical copies at `9af12f6cb891288f692990366e54b85bd21d9e24`. The original binding manifest and extension design remain unchanged. Separate release checks validate today's metadata. No broader file exemption, source change, new interpretation or gate approval is authorized by this amendment.

The snapshot files are raw historical context, not current navigation pages. Their retained relative links refer to their original repository paths, which the amendment records. Rewriting those links at the snapshot location would change the preserved evidence.

### Publication failure

A failed applicable check blocks publication. An unavailable Zenodo record leaves archival status pending; it does not justify a duplicate deposit or invented identifier. A material defect in a published release requires a documented corrective release. Existing tags, archives and research records remain recoverable and unchanged.

## Release-note maintenance

Each merged release-facing increment belongs in the changelog's Unreleased section until packaging. On publication, move that account into the named release and publish readable GitHub notes describing included changes, verification and unresolved limits. Update DOI status from the observed archive separately. This convention makes Releases a reliable entry point without treating every merge as a scientific milestone.
