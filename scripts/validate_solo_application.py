"""Replay conditional rubric checks; never certify documentary interpretations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.rubric.rules_v040 import evaluate_fr04, evaluate_fr09


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    base = ROOT / "research/strengthening/solo-001"
    packet = json.loads((base / "cases.json").read_text())
    if (packet["kind"] != "synthetic_conditional_rule_checks"
            or packet["human_adjudication"] != "pending"
            or packet["current_contract_assessment"] is not False):
        raise ValueError("Unsupported promotion of documentary or human evidence")
    cases = packet["cases"]
    if [case["id"] for case in cases] != [f"A{i:02}" for i in range(1, 7)]:
        raise ValueError("Missing, reordered, or duplicated planned case")
    evaluators = {"FR-04": evaluate_fr04, "FR-09": evaluate_fr09}
    observations = []
    for case in cases:
        actual = evaluators[case["rule"]](case["facts"])
        observations.append({"id": case["id"], "actual": actual,
                             "expected": case["expected"], "pass": actual == case["expected"]})
    paths = [base / name for name in ("plan.md", "dossier.md", "cases.json")]
    paths += [Path(__file__).resolve(), ROOT / "src/rubric/rules_v040.py"]
    result = {"study": packet["study"], "scope": packet["kind"],
              "documentary_interpretation_validated": False,
              "human_adjudication": "pending",
              "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in paths}, "observations": observations}
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    output = base / "results.json"
    if args.write:
        output.write_text(rendered)
    elif not output.exists() or output.read_text() != rendered:
        print("FAIL: retained solo results are missing or stale")
        return 1
    passed = sum(item["pass"] for item in observations)
    print(f"Conditional rule checks: {passed}/{len(observations)}. Documentary adjudication pending.")
    return 0 if passed == len(observations) else 1


if __name__ == "__main__":
    raise SystemExit(main())
