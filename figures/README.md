# Reproducible Figures

The [current development exhibits](development-2026-10-08/README.md) explain the assessment architecture, distinguish Ofqual event dates from later source publications, and compare qualification preservation in three representations. They are conceptual and documentary exhibits, not measures of validity or comparative performance. Their source records, exact locators, figure data, captions and reproduction instructions are kept together.

Each new exhibit has a vector SVG and a PNG preview. The artifact check verifies retained bytes and source bindings; the separate rendering check regenerates the vector output. Neither check establishes the truth of a source or accepts a pending interpretation.

## Historical claim-gate figure

The v0.6.5 research-integrity figure is generated from the audited claim map.

```bash
python scripts/run_research_integrity_audit.py
python scripts/run_research_integrity_audit.py --check
```

The generator writes derived CSV data, an SVG figure, the audit result, its narrative report, and a figure manifest. The check mode compares regenerated content with the committed files and fails on drift.
