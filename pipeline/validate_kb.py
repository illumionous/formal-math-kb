from __future__ import annotations

import argparse
from pathlib import Path

from .knowledge import load_knowledge_base
from .lean import LeanVerifier


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the knowledge schema, graph, and Lean statements")
    parser.add_argument("--kb", type=Path, required=True)
    parser.add_argument("--lean", choices=("auto", "required", "skip"), default="auto")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    points = load_knowledge_base(args.kb)
    verifier = LeanVerifier(args.project_root, args.lean)
    failures: list[str] = []
    if verifier.enabled:
        for point in points.values():
            result = verifier.check(point.statement_lean)
            if not result.accepted:
                failures.append(f"{point.id}: {result.diagnostics}")
    elif args.lean == "auto":
        print("warning: Lean unavailable; schema and graph were checked, statements were not compiled")

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"knowledge_points={len(points)} graph=valid lean={'valid' if verifier.enabled else 'skipped'}")


if __name__ == "__main__":
    main()
