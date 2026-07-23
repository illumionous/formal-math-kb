# Formal Math Knowledge Base

Formalized high-school mathematics concepts and a small, reproducible pipeline for producing machine-checked supervised fine-tuning (SFT) examples.

This repository is an honest MVP of the larger dataset design. It currently contains **12 representative knowledge points** across algebra, functions, sequences, trigonometry, geometry, and probability. The architecture is designed to grow to hundreds of atomic concepts; the number of formalized items is reported by the repository itself rather than claimed in advance.

## Why formalize the source?

Most mathematical SFT corpora are checked by sampling or human review. Here, every generated example carries a Lean proof certificate. The verifier invokes the Lean compiler and discards samples whose formal counterpart does not typecheck. This proves the formal claim; it does not by itself guarantee that a natural-language explanation is pedagogically excellent.

## Repository layout

```text
schema/       JSON Schema for atomic knowledge points
kb/           one JSON file and one Lean module per concept
FormalMathKB/ Lean library importing the formalized concepts
pipeline/     generation, validation, Lean verification, and deduplication
tests/        Python unit tests
data/         generated datasets (kept out of Git by default)
```

## Quick start

```bash
# Python side (Python 3.10+)
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m unittest discover -s tests -v

# Lean side (Lean 4 + Mathlib)
lake exe cache get
lake build

# Generate, verify, and deduplicate examples
python -m pipeline.generate --kb kb --out /tmp/sft.jsonl --n 50 --seed 7
python -m pipeline.verify --in /tmp/sft.jsonl --out /tmp/sft.verified.jsonl --lean required
python -m pipeline.dedup --in /tmp/sft.verified.jsonl --out /tmp/sft.final.jsonl
```

When Lean is not installed, use `--lean skip` for pipeline development. The CI workflow always runs the Lean build and required verification.

## Data contract

Each knowledge item is atomic: one definition, theorem, or solvable technique. It has paired LaTeX and Lean representations plus graph provenance:

```json
{
  "id": "alg.linear.solve",
  "title": "Solving a non-degenerate linear equation",
  "level": 1,
  "parents": ["alg.linear"],
  "prerequisites": [],
  "related": ["alg.quadratic.vieta"],
  "statement_latex": "For a ≠ 0, ax + b = c has the unique solution x = (c-b)/a.",
  "statement_lean": "theorem ... := by ...",
  "tags": ["algebra", "equations"]
}
```

Generated records contain `instruction`, `reasoning`, `answer`, `kb_ids`, `formal_proof`, and `verified`. The `kb_ids` field preserves provenance for auditing and curriculum construction.

## Current scope and limitations

- The checked knowledge base is a representative starter set, not 664 completed concepts.
- The generator currently uses deterministic templates for a few elementary problem families.
- Lean verification checks the formal counterpart and proof certificate. It cannot judge whether a prose trace is clear, original, or free of hidden assumptions.
- No fine-tuning benchmark result is claimed yet.

## License

MIT
