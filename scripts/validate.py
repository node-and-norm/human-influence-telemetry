#!/usr/bin/env python3
"""Validate the HIT 0.6.0 human result, current release metadata, and preserved contracts."""
from __future__ import annotations
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
from typing import Any
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from release_metadata import CURRENT_RELEASE, CURRENT_RELEASE_DATE, CURRENT_VERSION_DOI, validate_citation_guidance, validate_identity

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.validation.assessment import validate_assessment

RESULT_RELEASE = "0.6.0"
ENGINE, CONTRACT, LEGACY = "0.5.0", "0.4.0", "0.1.0"
SOFTWARE_CONCEPT_DOI = "10.5281/zenodo.21446141"
ORIGINATING_RESEARCH_DOI = "10.5281/zenodo.21204892"
PREVIOUS_VERSION_DOI = "10.5281/zenodo.21446142"
A_SHA = "9c90e2eaf0785cd83f4962058d622a948c2ba60c1de830e06a2474eb85542a33"
B_SHA = "553669d57679fc2034b27021a4b021333c94770ecc656d9b18c1c438f494dd9b"
CMP_SHA = "91b28ec23f6f446be3ccd4868d9975a7f143da917de87ab5c2f5ac0123b3ced2"
BUNDLE_SHA = "de655f5766009e8cd8a7c52652c53cc7930586f072007839877d542f4138617f"

P = {
    "schema": ROOT / "schema/hit-assessment.schema.json",
    "catalog": ROOT / "schema/hit-dimension-catalog.json",
    "example": ROOT / "fixtures/v0.4.0-canonical-example.json",
    "legacy_schema": ROOT / "archive/v0.1.0/schema/hit-assessment.schema.json",
    "scorer_schema": ROOT / "validation/scorer-submission.schema.json",
    "a": ROOT / "validation/submissions/HIT-IR-SCORER-A.json",
    "b": ROOT / "validation/submissions/HIT-IR-SCORER-B.json",
    "comparison": ROOT / "validation/results/pre-adjudication-comparison.json",
    "verification": ROOT / "validation/receipts/scorer-transcription-verifications.json",
    "execution": ROOT / "validation/results/pre-adjudication-execution-record.json",
    "preservation": ROOT / "validation/results/preservation-manifest.json",
    "assets": ROOT / "validation/results/release-assets-manifest.json",
    "migration": ROOT / "case-studies/migrations/v0.4.0/migration-manifest.json",
    "protocol": ROOT / "validation/protocol-lock.json",
}

REQUIRED = {
    "README.md", "RESEARCH.md", "ROADMAP.md", "LIMITATIONS.md", "PROVENANCE.md",
    "CHANGELOG.md", "CITATION.cff", ".zenodo.json", "SPECIFICATION.md", "docs/citation.md",
    "compatibility/hit-compatibility-manifest.json", "docs/application-handbook.md",
    "docs/releases/v0.6.0.md", "docs/releases/v0.6.4.md", "docs/releases/v0.6.5.md", "docs/v0.6.0-release-readiness.md",
    "docs/decisions/ADR-0004-advance-hit-to-maturity-level-2.md",
    "validation/README.md", "validation/inter-rater-protocol.md", "validation/protocol-lock.json",
    "validation/scorer-submission.schema.json", "validation/submissions/HIT-IR-SCORER-A.json",
    "validation/submissions/HIT-IR-SCORER-B.json",
    "validation/receipts/HIT-IR-SCORER-A-original-incomplete.receipt.json",
    "validation/receipts/HIT-IR-SCORER-A-corrected-locked.receipt.json",
    "validation/receipts/HIT-IR-SCORER-B-locked.receipt.json",
    "validation/receipts/scorer-transcription-verifications.json",
    "validation/receipts/manual-to-JSON-transcription-audit.json",
    "validation/results/pre-adjudication-comparison.json",
    "validation/results/pre-adjudication-comparison.md",
    "validation/results/pre-adjudication-execution-record.json",
    "validation/results/preservation-manifest.json", "validation/results/release-assets-manifest.json",
    "validation/results/adjudication-record.md", "validation/results/H3-maturity-decision.md",
    "case-studies/migrations/v0.4.0/migration-manifest.json", "scripts/compare_raters.py",
    "scripts/validate_v040_boundaries.py", "scripts/validate_v040_migrations.py",
    "scripts/validate_v050_cli.py",
}

