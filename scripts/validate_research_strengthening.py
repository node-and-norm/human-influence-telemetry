#!/usr/bin/env python3
"""Reproduce supplementary synthetic tests; no network or model inference."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.rubric.rules_v040 import evaluate_boundary_case

WORK = ROOT / "research/strengthening"


def load(name):
    return json.loads((WORK / name).read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def build():
    audit = load("claim-audit.json")
    require(audit["external_replication"] == "unresolved", "Replication cannot be promoted here")
    seen = set()
    for finding in audit["findings"]:
        require(finding["id"] not in seen, "Duplicate audit identifier")
        seen.add(finding["id"])
        target = (ROOT / finding["path"]).resolve()
        require(target.is_relative_to(ROOT), "Audit path escapes repository")
        require(finding["locator"] in target.read_text(encoding="utf-8"), f"Unresolved locator: {finding['id']}")
    rows = []
    suite = load("adversarial-cases.json")
    require(suite["evidence_class"] == "E1_synthetic", "Synthetic evidence boundary missing")
    seen = set()
    require(len(suite["cases"]) == 16, "Review changes to the declared 16-test schedule")
    for case in suite["cases"]:
        require(case["id"] not in seen, "Duplicate adversarial identifier")
        seen.add(case["id"])
        actual = evaluate_boundary_case(case["rule"], case["facts"])
        require(actual == case["expected"], f"{case['id']}: expected {case['expected']}, got {actual}")
        rows.append({"id": case["id"], "expected": case["expected"], "actual": actual, "match": True})
    utility = []
    cases = load("utility-cases.json")
    require(cases["evidence_class"] == "E1_synthetic", "Utility demonstration boundary missing")
    require(len(cases["cases"]) == 4, "Review changes to the four-case demonstration")
    seen = set()
    for case in cases["cases"]:
        require(case["id"] not in seen, "Duplicate utility identifier")
        seen.add(case["id"])
        facts = case["facts"]
        presence = "present" if facts.get("formal_authority") else "absent" if facts.get("no_named_human_authority") else "unknown"
        hit = evaluate_boundary_case("FR-06", facts)["finding"]
        require(presence == case["expected_presence"] and hit == case["expected_hit"], f"Utility mismatch: {case['id']}")
        utility.append({"id": case["id"], "human_presence": presence, "hit_command": hit})
    inputs = [WORK / name for name in ("claim-audit.json", "adversarial-cases.json", "utility-cases.json")]
    inputs += [ROOT / "src/rubric/rules_v040.py", Path(__file__).resolve()]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    return {"status": "PASS_SYNTHETIC_ONLY", "human_review": "pending", "external_replication": "unresolved", "input_sha256": hashes, "audit_locator_count": len(audit["findings"]), "adversarial_results": rows, "utility_demonstration": utility, "participant_count": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = build()
        content = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        output = WORK / "results.json"
        if args.write:
            output.write_text(content, encoding="utf-8")
        else:
            require(output.read_text(encoding="utf-8") == content, "Generated result is stale; review inputs and regenerate")
        print(f"PASS: {result['audit_locator_count']} locators, {len(result['adversarial_results'])} adversarial tests, {len(result['utility_demonstration'])} synthetic comparisons; no participant result")
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
