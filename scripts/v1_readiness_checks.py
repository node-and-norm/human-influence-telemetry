"""Shared fail-closed checks for the candidate v1 records.

These checks verify file presence and declared bytes. They cannot verify source
truth, reviewer identity, or scientific acceptance. Completion-state acceptance
requires a separately reviewed policy; the supported lifecycle is candidate only.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator


SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def checked_path(root: Path, value: Any, failures: list[str], label: str) -> Path | None:
    """Require a nonempty, canonical repo-relative path to a contained file."""
    if not isinstance(value, str) or not value or "\\" in value:
        failures.append(f"{label}: expected a nonempty POSIX repository-relative path")
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in value.split("/")):
        failures.append(f"{label}: unsafe or noncanonical repository-relative path: {value}")
        return None
    candidate = root / value
    try:
        candidate.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, RuntimeError, ValueError):
        failures.append(f"{label}: missing artifact or path escapes repository: {value}")
        return None
    if not candidate.is_file() or candidate.stat().st_size == 0:
        failures.append(f"{label}: artifact is not a nonempty regular file: {value}")
        return None
    return candidate


def check_artifacts(
    root: Path, records: Any, failures: list[str], *, hashes_required: bool = False,
) -> None:
    """Check declared file bytes, while making no claim about their adequacy."""
    if not isinstance(records, list) or not records:
        failures.append("required_artifacts must be a nonempty list")
        return
    seen: set[str] = set()
    for index, item in enumerate(records):
        label = f"required_artifacts[{index}]"
        if not isinstance(item, dict):
            failures.append(f"{label}: expected an object")
            continue
        value = item.get("path")
        path = checked_path(root, value, failures, label)
        if isinstance(value, str):
            if value in seen:
                failures.append(f"{label}: duplicate artifact: {value}")
            seen.add(value)
        digest = item.get("sha256")
        if digest is None and not hashes_required:
            continue
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            failures.append(f"{label}: missing or invalid SHA-256")
        elif path is not None and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            failures.append(f"{label}: SHA-256 mismatch: {value}")


def check_eligibility_record(root: Path, reference: Any, failures: list[str]) -> None:
    """Check an optional candidate declaration without authenticating its signer.

    A declaration is necessary, never sufficient. This function cannot establish
    real-world independence. Promotion still needs the separately reviewed audit
    acceptance policy and the maintainer's evidence-backed decision.
    """
    if not isinstance(reference, dict):
        failures.append("independent_auditor_eligibility_record must declare path and sha256")
        return
    check_artifacts(root, [reference], failures, hashes_required=True)
    path = checked_path(root, reference.get("path"), failures, "auditor eligibility")
    if path is None:
        return
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        failures.append(f"auditor eligibility is not readable JSON: {exc}")
        return
    if not isinstance(record, dict):
        failures.append("auditor eligibility must be an object")
        return
    schema_path = checked_path(
        root, "implementation/v1.0.0-candidate/audit-submission.schema.json",
        failures, "published auditor schema",
    )
    if schema_path is None:
        return
    public_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    auditor_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": "#/$defs/auditor", "$defs": public_schema["$defs"],
    }
    Draft202012Validator.check_schema(auditor_schema)
    for error in Draft202012Validator(auditor_schema).iter_errors(record):
        failures.append(f"auditor eligibility: {error.json_path}: {error.message}")
    for field in (
        "human_supplied_declarations", "is_human", "not_hit_author",
        "no_material_packet_contribution", "used_public_material_only",
    ):
        if record.get(field) is not True:
            failures.append(f"independent human auditor eligibility requires {field}=true")
    for field in ("identity", "competence", "conflicts", "prior_exposure"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            failures.append(f"auditor eligibility missing {field}")
    # Avoid treating a contradictory self-description as an independent person.
    if str(record.get("identity", "")).strip().casefold() in {
        "mark julius banasihan", "mark banasihan", "mj3b", "codex", "chatgpt",
        "claude", "jev", "assistant", "author",
    }:
        failures.append("auditor identity identifies the author or an AI system")
