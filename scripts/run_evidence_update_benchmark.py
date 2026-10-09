#!/usr/bin/env python3
"""Score explicit constructed updates; never create observed trial responses."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "research/strengthening/evidence-update-001"
STUDY = "HIT-EU-001"
METHODS = ("hit_graph", "structured_table")
CLAIMS = tuple(f"P{i:02}" for i in range(1, 9))
QUALS = tuple(f"Q{i:02}" for i in range(1, 8))
SCENARIOS = tuple(f"U{i:02}" for i in range(5))
STATES = {"supported", "limited_support", "unsupported", "unresolved", "conflicted"}
FROZEN = tuple(f"{BASE}/{name}" for name in (
    "PROTOCOL.md", "README.md", "inputs/instructions.md", "inputs/dossier.json",
    "inputs/updates.json", "inputs/hit_graph.json", "inputs/structured_table.json",
    "inputs/oracle.json")) + (
    "scripts/run_evidence_update_benchmark.py", "scripts/test_evidence_update_benchmark.py")


def require(value, message):
    if not value:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()


def decoded(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda _: require(False, "nonfinite number"))


def raw(root, path):
    target = root / path
    require(not Path(path).is_absolute() and ".." not in Path(path).parts,
            "unsafe input path")
    require(target.resolve().is_relative_to(root.resolve()), "input escapes repository")
    cursor = target
    while cursor != root:
        require(not cursor.is_symlink(), "symlink input prohibited")
        cursor = cursor.parent
    require(target.is_file(), f"missing input: {path}")
    return target.read_bytes()


def load(root, name):
    return decoded(raw(root, f"{BASE}/{name}"))


def sha(value):
    return hashlib.sha256(value).hexdigest()


def ordered(rows, ids, label):
    require(isinstance(rows, list) and all(isinstance(x, dict) for x in rows)
            and [x.get("id") for x in rows] == list(ids), f"invalid {label} rows")
    return rows


def text(value):
    return isinstance(value, str) and bool(value.strip())


def keys(value, names, label):
    require(isinstance(value, dict) and set(value) == set(names.split()), f"invalid {label} fields")


def permitted(method):
    return [f"{BASE}/inputs/{name}" for name in
            ("instructions.md", "dossier.json", "updates.json", f"{method}.json")]


def manifest(root):
    return {path: sha(raw(root, path)) for path in FROZEN}


def prepare(root):
    design = load(root, "design.json")
    require(design["study_id"] == STUDY and design["frozen_sha256"] == manifest(root),
            "frozen manifest mismatch")
    dossier = load(root, "inputs/dossier.json")
    require(dossier["synthetic"] is True, "fixture must remain explicitly synthetic")
    sources = [x["id"] for x in dossier["sources"]]
    require(sources == ["S01", "S02", "S03", "S04"], "unexpected original sources")
    qualifications = ordered(dossier["qualifications"], QUALS, "qualification")
    for row in qualifications:
        require(text(row["text"]) and len(row["allowed_states"]) == len(set(row["allowed_states"])),
                "invalid qualification choices")
    graph = load(root, "inputs/hit_graph.json")
    table = load(root, "inputs/structured_table.json")
    require(graph["method_id"] == METHODS[0] and table["method_id"] == METHODS[1], "method mismatch")
    propositions = ordered(graph["propositions"], CLAIMS, "graph proposition")
    table_rows = ordered(table["review_rows"], CLAIMS, "table proposition")
    relations = graph["relations"]
    require(len(relations) == len({(r["from"], r["type"], r["to"]) for r in relations}),
            "duplicate graph relation")
    canonical = []
    for p in propositions:
        links = {kind: sorted(r["to"] for r in relations if r["from"] == p["id"] and r["type"] == kind)
                 for kind in ("evidence", "qualification")}
        canonical.append({k: p[k] for k in ("id", "text", "initial_status")} |
                         {"evidence_refs": links["evidence"], "qualification_refs": links["qualification"]})
    normalized = [{k: v for k, v in row.items() if k != "navigation"} for row in table_rows]
    normalized = [row | {"evidence_refs": sorted(row["evidence_refs"]),
                          "qualification_refs": sorted(row["qualification_refs"])} for row in normalized]
    require(canonical == normalized, "method packets have unequal semantic content")
    for relation in relations:
        require(relation["from"] in CLAIMS and relation["type"] in {"evidence", "qualification"}
                and relation["to"] in (sources if relation["type"] == "evidence" else QUALS),
                "unknown graph reference")
    updates = ordered(load(root, "inputs/updates.json")["scenarios"], SCENARIOS, "update")
    oracle = ordered(load(root, "inputs/oracle.json")["scenarios"], SCENARIOS, "oracle")
    for update, expected in zip(updates, oracle):
        require(set(expected["claim_states"]) == set(CLAIMS)
                and set(expected["claim_states"].values()) <= STATES, "invalid oracle claim states")
        require(set(expected["qualification_states"]) == set(QUALS), "invalid oracle qualifications")
        require(set(expected["affected_claims"]) <= set(CLAIMS)
                and len(expected["affected_claims"]) == len(set(expected["affected_claims"])), "invalid affected claims")
        for q in qualifications:
            require(expected["qualification_states"][q["id"]] in q["allowed_states"],
                    "invalid oracle qualification state")
        require(set(update["withdrawn_sources"]) <= set(sources), "unknown withdrawn source")
    require(sum(len(row["affected_claims"]) for row in oracle) == 4, "expected four injected impacts")
    return dossier, updates, oracle


def committed(root, commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=root,
                                   stderr=subprocess.DEVNULL)


def verify_freeze(root, commit):
    require(isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit), "invalid freeze commit")
    for path in (*FROZEN, f"{BASE}/design.json"):
        require(committed(root, commit, path) == raw(root, path), f"post-freeze input change: {path}")


def inspect_response(root, method, data, dossier, updates):
    keys(data, "study_id method_id protocol_commit input_sha256 executor independent_review "
         "author_review access_declaration scenarios", "response")
    require(data["study_id"] == STUDY and data["method_id"] == method, "response identity mismatch")
    require(data["executor"] == "ai_assistant" and data["independent_review"] is False
            and data["author_review"] == "pending", "unsupported review promotion")
    require(text(data["access_declaration"]), "missing access declaration")
    require(data["input_sha256"] == {p: sha(raw(root, p)) for p in permitted(method)},
            "response input digest mismatch")
    verify_freeze(root, data["protocol_commit"])
    rows = ordered(data["scenarios"], SCENARIOS, "response scenario")
    original_sources = {s["id"] for s in dossier["sources"]}
    choices = {q["id"]: q["allowed_states"] for q in dossier["qualifications"]}
    for row, update in zip(rows, updates):
        keys(row, "id claims qualifications", "scenario")
        allowed = original_sources | {s["id"] for s in update["new_sources"]}
        for claim in ordered(row["claims"], CLAIMS, "response claim"):
            keys(claim, "id action status updated_statement evidence_refs rationale", "claim")
            require(claim["action"] in {"retain", "revise"} and claim["status"] in STATES,
                    "invalid claim action or support state")
            require(text(claim["updated_statement"]) and text(claim["rationale"]), "missing claim prose")
            refs = claim["evidence_refs"]
            require(isinstance(refs, list) and all(isinstance(r, str) for r in refs)
                    and len(refs) == len(set(refs)) and set(refs) <= allowed, "unknown or duplicate evidence reference")
        for qual in ordered(row["qualifications"], QUALS, "response qualification"):
            keys(qual, "id state rationale", "qualification")
            require(qual["state"] in choices[qual["id"]] and text(qual["rationale"]), "invalid qualification answer")
    return rows


def score(rows, oracle):
    details = []
    total = {"affected_true_positive": 0, "affected_missed": 0, "unaffected_false_positive": 0,
             "unaffected_correctly_retained": 0, "claim_state_matches": 0,
             "qualification_state_matches": 0, "content_token_matches": 0}
    for row, expected in zip(rows, oracle):
        actual = {c["id"] for c in row["claims"] if c["action"] == "revise"}
        affected = set(expected["affected_claims"])
        state_errors = [c["id"] for c in row["claims"] if c["status"] != expected["claim_states"][c["id"]]]
        qual_errors = [q["id"] for q in row["qualifications"]
                       if q["state"] != expected["qualification_states"][q["id"]]]
        content = []
        if row["id"] == "U02":
            statement = row["claims"][0]["updated_statement"]
            content.append({"item": "corrected_direction_date", "matches":
                            bool(re.search(r"18(?:th)? August 2040|2040-08-18", statement))})
        if row["id"] == "U04":
            statement = row["claims"][4]["updated_statement"]
            content.append({"item": "five_recipient_identifiers", "matches":
                            all(re.search(rf"\bA{i:02}\b", statement) for i in range(1, 6))})
        total["affected_true_positive"] += len(actual & affected)
        total["affected_missed"] += len(affected - actual)
        total["unaffected_false_positive"] += len(actual - affected)
        total["unaffected_correctly_retained"] += len(set(CLAIMS) - actual - affected)
        total["claim_state_matches"] += len(CLAIMS) - len(state_errors)
        total["qualification_state_matches"] += len(QUALS) - len(qual_errors)
        total["content_token_matches"] += sum(c["matches"] for c in content)
        details.append({"id": row["id"], "missed_claims": sorted(affected - actual),
                        "false_positive_claims": sorted(actual - affected),
                        "wrong_claim_states": state_errors, "wrong_qualification_states": qual_errors,
                        "narrow_content_checks": content})
    return {"denominators": {"affected": 4, "unchanged": 36, "claim_states": 40,
                             "qualification_states": 35, "content_token_checks": 2},
            "counts": total, "scenarios": details}


def analyze(root):
    dossier, updates, oracle = prepare(root)
    results, commits, response_hashes = {}, set(), {}
    for method in METHODS:
        path = f"{BASE}/responses/{method}.json"
        response = decoded(raw(root, path))
        rows = inspect_response(root, method, response, dossier, updates)
        results[method] = score(rows, oracle)
        commits.add(response["protocol_commit"])
        response_hashes[path] = sha(raw(root, path))
    require(len(commits) == 1, "methods must share a freeze commit")
    return {"study_id": STUDY, "protocol_commit": commits.pop(), "response_sha256": response_hashes,
            "status": "completed_pending_author_review", "executor": "ai_assistant",
            "independent_review": False, "semantic_prose_validated": False,
            "historical_truth_validated": False, "comparative_utility_established": False,
            "release_gate_satisfied": False, "scientific_conclusion_eligible": False,
            "methods": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--analyze", action="store_true")
    args = parser.parse_args()
    try:
        if args.prepare:
            prepare(ROOT)
            result = {"study_id": STUDY, "status": "prepared", "trial_executed": False,
                      "semantic_input_equivalence": True, "release_gate_satisfied": False}
        else:
            result = analyze(ROOT)
        print(encoded(result).decode(), end="")
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
