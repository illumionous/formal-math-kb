from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Any, Iterable

from .io import read_jsonl, write_jsonl


def fingerprint(record: dict[str, Any]) -> str:
    instruction = re.sub(r"\s+", " ", record.get("instruction", "").strip().lower())
    answer = re.sub(r"\s+", " ", record.get("answer", "").strip().lower())
    return hashlib.sha256(f"{instruction}\n{answer}".encode()).hexdigest()


def deduplicate(records: Iterable[dict[str, Any]], include_unverified: bool = False) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    for record in records:
        if not include_unverified and not record.get("verified", False):
            continue
        key = fingerprint(record)
        if key in seen:
            continue
        seen.add(key)
        output.append(record)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove deterministic duplicates from SFT JSONL")
    parser.add_argument("--in", dest="input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--include-unverified", action="store_true")
    args = parser.parse_args()
    records = list(read_jsonl(args.input))
    output = deduplicate(records, args.include_unverified)
    write_jsonl(args.out, output)
    print(f"input={len(records)} output={len(output)} removed={len(records) - len(output)}")


if __name__ == "__main__":
    main()
