<div align="center">

# Human Influence Telemetry

Documentary evidence of practical human authority.

[![HIT Validation](https://github.com/node-and-norm/human-influence-telemetry/actions/workflows/validate.yml/badge.svg)](https://github.com/node-and-norm/human-influence-telemetry/actions/workflows/validate.yml) [![Release: v0.6.6](https://img.shields.io/badge/release-v0.6.6-blue)](https://github.com/node-and-norm/human-influence-telemetry/releases/tag/v0.6.6) [![Maturity: Level 2](https://img.shields.io/badge/maturity-Level%202-orange)](RESEARCH.md) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE) [![ORCID](https://img.shields.io/badge/ORCID-0009--0001--8121--2878-brightgreen)](https://orcid.org/0009-0001-8121-2878)

</div>

[At a glance](#at-a-glance) · [Choose your path](#choose-your-path) · [The research problem](#the-research-problem) · [Current results](#current-results) · [Repository map](#repository-map) · [Reproduce the checks](#reproduce-the-checks) · [Research boundaries](#research-boundaries) · [Citation](#citation) · [Release history and next gates](#release-history-and-next-gates)

## At a glance

A record that a person reviewed an algorithmic decision does not establish what that person could understand or change. Human Influence Telemetry (HIT) helps researchers organize documentary evidence about that practical authority, identify missing records, and make assessment judgments open to inspection.

Use the specification and handbook to define an actor, decision, period, and evidence boundary. Record the finding and its supporting sources, then run the conformance checks. A valid assessment record still requires a defensible interpretation of the evidence.

| Research checkpoint | Current account |
| :--- | :--- |
| Published artifact | Repository release 0.6.6, archived on Zenodo; normative contract 0.4.0; conformance engine 0.5.0 |
| Human evidence | Two independent scorers agreed on 7 of 7 items for one frozen Cigna packet under the earlier 0.1.0 scorer contract |
| Publication controls | Thirteen mapped claims, five gates, eight negative controls; audit state `PASS_WITH_EXCEPTIONS` |
| Development evidence | Three partial applications, two retained advisory model experiments, and one complete Ofqual draft pending author review; no maturity promotion |
| Open questions | Current-contract replication, broader validity, comparative usefulness, novelty, and institutional outcomes remain unresolved |

**Current release:** 0.6.6

**Publication state:** Published on [GitHub](https://github.com/node-and-norm/human-influence-telemetry/releases/tag/v0.6.6) and [Zenodo](https://zenodo.org/records/23226713). The [publication receipt](release/v0.6.6/publication-receipt.json) records the exact commit, passing validation and archive comparison.

**Current exact-version DOI:** `10.5281/zenodo.23226713`

**Human-result release:** 0.6.0

**Conformance engine version:** 0.5.0

**Current maturity:** Level 2, Applicable

The [working manuscript](paper/manuscript.md) is a methods draft. The [five-priority status](research/strengthening/priority-status.md) distinguishes completed development work from pending research obligations. Release 0.6.6 collects development work beyond the archived v0.6.5 package; distributing those records does not accept their scientific interpretations.

## Choose your path

| Reader | Start here | Then inspect |
| :--- | :--- | :--- |
| Researcher | [Application handbook](docs/application-handbook.md) and [specification](SPECIFICATION.md) | [Historical cases](case-studies/README.md), [solo evaluation design](research/strengthening/solo-evaluation.md), and [limitations](LIMITATIONS.md) |
| Reviewer | [Research claims](RESEARCH.md) and [claim-evidence map](evidence/claim-evidence-map.json) | [Integrity audit](audits/v0.6.5/audit-report.md), [source challenges](research/strengthening/solo-001/dossier.md), and [author decisions](research/strengthening/author-decisions.md) |
| Implementer | [Reproduce the checks](#reproduce-the-checks) and [schema](schema/) | [Conformance fixtures](fixtures/v0.5.0-conformance/README.md) and [implementation candidate](implementation/v1.0.0-candidate/README.md) |

## The research problem

> Can observable records distinguish substantive human influence from ceremonial human presence in AI-mediated institutional decisions?

HIT assesses what records establish about a named actor's influence. It does not infer intention or control deployed systems. A signature or review step prompts questions about access, reasoning, intervention, and consequences; the label alone cannot answer them.

### Six substantive dimensions plus Telemetry Integrity

| Dimension | Documentary question |
| :--- | :--- |
| Counsel | Did the authority have pre-decision access to relevant underlying evidence? |
| Judgment | Did the authority independently evaluate reasons, alternatives, uncertainty, and context? |
| Command | Could the authority practically approve, reject, modify, stop, or escalate? |
| Correction | Could a decision be contested, reconsidered, modified, reversed, or appealed in practice? |
| Repair | After qualifying harm, did a named actor own and deliver remediation to affected persons? |
| Reform | Did a named authority exercise power to change the decision architecture? |
| Telemetry Integrity | What do process coverage and packet integrity establish about the assessment's documentary basis? |

The [specification](SPECIFICATION.md) controls the exact thresholds and evidence routes. These questions are a reading guide.

### Finding states

- `0`: absence supported by affirmative evidence.
- `1`: process-specific formal or ceremonial presence under the applicable rule.
- `2`: substantive exercise or qualifying operational capability under the applicable rule.
- `IE`: insufficient evidence.

`IE` is not converted to zero or averaged into an ordinal total. A substantive finding must identify its evidence route. Practical authority can be exercised harmfully; a high finding does not establish a fair outcome.

## Current results

### Preserved human exercise

Two eligible independent scorers assessed frozen packet `HIT-IR-CIGNA-PXDX-001` under protocol `HIT-IRP-CIGNA-001` and scorer contract 0.1.0. They produced 7 of 7 exact agreements, with zero critical disagreements. Both assigned `1` to all six substantive dimensions and `limited` to Telemetry Integrity.

Cohen's kappa is undefined because the six substantive ratings have no category variance. This result describes one packet, two scorers, and one category pattern. It does not establish population reliability or replication under contract 0.4.0. See the [preserved results](validation/results/README.md) and [maturity decision](docs/decisions/ADR-0004-advance-hit-to-maturity-level-2.md).

### Executable publication controls

Version 0.6.5 connects H1–H9 and four material paper claims to traceability, integrity, human support review, evidence fitness, and dependency-closure gates. Evidence fitness separates directness, contemporaneity, independence, completeness, and publication authority. Eight negative controls test specified corruptions.

The [audit](audits/v0.6.5/audit-report.md) reports `PASS_WITH_EXCEPTIONS`. That state describes mapped claims and controls; it does not certify every repository statement or external source.

### Development documentary and model work

The [development workbench](research/strengthening/README.md) contains three partial applications: Obermeyer, Ofqual, and selected Robodebt inquiry recommendations. The assistant-prepared comparisons propose ties with a capable structured review. The [author decision record](research/strengthening/author-decisions.md) accepts two bounded Obermeyer qualifications while preserving historical scores.

Two separate Jev experiments matched 8/8 and 9/10 assistant-authored reference labels. The [second experiment](research/strengthening/passage-report.md) retains a date-related interpretation disagreement. Its inputs are constructed passages, not full historical documents. These results test advisory model behavior; they supply no independent human ratings or measured user benefit.

The [complete Ofqual draft](research/strengthening/solo-002-complete/README.md) extends the earlier announcement-only dossier. It passes record conformance while source interpretation and responsible-author adjudication remain pending. Its matched baseline proposes a tie. The [release notes](docs/releases/v0.6.6.md) distinguish these development artifacts from the unchanged human result and all eight unresolved stable-release gates.

## Repository map

| Location | Purpose |
| :--- | :--- |
| [SPECIFICATION.md](SPECIFICATION.md), [schema/](schema/), [handbook](docs/application-handbook.md) | Normative rules, record structure, and application guidance |
| [case-studies/](case-studies/README.md) | Version-bound historical assessments |
| [validation/](validation/README.md) | Preserved human results and gated replication work |
| [src/](src/), [fixtures/](fixtures/README.md), [scripts/](scripts/) | Conformance implementation, test inputs, and validation tools |
| [evidence/](evidence/), [audits/](audits/), [protocols/](protocols/) | Claim support, research lineage, and publication controls |
| [research/strengthening/](research/strengthening/README.md) | Current documentary tests, model results, literature challenges, and author decisions |
| [paper/](paper/README.md), [figures/](figures/README.md) | Working manuscript, references, and reproducible publication figures |
| [Release index](docs/releases/README.md), [roadmap](ROADMAP.md) | Published checkpoints and future gates |
| [Repository audit](docs/repository-audit-2026-10-03.md) | Cleanup findings, checks performed, and remaining limits |

## Reproduce the checks

Use Python 3.12, matching CI. From a local clone, create and activate a virtual environment, then install the pinned dependencies:

```bash
git clone https://github.com/node-and-norm/human-influence-telemetry.git
cd human-influence-telemetry
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --requirement requirements-dev.txt
python -m src conformance --all
python scripts/run_research_integrity_audit.py --check
python scripts/validate_research_strengthening.py --check
python scripts/validate_solo_application.py --check
python scripts/test_research_strengthening.py
python scripts/validate_solo_complete.py --check
python scripts/test_solo_complete.py
python scripts/test_v1_readiness.py
python scripts/run_jev_claim_pilot.py --analyze research/strengthening/jev-live-001
python scripts/run_jev_claim_pilot.py --analyze research/strengthening/jev-live-002
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in PowerShell. These checks and model replays require no API key or live inference. The [CI workflow](.github/workflows/validate.yml) lists the additional release, replication-candidate, and implementation-readiness checks.

To inspect your own record, run `python -m src conformance --path assessment.json`. For a historical record, `python -m src migration-plan --path historical-assessment.json` produces a non-mutating migration plan. Conformance checks record structure and declared rules; it does not verify source truth.

The [evaluation-methods register](research/strengthening/evaluation-methods.md) states what each software check, documentary review, and research evaluation can establish. It distinguishes completed development procedures from pending independent implementation and current-contract reliability studies.

## Research boundaries

HIT has not established population reliability, causal effectiveness, legal conformity, independent institutional adoption, or general field validity. The literature review and novelty assessment remain incomplete. Model agreement, deterministic tests, and a valid record cannot substitute for source interpretation or independent human evidence.

**Active replication protocol:** `HIT-IRP-HIT040-002`, candidate, scoring prohibited

The solo development track remains separate from that protocol. Ofqual and Robodebt are automation-boundary applications; their inclusion does not establish that each system meets every definition of AI. Read [LIMITATIONS.md](LIMITATIONS.md), the [closest-method comparison](research/strengthening/closest-methods.md), and the [author decision queue](research/strengthening/priority-status.md) before reusing conclusions.

Contributions should identify the changed proposition, supporting evidence, uncertainty, and conditions that would reverse the conclusion. Follow [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md); exclude confidential or restricted case material without documented publication authority.

## Citation

Cite the exact software version and commit you used. The v0.6.6 DOI identifies the archive at tag `v0.6.6`, commit `6745873a990554cf40303e217865895122494696`. The v0.6.5 DOI identifies only that earlier archive and must not be attached to 0.6.6.

**Exact-version DOI:** [10.5281/zenodo.23226713](https://doi.org/10.5281/zenodo.23226713)

Use this citation for the verified v0.6.6 archive:

> Banasihan, M. J. (2026). *Human Influence Telemetry* (Version 0.6.6) [Software]. Zenodo. https://doi.org/10.5281/zenodo.23226713

**Previous version DOI, exact `v0.6.5` release:** [10.5281/zenodo.21864224](https://doi.org/10.5281/zenodo.21864224)

**Concept DOI, all software versions:** [10.5281/zenodo.21446141](https://doi.org/10.5281/zenodo.21446141)

**Originating research DOI:** [10.5281/zenodo.21204892](https://doi.org/10.5281/zenodo.21204892)

**Previous version DOI, exact `v0.6.4` release:** [10.5281/zenodo.21446142](https://doi.org/10.5281/zenodo.21446142)

Machine-readable citation metadata is in [CITATION.cff](CITATION.cff). The originating research record and software archives are separate artifacts.

## Author

Mark Julius Banasihan · [Node & Norm](https://github.com/node-and-norm) · [ORCID](https://orcid.org/0009-0001-8121-2878)

Repository stewardship moved to Node & Norm on 2026-09-15. Published versions, authorship, and research-status claims retain their existing scope. AI assistance and scoped author decisions are disclosed in the research records.

## Release history and next gates

<details>
<summary>Published layers and preserved boundaries</summary>

| Version | Published contribution |
| :--- | :--- |
| 0.4.0 | Normative assessment contract |
| 0.5.0 | Complete-record conformance engine |
| 0.6.0 | Bounded human result; maturity Level 2, Applicable |
| 0.6.4 | Standalone software archive and DOI metadata |
| 0.6.5 | Claim-evidence controls and paper workspace |
| 0.6.6 | Development workbench, reproducibility and release-readiness controls |

Version 0.6.6 is published as a nonbreaking development and reproducibility release. Its GitHub release and exact-version archive are verified in the publication receipt. It does not activate the study or implementation-audit candidates.

Specification, assessment schema, and dimension catalog remain 0.4.0. The engine remains 0.5.0. See the [release index](docs/releases/README.md) for checkpoint details.

</details>

<details>
<summary>Future releases and v1.0 gates</summary>

**Stable target:** `1.0.0`, release prohibited until the published gates pass.

Version 1.0.0 would make a compatibility and public-implementability commitment. Research maturity remains a separate claim. Candidate and future-version documents in the repository are planning and release-control artifacts. They are not published releases.

The stable track leads to 0.9.0 implementation review and release-candidate freeze before 1.0.0 promotion. The planned 0.7.0 packet/protocol package and 0.8.0 empirical-result package belong to the separate study track. Later study publication requires an explicit chronological version allocation if the stable track advances first; protected protocol requirements remain unchanged.

Stable-release gates include current-contract applications or substantiated migration exceptions, a complete implementation packet, independent human clean-room review, a public release candidate, and synchronized component promotion. [ADR-0005](docs/decisions/ADR-0005-separate-stable-and-empirical-tracks.md) assigns human case selection, frozen packets, and locked scoring materials to the separate replication track. Draft workbooks remain scoring-prohibited. See the [five-priority execution record](research/strengthening/v1-priorities.md) and [stable gate register](release/v1.0.0/gate-register.json).

The [readiness plan](docs/v1-readiness-plan.md), [candidate release](docs/releases/v1.0.0-candidate.md), and [machine-readable gate ledger](release/v1.0.0/contract-freeze.candidate.json) govern these decisions.

</details>
