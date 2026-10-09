# Which HIT DOI should I cite?

Cite the software version you actually used. The [README citation](../README.md#citation) and [CITATION.cff](../CITATION.cff) identify the current published release, 0.6.7, through its verified exact-version DOI.

## A specific software release

Each version DOI identifies a separate archive. An older DOI remains appropriate when your work used that older version; publication of a newer version does not require you to change that citation.

| Software version | Exact-version DOI | Release record |
| :--- | :--- | :--- |
| 0.6.7 | [10.5281/zenodo.23252877](https://doi.org/10.5281/zenodo.23252877) | [Current release](releases/v0.6.7.md) |
| 0.6.6 | [10.5281/zenodo.23226713](https://doi.org/10.5281/zenodo.23226713) | [Historical release](releases/v0.6.6.md) |
| 0.6.5 | [10.5281/zenodo.21864224](https://doi.org/10.5281/zenodo.21864224) | [Historical release](releases/v0.6.5.md) |
| 0.6.4 | [10.5281/zenodo.21446142](https://doi.org/10.5281/zenodo.21446142) | [Historical release](releases/v0.6.4.md) |

The 0.6.6 archive corresponds to tag `v0.6.6`, commit `6745873a990554cf40303e217865895122494696`. Its [publication receipt](../release/v0.6.6/publication-receipt.json) records the archive comparison. The receipt and later documentation updates are outside that archive; they do not change its contents or DOI.

The 0.6.7 archive corresponds to tag `v0.6.7`, commit `4336b8acd16d571ef9b5ab1d8ca1ecc2ea0eb01e`. It includes the later author-review supplements, evidence-update rehearsal, and current working manuscript with three exhibits. Its [publication receipt](../release/v0.6.7/publication-receipt.json) records the archive comparison. The 0.6.6 DOI does not identify those additions. The original 0.6.7 tag retains its prepared metadata; the receipt and this publication-status update are outside its archive and do not alter the tag or DOI.

For work using changes after a published tag, also record the exact Git commit and repository URL. A release DOI does not identify later commits. See the [release index](releases/README.md) for other checkpoints and candidate status.

## The project across versions

The software concept DOI, [10.5281/zenodo.21446141](https://doi.org/10.5281/zenodo.21446141), represents Human Influence Telemetry across its published software versions. Use it when discussing the evolving project without referring to a particular implementation or result. Reproduction of version-dependent work requires the exact version and commit used.

## The originating research

The originating research DOI, [10.5281/zenodo.21204892](https://doi.org/10.5281/zenodo.21204892), identifies a separate research record. Cite it when discussing that record; use a software-version DOI for the corresponding software archive. The research record and software releases retain their own evidence and claim boundaries.
