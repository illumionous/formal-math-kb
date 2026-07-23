from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .io import read_jsonl, write_jsonl
from .lean import LeanVerifier

REQUIRED_EXAMPLE_FIELDS = {
    "instruction": str,
    "reasoning": str,
    "answer": str,
    "kb_ids": list,
    "formal_proof": str,
    "difficulty": int,
    "verified": bool,
}


def validate_example(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field, expected_type in REQUIRED_EXAMPLE_FIELDS.items():
        if field not in record:
            errors.append(f"missing field: {field}")
        elif not isinstance(record[field], expected_type):
            errors.append(f"{field} must be {expected_type.__name__}")
    if isinstance(record.get("kb_ids"), list) and (
        not record["kb_ids"] or not all(isinstance(item, str) for item in record["kb_ids"])
    ):
        errors.append("kb_ids must be a non-empty string array")
    for field in ("instruction", "reasoning", "answer", "formal_proof"):
        if isinstance(record.get(field), str) and not record[field].strip():
            errors.append(f"{field} must not be empty")
    return errors


def verify_records(
    records: list[dict[str, Any]], verifier: LeanVerifier
) -> tuple[list[dict[str, Any]], int]:
    output: list[dict[str, Any]] = []
    accepted = 0
    for record in records:
        candidate = dict(record)
        errors = validate_example(candidate)
        if errors:
            candidate["verified"] = False
            candidate["verification_error"] = "; ".join(errors)
        else:
            result = verifier.check(candidate["formal_proof"])
            candidate["verified"] = result.accepted
            if result.accepted:
                candidate.pop("verification_error", None)
                accepted += 1
            else:
                candidate["verification_error"] = result.diagnostics
        output.append(candidate)
    return output, accepted


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify SFT proof certificates with Lean")
    parser.add_argument("--in", dest="input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--lean", choices=("auto", "required", "skip"), default="auto")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    records = list(read_jsonl(args.input))
    output, accepted = verify_records(records, LeanVerifier(args.project_root, args.lean))
    write_jsonl(args.out, output)
    print(f"checked={len(records)} accepted={accepted} rejected={len(records) - accepted} output={args.out}")


if __name__ == "__main__":
    main()
