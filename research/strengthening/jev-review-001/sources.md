# Primary-source excerpts for the advisory rehearsal

The retained input is [sources.json](sources.json): nine passages, 2,520 whitespace-separated words, from four government-authored GOV.UK documents. Codex selected and extracted them on 7 October 2026, America/New_York, under the author's development-work authorization. Retrieval ran at `2026-10-08T02:22:26+00:00` to `2026-10-08T02:22:27+00:00`, the same evening locally.

These are selected current HTML representations of historical documents. They support a bounded advisory-model rehearsal. They do not replace the six-document [Ofqual application plan](../solo-002-complete/plan.md), its source ledger, or the pending scientific decisions. OCR-01 and OFQ-04 are excluded from this rehearsal; no awarding-body announcement, repository code, full-document search, publication-day snapshot, or private institutional record is supplied.

## Attribution and permission

Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

The publishers are Ofqual and the Department for Education. Each source below links to the original publication. GOV.UK identifies its content as available under OGL v3.0 except where otherwise stated; the three HTML publications also contain that licence statement. The National Archives licence was retrieved and checked for copying, distribution, attribution, exclusions and non-endorsement terms. Only government-authored prose is retained. Images, logos and linked third-party documents are excluded. Neither publisher endorses HIT or this use of its material.

| Source | Primary publication | First published | Public update | Status at retrieval |
| :--- | :--- | :--- | :--- | :--- |
| OFQ-01, Ofqual | [Statement from Roger Taylor, Chair, Ofqual](https://www.gov.uk/government/news/statement-from-roger-taylor-chair-ofqual) | 17 August 2020 | 17 August 2020 | No withdrawal marker observed |
| OFQ-02, Ofqual | [Annual Report and Accounts 2020 to 2021](https://www.gov.uk/government/publications/ofqual-annual-report-for-the-period-1-april-2020-to-31-march-2021/annual-report-and-accounts-2020-to-2021) | 20 July 2021 | 20 July 2021 | Retrospective report |
| OFQ-03, Ofqual | [Regulatory Burden Statement, April 2021](https://www.gov.uk/government/publications/ofquals-regulatory-burden-statement/regulatory-burden-statement-april-2021) | 30 April 2021 | 11 April 2024 | Later publicly updated representation |
| DFE-01, Department for Education | [Taking exams during the coronavirus outbreak](https://www.gov.uk/government/publications/coronavirus-covid-19-cancellation-of-gcses-as-and-a-levels-in-2020/coronavirus-covid-19-cancellation-of-gcses-as-and-a-levels-in-2020) | 20 March 2020 | 27 August 2020 | Withdrawn 25 February 2021 |

Publication and public-update dates come from GOV.UK's `first-published-at` and `public-updated-at` metadata. The JSON separately preserves later technical `updated-at` timestamps: 19 March 2026 for the Ofqual pages and 24 September 2026 for DFE-01. Those technical dates do not establish when any substantive passage changed. OFQ-03's 2024 public update remains an explicit limitation; no earlier wording was authenticated. DFE-01's full withdrawal notice is retained in the JSON. Its public update also postdates the application's 20 August 2020 follow-up boundary.

## Included passages

| Stable passage ID | Retained context |
| :--- | :--- |
| `OFQ-01-statement` | All six statement paragraphs, including reasons, apology, the changed grading rule and prospective implementation wording |
| `OFQ-02-advice` | Complete External Advisory Group and quality assurance subsection, including the report's own claims about model testing and bias |
| `OFQ-02-board` | Governance overview's Board-authority and executive-delegation paragraph, followed by the complete Secretary of State Directions subsection; the locator explicitly identifies this non-contiguous selection |
| `OFQ-02-results` | Complete Public confidence and results days subsection, including its asserted absence of systematic bias, public concern, Board decision and reported GCSE issue |
| `OFQ-03-direction` | Complete section 2.3, preserving the distinction between general qualifications and vocational or technical qualifications around the reissue requirement |
| `DFE-01-results` | Complete Results days subsection, including revised AS/A level issue, GCSE issue and qualifications whose results were delayed |
| `DFE-01-external` | Complete external-candidate subsection, including conditions for evidence acceptance, candidates who received no grade and possible admissions consideration |
| `DFE-01-admissions` | Complete grade-acceptance subsection, including capacity constraints, alternative courses and deferred places |
| `DFE-01-appeals` | Complete summer-appeals subsection and the adjacent Bias and discrimination subsection; the complaint route is retained alongside restricted appeal grounds |

The three Ofqual publications share institutional authorship. DfE is a separate publisher involved in the same response, with possible shared underlying information. Their statements are primary institutional reports, not independently verified findings. References within the reports to independent advisers do not make this packet an independent assessment of HIT or the reported outcomes. The financial audit of the annual report is outside these excerpts and supplies no assurance about the grading propositions here.

## Locator qualifications

During pre-run review, the retained OFQ-03 section 2.3 places the reissue statement in its fourth paragraph, whereas the existing draft locator says paragraph six. The DFE-01 external-candidate subsection places the no-grade qualification in its second paragraph, whereas the draft locator says paragraph three. These are differences between current retained passage locations and draft locators; this review does not establish why they differ. Section names and exact retained text identify the intended statements. The historical draft and its hashes remain unchanged; an author-reviewed correction can record its own provenance later.

## Extraction and verification

The [retrieval script](../../../scripts/fetch_jev_review_sources.py) selects paragraphs, list items and subsection headings from the main GOV.UK prose container. It decodes HTML character references and collapses whitespace within each block. It preserves words, punctuation and block order. No wording is paraphrased or corrected. Two newlines separate retained blocks; the JSON records each source-local block index and a prose locator.

Each passage has a SHA-256 digest of its UTF-8 text. Each source has a raw-response byte count and SHA-256 digest. Raw HTML is not retained; its hash includes page markup and may change without a prose change. These hashes identify retrieved inputs and retained extracts. They do not authenticate publication-day content, source truth, institutional independence or the correctness of a later model interpretation.

The source packet's SHA-256 is `69b66c02bbe76e1a70c03049b108957684e0121849359c71e1496f51c1afaa98`. Extraction produced four sources and nine unique passage IDs. Each retained text digest and its reconstruction from the stored blocks were checked. The complete Chair statement and the selected subsection boundaries were inspected against the public pages.

The script requires network access. To inspect fresh extracts without writing, run `python scripts/fetch_jev_review_sources.py --inspect`. To preserve a new comparison retrieval, use `--write --output` with a new file path. It refuses to overwrite an existing packet. Fresh retrieval may differ; any such change requires review before use. This script makes no model calls and supplies no assessment score or reference label.

Source selection remains assistant-prepared and exposed to the earlier Ofqual work. This packet cannot establish a held-out test, calibrated accuracy, human agreement, comparative usefulness or closure of an author decision or release gate.