HISTORICAL = {
    "HIT-CASE-TOESLAGENAFFAIRE-HARM-2013-2019": ("case-studies/assessments/toeslagenaffaire-harm-period.json", "1f0a8099974ce0970df97d42cd4f10079e5e0e09"),
    "HIT-CASE-OBERMEYER-DEPLOYERS-2019": ("case-studies/assessments/obermeyer-deployers.json", "2290b4504156a0eaff0c4c6939bd67f9ee269e00"),
    "HIT-CASE-OBERMEYER-MANUFACTURER-2019": ("case-studies/assessments/obermeyer-manufacturer.json", "a0218f42e27afd8013af25c51ca3bc692ecab2a4"),
    "HIT-CASE-CIGNA-PXDX-2022-2025": ("case-studies/assessments/cigna-pxdx.json", "e1a9458b656b103f0160d89c02fc6da5cacab746"),
}

def read(path: str | Path) -> str:
    return (path if isinstance(path, Path) else ROOT / path).read_text(encoding="utf-8")

def load(path: str | Path) -> Any:
    return json.loads(read(path))

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def require(failures: list[str], path: str, value: str) -> None:
    if value not in read(path): failures.append(f"{path}: missing text: {value}")

def subcheck(path: str) -> list[str]:
    run = subprocess.run([sys.executable, str(ROOT / path)], cwd=ROOT, capture_output=True, text=True)
    return [] if run.returncode == 0 else [f"{path} failed:\n{(run.stdout + run.stderr).strip()}"]

