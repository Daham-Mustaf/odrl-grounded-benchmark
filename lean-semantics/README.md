# Lean mechanization of the grounded ODRL semantics

Mechanizes "Denotational Semantics for Externally-Grounded ODRL Policies".
Core Lean only, no Mathlib yet. Build from this folder:

    lake build

| File | Paper |
|---|---|
| OdrlGrounded/Model.lean | Resource and background theory, Structure, Models |
| OdrlGrounded/Syntax.lean | Signature and well-sortedness, constraint sets |
| OdrlGrounded/Semantics.lean | Denotation, Valuation and satisfaction |
| OdrlGrounded/Verdict.lean | Verdict (one operand) |
| OdrlGrounded/Examples/Language.lean | Figure 1, language row |

Later steps add Witness.lean, Collapse.lean, Factoring.lean and Checker.lean,
and Examples/Purpose.lean and Examples/Spatial.lean.
