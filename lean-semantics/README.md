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
| OdrlGrounded/Grounding.lean | Grounding, candidate set, ungrounded clause |
| OdrlGrounded/VerdictProperties.lean | Exclusivity, monotonicity, soundness |
| OdrlGrounded/Witness.lean | Witness lemma for a conjunction of atoms |
| OdrlGrounded/Disjuncts.lean | Reduction of a constraint set to disjuncts, with or, xone and negation |
| OdrlGrounded/Decision.lean | Computing verdicts: the two entailment queries |
| OdrlGrounded/Factoring.lean | Operand independence, operand-wise factoring |
| OdrlGrounded/Examples/Language.lean | Figure 1, language row |
| OdrlGrounded/Examples/Grounding.lean | Language row with values, ungrounded alternative |
| OdrlGrounded/Examples/Purpose.lean | Figure 1, purpose row: `Compatible`, with a model of the published assertion |
| OdrlGrounded/Examples/Spatial.lean | Figure 1, place row: `Compatible`, with a model of the published assertion |
| OdrlGrounded/Examples/Verdicts.lean | All three verdicts under consistent theories, an inconsistent theory, well-sortedness |
| OdrlGrounded/Audit.lean | `#print axioms` for the main theorems and examples |

Folder `crosscheck/` holds the brute-force Python checks of the same
claims, with a table of which Lean theorem covers which check.

Axiom check:

    lake build OdrlGrounded.Audit 2>&1 | grep -E "axioms|error|sorry"

A later step adds Checker.lean.
