# Design notes

## Trust boundary

The JSON Schema and graph validator establish structural consistency. Lean establishes that a formal proposition typechecks. Neither mechanism proves that the LaTeX statement is a perfect translation of the Lean statement, so paired-representation review remains part of knowledge-base maintenance.

An SFT record receives `verified: true` only after its `formal_proof` is accepted by `lake env lean`. Skip mode is intended for pipeline development and always leaves `verified` false.

## Graph semantics

`prerequisites` is a directed acyclic graph and is checked for missing references, self-edges, and cycles. `related` is an undirected editorial relationship in practice, although symmetry is not required by the schema. `parents` refers to taxonomy nodes and therefore does not have to resolve to another atomic item.

## Growth path

1. Add atomic items with reviewed LaTeX and Lean declarations.
2. Add generators only after their output family has a meaningful proof certificate.
3. Introduce graph-path composition for multi-concept questions.
4. Add semantic near-duplicate detection and measured difficulty calibration.
5. Evaluate the resulting training data on a held-out mathematical reasoning benchmark.
