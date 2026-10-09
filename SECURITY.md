# Security Policy

## Supported versions

Security and integrity fixes are applied to `main` and the latest tagged release. The stable `1.0.0` target remains under gated development and is not yet a supported published release.

| Version | Supported |
|---|---|
| `main`, pre-`1.0.0` stabilization | Yes |
| `0.6.7`, latest tagged release | Yes |
| Earlier tagged releases | Best effort |
| Candidate `0.7.0`, `0.9.0`, and `1.0.0` documents | Development artifacts, not release channels |

Version 0.6.7 is published on the [canonical GitHub Releases page](https://github.com/node-and-norm/human-influence-telemetry/releases/tag/v0.6.7). Its [release notes](docs/releases/v0.6.7.md) and [publication receipt](release/v0.6.7/publication-receipt.json) identify the checks and verified archive. This development checkpoint retains all limits on institutional suitability and scientific assurance.

## Reporting a vulnerability

Do not publish an exploit, sensitive institutional record, private decision data, or credential in a public issue.

Report vulnerabilities through GitHub private vulnerability reporting when it is enabled for this repository. When that channel is unavailable, contact the maintainer privately through the contact method listed on the maintainer's GitHub profile.

Include:

- affected version or commit;
- affected file, schema field, validator, workflow, or documentation rule;
- reproduction steps;
- expected and observed behavior;
- impact on integrity, confidentiality, availability, or evidentiary reliability;
- proposed mitigation, when known.

## Relevant vulnerability classes

This project is especially concerned with:

- schema bypasses that accept structurally invalid assessments;
- duplicate or omitted dimension findings that pass validation;
- path traversal or unsafe file handling in reference tooling;
- workflow dependency compromise;
- tampering with fixtures, provenance, or release metadata;
- misleading evidence-integrity claims;
- publication of confidential or personally identifying case material;
- silent version drift among the specification, schema, fixtures, implementation, release notes, and citation metadata;
- activation of scorer or clean-room materials before their declared lock conditions pass;
- metadata that presents a candidate version as a published release.

## Response process

The maintainer will acknowledge a sufficiently detailed report, assess severity, determine whether coordinated disclosure is required, and prepare a tested correction. No fixed response-time guarantee is made during the pre-`1.0.0` research and stabilization phase.

A security fix does not by itself establish that HIT is suitable for high-stakes deployment. Implementers remain responsible for their own threat model, access controls, retention, privacy, and audit architecture.
