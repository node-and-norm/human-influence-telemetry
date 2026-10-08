# Which HIT DOI should I cite?

Use the DOI for the software version you actually used. The [README citation](../README.md#citation) and [CITATION.cff](../CITATION.cff) identify the current published release, 0.6.6.

## A specific software release

Each version DOI identifies a separate archive. An older DOI remains appropriate when your work used that older version; publication of a newer version does not require you to change that citation.

| Software version | Exact-version DOI | Release record |
| :--- | :--- | :--- |
| 0.6.6 | [10.5281/zenodo.23226713](https://doi.org/10.5281/zenodo.23226713) | [Current release](releases/v0.6.6.md) |
| 0.6.5 | [10.5281/zenodo.21864224](https://doi.org/10.5281/zenodo.21864224) | [Historical release](releases/v0.6.5.md) |
| 0.6.4 | [10.5281/zenodo.21446142](https://doi.org/10.5281/zenodo.21446142) | [Historical release](releases/v0.6.4.md) |

The 0.6.6 archive corresponds to tag `v0.6.6`, commit `6745873a990554cf40303e217865895122494696`. Its [publication receipt](../release/v0.6.6/publication-receipt.json) records the archive comparison. The receipt and later documentation updates are outside that archive; they do not change its contents or DOI.

For work using changes after a published tag, also record the exact Git commit and repository URL. A release DOI does not identify later commits. See the [release index](releases/README.md) for other checkpoints and candidate status.

## The project across versions

The software concept DOI, [10.5281/zenodo.21446141](https://doi.org/10.5281/zenodo.21446141), represents Human Influence Telemetry across its published software versions. Use it when discussing the evolving project without referring to a particular implementation or result. Reproduction of version-dependent work requires the exact version and commit used.

## The originating research

The originating research DOI, [10.5281/zenodo.21204892](https://doi.org/10.5281/zenodo.21204892), identifies a separate research record. Cite it when discussing that record; use a software-version DOI for the corresponding software archive. The research record and software releases retain their own evidence and claim boundaries.
