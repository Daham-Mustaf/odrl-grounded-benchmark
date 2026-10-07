# Lean mechanization of the grounded ODRL semantics

Mechanizes "Denotational Semantics and Open-World Reasoning for Externally-Grounded ODRL Constraints".
Core Lean only, no Mathlib. Build from this folder:

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
| OdrlGrounded/Examples/Language.lean | Running example, language row |
| OdrlGrounded/Examples/Grounding.lean | Language row with values, ungrounded alternative |
| OdrlGrounded/Examples/Purpose.lean | Running example, purpose row: `Compatible`, with a model of the published assertion |
| OdrlGrounded/Examples/Spatial.lean | Running example, place row: `Compatible`, with a model of the published assertion |
| OdrlGrounded/Examples/Verdicts.lean | All three verdicts under consistent theories, an inconsistent theory, well-sortedness |
| OdrlGrounded/Audit.lean | `#print axioms` for the main theorems and examples |

Folder `crosscheck/` holds the brute-force Python checks of the same
claims, with a table of which Lean theorem covers which check.

Axiom check:

    lake build OdrlGrounded.Audit 2>&1 | grep -E "axioms|error|sorry"

## Paper to Lean

| Paper | Lean | File |
|---|---|---|
| Signature and well-sortedness | `Atom.wellSorted`, `Item.wellSorted`, `ConstraintSet.xoneOk_of_wellSorted` | Syntax.lean |
| Resource, background theory, models | `Assertion`, `Model`, `Mod`, `Consistent` | Model.lean |
| Structure with unnamed elements | `Structure`, `structVerdict` | Collapse.lean |
| Grounding, ungrounded clause | `Grounding`, `Grounding.range`, `groundedVerdict`, `groundedVerdict_of_left_none`, `groundedVerdict_of_right_none` | Grounding.lean |
| Denotation, valuation and satisfaction | `Atom.denot`, `Model.satAtom`, `Model.satItem`, `Model.satSet`, `Model.admits` | Semantics.lean |
| Verdict | `Compatible`, `Incompatible`, `verdict`, `verdict_eq_compatible_iff`, `verdict_eq_incompatible_iff`, `verdict_eq_unknown_iff` | Verdict.lean, VerdictProperties.lean |
| Exclusivity | `not_compatible_and_incompatible` | VerdictProperties.lean |
| Monotonicity | `verdict_compatible_mono`, `verdict_incompatible_mono` | VerdictProperties.lean |
| Soundness | `sound_compatible`, `sound_incompatible` | VerdictProperties.lean |
| Witness lemma | `Model.witness`, `witness_iff`, `admits_atoms_iff` | Witness.lean |
| Reduction of a constraint set | `setDisj`, `admits_iff_exists_witness` | Disjuncts.lean |
| Verdict from the witness condition | `Model.pairWitness`, `verdict_compatible_iff_witness`, `verdict_incompatible_iff_witness` | Decision.lean |
| Operand-wise factoring | `mverdict`, `minVerdict`, `factoring` | Factoring.lean |
| Structures against preorders | `verdict_eq_structVerdict` | Collapse.lean |
| Running example | `language_unknown`, `language_declared_verdict`, `purpose_verdict`, `spatial_verdict` | Examples/ |
| All three verdicts, inconsistent theory | `three_verdicts_occur`, `contradictory_verdict` | Examples/Verdicts.lean |

Hypotheses. `Consistent T` is needed for exclusivity, for the Incompatible
direction of the decision form, and for the Incompatible case of monotonicity
(on the larger theory). `xoneOk`, a consequence of well-sortedness, is needed by
the witness decision. Without consistency both verdicts hold vacuously and
`verdict` reports Compatible (`contradictory_verdict`).

Axioms. Every main theorem depends only on `propext`, `Classical.choice` and
`Quot.sound`, or fewer. `Classical.choice` enters through `verdict`, which is a
noncomputable case split on propositions. No decidability is claimed in Lean.

Not mechanised. The encoding of the two queries into TPTP, SMT-LIB or the
Bernays-Schönfinkel fragment and its decidability, Algorithm 1, the reading of
ODRL policies and resource files into constraint sets and assertions, and the
content of the vocabularies themselves. The folder `crosscheck/` and the
benchmark check these outside Lean.

Build. The toolchain is pinned in `lean-toolchain` and there are no
dependencies. A clean build takes under a minute, and the axiom check prints one
line per audited theorem.