def compare_module():
    spec = importlib.util.spec_from_file_location("hit_compare", ROOT / "scripts/compare_raters.py")
    if spec is None or spec.loader is None: raise RuntimeError("cannot load compare_raters.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def validate() -> list[str]:
    f: list[str] = []
    for item in sorted(REQUIRED):
        path = ROOT / item
        if not path.is_file() or path.stat().st_size == 0: f.append(f"missing or empty file: {item}")
    if f: return f

    schema, catalog, example = load(P["schema"]), load(P["catalog"]), load(P["example"])
    Draft202012Validator.check_schema(schema)
    if schema["properties"]["schema_version"].get("const") != CONTRACT: f.append("schema version changed")
    if schema["properties"]["specification_version"].get("const") != CONTRACT: f.append("specification version changed")
    if catalog.get("catalog_version") != CONTRACT: f.append("catalog version changed")
    result = validate_assessment(example, schema, source=str(P["example"].relative_to(ROOT)))
    f += [f"canonical example {x.code} {x.path}: {x.message}" for x in result.issues if not result.valid]
    if '"engine_version": "0.5.0"' not in read("compatibility/hit-compatibility-manifest.json"): f.append("compatibility engine changed")
    if '"engine_version": "0.5.0"' not in read("src/conformance/runner.py"): f.append("runner engine changed")

    legacy_validator = Draft202012Validator(load(P["legacy_schema"]), format_checker=FormatChecker())
    for assessment_id, (relative, expected_blob) in HISTORICAL.items():
        path, record = ROOT / relative, load(relative)
        f += [f"{relative}: {e.message}" for e in legacy_validator.iter_errors(record)]
        if record.get("assessment_id") != assessment_id or record.get("schema_version") != LEGACY: f.append(f"{relative}: identity changed")
        if git_blob(path) != expected_blob: f.append(f"{relative}: blob changed")
    migration = {x["assessment_id"]: x for x in load(P["migration"])["cases"]}
    expected_disp = {k: "historical_version_bound" for k in HISTORICAL}
    expected_disp["HIT-CASE-CIGNA-PXDX-2022-2025"] = "protocol_completed_historical_version_bound"
    if set(migration) != set(expected_disp): f.append("migration case set changed")
    else:
        for key, disposition in expected_disp.items():
            item = migration[key]
            if item.get("disposition") != disposition: f.append(f"{key}: migration disposition incorrect")
            if item.get("candidate_record_path") is not None or item.get("findings_changed") is not False: f.append(f"{key}: historical boundary weakened")

    lock = load(P["protocol"])
    locked = {"protocol_id":"HIT-IRP-CIGNA-001","protocol_version":"1.0.0","target_repository_release":"0.3.0","method_specification_version":"0.1.0","assessment_schema_version":"0.1.0","packet_id":"HIT-IR-CIGNA-PXDX-001","status":"locked","minimum_exact_agreements":6,"minimum_exact_agreement_proportion":0.8571,"critical_disagreements_allowed":0,"required_scorers":2,"author_may_score":False,"post_adjudication_rescoring_changes_primary_result":False,"failure_result_must_be_published":True}
    for key, value in locked.items():
        if lock.get(key) != value: f.append(f"protocol lock changed: {key}")

    for path, expected in ((P["a"], A_SHA), (P["b"], B_SHA), (P["comparison"], CMP_SHA)):
        if sha256(path) != expected: f.append(f"SHA-256 changed: {path.relative_to(ROOT)}")
    scorer_validator = Draft202012Validator(load(P["scorer_schema"]), format_checker=FormatChecker())
    module = compare_module()
    a = module.validate_submission(load(P["a"]), scorer_validator, "A")
    b = module.validate_submission(load(P["b"]), scorer_validator, "B")
    published = load(P["comparison"])
    if module.compare_submissions(a, b) != published: f.append("comparison recomputation mismatch")
    expected_result = {"items_compared":7,"exact_agreements":7,"exact_agreement_proportion":1.0,"critical_disagreement_count":0,"disagreements":[],"substantive_dimension_cohens_kappa":None,"advancement_threshold_met":True}
    for key, value in expected_result.items():
        if published.get(key) != value: f.append(f"comparison field incorrect: {key}")

    confirmations = {x["scorer_public_id"]: x for x in load(P["verification"])["confirmations"]}
    for scorer, digest in {"HIT-SCORER-A":A_SHA,"HIT-SCORER-B":B_SHA}.items():
        item = confirmations.get(scorer, {})
        if item.get("confirmation") != "Confirmed exact." or item.get("verified_json_sha256") != digest: f.append(f"{scorer}: verification incorrect")
    execution = load(P["execution"])
    if execution.get("inputs",{}).get("scorer_a_sha256") != A_SHA: f.append("execution A hash incorrect")
    if execution.get("inputs",{}).get("scorer_b_sha256") != B_SHA: f.append("execution B hash incorrect")
    if execution.get("outputs",{}).get("json_sha256") != CMP_SHA: f.append("execution comparison hash incorrect")
    if execution.get("pre_adjudication_frozen") is not True: f.append("pre-adjudication result not frozen")

    assets = load(P["assets"]); asset_map = {x.get("path"):x for x in assets.get("files",[])}
    binary = {
      "manual-submissions/HIT-SCORER-A/original-incomplete/HIT_Manual_Scorer_Packet_NonTechnical_v1.0.docx":"6d1674cd476879ce4792e6dbf55c8ea1b834da4ca8da7cf366d572506d0cceca",
      "manual-submissions/HIT-SCORER-A/corrected-locked/HIT_Manual_Scorer_Packet_NonTechnical_v1.0.docx":"53369878cd58f78a820f4281dacd6d83240dea7fd934d857fe64b3f0e3208567",
      "manual-submissions/HIT-SCORER-B/locked/HIT_Manual_Scorer_Packet_NonTechnical_v1.0.pdf":"f387874663ce8a52b7febc11f7b23ba339f71815bc47ea418496e6cfa7888cee"}
    for path, digest in binary.items():
        if asset_map.get(path,{}).get("sha256") != digest: f.append(f"asset hash incorrect: {path}")
    if assets.get("release_bundle",{}).get("sha256") != BUNDLE_SHA: f.append("bundle hash incorrect")
    if load(P["preservation"]).get("release_asset_bundle",{}).get("sha256") != BUNDLE_SHA: f.append("preservation bundle hash incorrect")

    citation, zenodo = yaml.safe_load(read("CITATION.cff")), load(".zenodo.json")
    f += validate_identity(citation, zenodo, load("release/v1.0.0/contract-freeze.candidate.json"))
    f += validate_citation_guidance(read("README.md"), read("docs/citation.md"))
    if citation.get("version") != CURRENT_RELEASE or citation.get("date-released") != CURRENT_RELEASE_DATE: f.append("citation metadata incorrect")
    if citation.get("doi") != CURRENT_VERSION_DOI: f.append("citation exact-version DOI incorrect")
    dois = {str(x.get("value")) for x in citation.get("identifiers",[]) if x.get("type") == "doi"}
    if dois != {SOFTWARE_CONCEPT_DOI}: f.append("citation software concept DOI incorrect")
    if zenodo.get("version") != CURRENT_RELEASE or zenodo.get("upload_type") != "software": f.append("Zenodo metadata incorrect")
    related_identifiers = zenodo.get("related_identifiers", [])
    if {"identifier": ORIGINATING_RESEARCH_DOI, "relation": "isSupplementTo", "resource_type": "dataset"} not in related_identifiers: f.append("Zenodo originating research relation incorrect")
    phrases = {
      "README.md":["**Current release:** 0.6.6","**Human-result release:** 0.6.0","**Conformance engine version:** 0.5.0","**Current maturity:** Level 2, Applicable","7 of 7 exact agreements"],
      "RESEARCH.md":["Current repository release: `0.6.6`","Software concept DOI: `10.5281/zenodo.21446141`","Version-specific software DOI for v0.6.5: `10.5281/zenodo.21864224`","Supported for one frozen Cigna packet","Level 2, Applicable"],
      "ROADMAP.md":["0.6.6: Development and reproducibility controls, current release"],
      "LIMITATIONS.md":["Narrow reliability evidence","Kappa indeterminacy"],
      "PROVENANCE.md":["Current repository release: 0.6.6","Originating research DOI: 10.5281/zenodo.21204892","Concept DOI for all HIT software versions: 10.5281/zenodo.21446141","Version-specific software DOI for `v0.6.5`: 10.5281/zenodo.21864224","Version-specific software DOI for `v0.6.4`: 10.5281/zenodo.21446142","Research maturity: Level 2, Applicable"],
      "CHANGELOG.md":["## [0.6.5] - 2026-08-09","## [0.6.4] - 2026-07-19","## [0.6.0] - 2026-07-18","Exact agreements: 7 of 7"],
      "docs/releases/v0.6.0.md":["Maturity Level 2, Applicable","Conformance engine: `0.5.0`"],
      "docs/releases/v0.6.4.md":["Concept DOI, all software versions","10.5281/zenodo.21446141","10.5281/zenodo.21446142","Human-result release: `0.6.0`"],
      "docs/releases/v0.6.5.md":["Status:** Published","Concept DOI, all software versions","10.5281/zenodo.21446141","Version-specific software DOI:** [10.5281/zenodo.21864224]","Human-result release:** `0.6.0`"],
      "docs/v0.6.0-release-readiness.md":["Tagging and release publication require separate maintainer approval"],
      "validation/results/H3-maturity-decision.md":["Level 2, Applicable"],
      "validation/results/adjudication-record.md":["No substantive adjudication required"],
      "case-studies/README.md":["protocol_completed_historical_version_bound"]}
    for path, values in phrases.items():
        for value in values: require(f, path, value)
    return f

def main() -> int:
    failures = validate()
    if not failures:
        for path in ("scripts/validate_v040_boundaries.py","scripts/validate_v040_migrations.py","scripts/validate_v050_cli.py"):
            failures += subcheck(path)
    if failures:
        for item in failures: print(f"FAIL: {item}")
        return 1
    print("HIT 0.6.0 result package and current release metadata checks passed")
    print(f"- current repository release metadata: {CURRENT_RELEASE}; human-result release: 0.6.0")
    print(f"- current exact-version DOI: {CURRENT_VERSION_DOI or 'pending verification'}")
    print("- software concept DOI: 10.5281/zenodo.21446141")
    print("- originating research DOI: 10.5281/zenodo.21204892")
    print("- v0.6.5 version DOI: 10.5281/zenodo.21864224")
    print("- previous v0.6.4 DOI: 10.5281/zenodo.21446142")
    print("- engine 0.5.0; contract 0.4.0; scorer contract 0.1.0")
    print("- exact agreement: 7 / 7; critical disagreements: 0")
    print("- H3 supported for one frozen packet; maturity Level 2, Applicable")
    return 0

if __name__ == "__main__": raise SystemExit(main())
