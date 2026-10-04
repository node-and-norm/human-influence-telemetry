# Research strengthening workbench

This supplementary workbench tests the usefulness and limits of HIT. It is development work following v0.6.5, with no new release or research-maturity decision. The submitted chapter is outside its scope.

| Priority | Deliverable | Evidence available |
|---|---|---|
| 1. Claim audit | [Findings and dispositions](claim-audit.md), machine-readable [register](claim-audit.json) | Repository observations and proposed interpretation limits; human adjudication pending |
| 2. Closest literature | [Comparison and search record](literature-review.md) | Targeted source review; systematic coverage and independent novelty review pending |
| 3. Adversarial tests | [Protocol](adversarial-protocol.md), [cases](adversarial-cases.json), generated [results](results.json) | Deterministic tests of supplied facts; source interpretation remains untested |
| 4. Practical usefulness | [Comparison protocol and worked demonstration](utility-protocol.md) | Synthetic worked demonstration; participant results absent |
| 5. External evaluation | [Reviewer packet](external-review.md), [response template](review-response.template.json) | Ready for scoped review; no external review claimed |

Run `python scripts/validate_research_strengthening.py --check` from the repository root. Use `--write` to regenerate the result after reviewing changes to inputs. Neither command calls an AI service. Results include hashes of inputs and the existing rubric implementation. CI verifies reproducibility and rejects unsupported promotions in this workbench.

The 0.4.0 contract, 0.5.0 conformance engine, historical applications, 0.6.0 human result, and v0.6.5 archive remain preserved. Current-contract external-rater replication under HIT-IRP-HIT040-002 remains unresolved; its recruitment and scoring gates still apply. This package does not authorize participant recruitment under that protocol.

The candidate contribution is a reproducible representation of documentary judgments about practical authority, with explicit uncertainty and actor/period boundaries. Whether this representation improves assessment is an open empirical question. High findings do not establish a fair decision, lower harm, or legitimate authority.

## Completion criteria

The local deliverables are complete when the five linked artifacts exist and validation passes. Research conclusions require additional evidence: responsible-author adjudication of audit findings; independently checked literature comparisons; raw participant outputs for usefulness; and external reviewer records. Each result must state which criterion it satisfies. Repository size, test count, and model agreement are not proxies for field validity.

## Assistance and provenance

Prepared with Codex assistance on 2026-10-03 against main commit `74558075da0e6a8bc0c25357dac27f4428bede9e`. The user authorized implementation of five repository priorities and reuse of the existing private Jev credential. AI assistance covered repository inspection, targeted literature retrieval, proposed judgments, code, and prose. Human scientific adjudication is pending; user authorization is not recorded as agreement with each finding. No new human ratings or institutional records were produced. One Jev request returned eight advisory judgments after the design was committed. See [AI review design](ai-review.md) and the [pilot report](jev-report.md).
