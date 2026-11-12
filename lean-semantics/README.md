# Lean mechanization of the grounded ODRL semantics

Mechanizes "Denotational Semantics and Open-World Reasoning for Externally-Grounded ODRL Constraints".
Core Lean only, no Mathlib. Build from this folder:

    lake build

| File | Paper |
|---|---|
| OdrlGrounded/Model.lean | Binding, Structure, Models |
| OdrlGrounded/Syntax.lean | Well-sortedness, constraint sets |
| OdrlGrounded/Semantics.lean | Denotation, Satisfaction of constraints |
| OdrlGrounded/Verdict.lean | Verdict (one operand) |
| OdrlGrounded/Grounding.lean | Grounding, concept set, rejection of an ungrounded value |
| OdrlGrounded/VerdictProperties.lean | Exclusivity, adding statements, soundness |
| OdrlGrounded/Witness.lean | Lemma "Formula and valuations", for a conjunction of atoms |
| OdrlGrounded/Disjuncts.lean | Reduction of a constraint set to cases, with or, xone and negation |
| OdrlGrounded/Decision.lean | Proposition "Three checks": the two entailment queries |
| OdrlGrounded/Factoring.lean | Proposition "Verdict by left operand" |
| OdrlGrounded/Examples/Language.lean | Running example, language row |
| OdrlGrounded/Examples/Grounding.lean | Language row with values, ungrounded alternative |
| OdrlGrounded/Examples/Purpose.lean | Running example, purpose row: `Compatible`, with a model of the published statement |
| OdrlGrounded/Examples/Spatial.lean | Running example, place row: `Compatible`, with a model of the published statement |
| OdrlGrounded/Examples/Verdicts.lean | All three verdicts under consistent statements, inconsistent statements, well-sortedness |
| OdrlGrounded/Audit.lean | `#print axioms` for the main theorems and examples |

Folder `crosscheck/` holds the brute-force Python checks of the same
claims, with a table of which Lean theorem covers which check.

Axiom check:

    lake build OdrlGrounded.Audit 2>&1 | grep -E "axioms|error|sorry"

## Paper to Lean

| Paper | Lean | File |
|---|---|---|
| Well-sortedness | `Atom.wellSorted`, `Item.wellSorted`, `ConstraintSet.xoneOk_of_wellSorted` | Syntax.lean |
| Binding, declarations, models | `Statement`, `ConceptOrder`, `Mod`, `Consistent` | Model.lean |
| Disjointness excludes identity and order | `ConceptOrder.not_le_of_disjoint`, `ConceptOrder.not_eqv_of_disjoint` | Model.lean |
| Structure with unnamed elements | `Structure`, `structVerdict` | Collapse.lean |
| Grounding, ungrounded clause | `Grounding`, `Grounding.range`, `groundedVerdict`, `groundedVerdict_of_left_none`, `groundedVerdict_of_right_none` | Grounding.lean |
| The concept set of the left operand, Definition 4 (Grounding); not the N of Definition 10 (Formula of a case) | `N` | Semantics.lean, Grounding.lean |
| Denotation, satisfaction of constraints | `Atom.denot`, `ConceptOrder.satAtom`, `ConceptOrder.satItem`, `ConceptOrder.satSet`, `ConceptOrder.admits` | Semantics.lean |
| Verdict | `Compatible`, `Incompatible`, `verdict`, `verdict_eq_compatible_iff`, `verdict_eq_incompatible_iff`, `verdict_eq_unknown_iff` | Verdict.lean, VerdictProperties.lean |
| Verdict, only for consistent statements | `checkedVerdict`, `checkedVerdict_eq_none_iff`, `checkedVerdict_of_consistent` | Verdict.lean |
| Exclusivity | `not_compatible_and_incompatible` | VerdictProperties.lean |
| Proposition "Adding statements" | `verdict_compatible_mono`, `verdict_incompatible_mono` | VerdictProperties.lean |
| Theorem "Soundness" | `sound_compatible`, `sound_incompatible` | VerdictProperties.lean |
| Lemma "Formula and valuations" | `witness_iff`, `admits_atoms_iff`, `admits_iff_exists_witness` | Witness.lean, Disjuncts.lean |
| Proposition "Three checks" | `verdict_compatible_iff_witness`, `verdict_incompatible_iff_witness` | Decision.lean |
| Proposition "Verdict by left operand" | `factoring` | Factoring.lean |
| Structures against preorders | `verdict_eq_structVerdict` | Collapse.lean |
| Running example | `language_unknown`, `language_declared_verdict`, `purpose_verdict`, `spatial_verdict` | Examples/ |
| All three verdicts, inconsistent statements | `three_verdicts_occur`, `contradictory_verdict`, `contradictory_checkedVerdict` | Examples/Verdicts.lean |

Hypotheses. `Consistent T` is needed for exclusivity, for the Incompatible
direction of the decision form, and for the Incompatible case of monotonicity
(on the larger statements `T'`). Without consistency both verdicts hold vacuously and
`verdict` reports Compatible (`contradictory_verdict`). `xoneOk`, no `isAllOf`
among the alternatives of an `xone`, is needed by `admits_iff_exists_witness`,
`verdict_compatible_iff_witness` and `verdict_incompatible_iff_witness`. The
paper rejects such input: by Definition 1 (Well-sortedness) an `xone` must
not combine an `isAllOf` constraint. The benchmark compiler rejects it too
(`check_tree` in `generators/compile.py`, and the rejected case KGC123). The
compiler keeps its rewrite of a negated `isAllOf` to a disjunction of `neq`,
but only the unit tests reach it (`tests/test_witness.py`); `crosscheck/`
(T1, second line) checks the rewrite in its own code. It is not in Lean yet.

The ungrounded clause. `groundedVerdict` returns `Option Verdict`, and `none`
when a value is ungrounded: the input is rejected, as in the paper, and the
benchmark rejects the test case.

Axioms. Every main theorem depends only on `propext`, `Classical.choice` and
`Quot.sound`, or fewer. `Classical.choice` enters through `verdict`, which is a
noncomputable case split on propositions. No decidability is claimed in Lean.

Not mechanised. The encoding of the two queries into TPTP, SMT-LIB or the
Bernays-Schönfinkel fragment and its decidability, Algorithm 1, the reading of
ODRL policies and resource files into constraint sets and statements, and the
content of the vocabularies themselves. The folder `crosscheck/` and the
benchmark check these outside Lean.

Build. The toolchain is pinned in `lean-toolchain` and there are no
dependencies. A clean build takes under a minute, and the axiom check prints one
line per audited theorem.
