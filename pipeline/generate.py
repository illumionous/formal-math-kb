from __future__ import annotations

import argparse
import random
from pathlib import Path

from .io import write_jsonl
from .knowledge import load_knowledge_base
from .templates import GENERATORS


def generate_records(kb_root: Path, count: int, seed: int) -> list[dict]:
    if count < 1:
        raise ValueError("--n must be positive")
    points = load_knowledge_base(kb_root)
    rng = random.Random(seed)
    records: list[dict] = []
    for index in range(count):
        generator = GENERATORS[index % len(GENERATORS)]
        example = generator(rng)
        unknown = set(example.kb_ids) - points.keys()
        if unknown:
            raise ValueError(f"generator emitted unknown knowledge ids: {sorted(unknown)}")
        records.append(example.to_dict())
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate formal-mathematics SFT examples")
    parser.add_argument("--kb", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    count = write_jsonl(args.out, generate_records(args.kb, args.n, args.seed))
    print(f"generated={count} output={args.out}")


if __name__ == "__main__":
    main()
