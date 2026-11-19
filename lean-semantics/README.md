# Lean mechanization of the grounded ODRL semantics

Mechanizes "Denotational Semantics and Open-World Reasoning for Externally-Grounded ODRL Constraints".
Core Lean only, no Mathlib. Build from this folder:

    lake build

| File | Paper |
|---|---|
| OdrlGrounded/Model.lean | Binding (statements and declarations), Models; a structure as a preorder on the concepts |
| OdrlGrounded/Syntax.lean | Well-sortedness, constraint sets |
| OdrlGrounded/Semantics.lean | Denotation, Satisfaction of constraints |
| OdrlGrounded/Verdict.lean | Verdict for one left operand, and no verdict for inconsistent statements |
| OdrlGrounded/Grounding.lean | Grounding, the concept set, rejection of an ungrounded value |
| OdrlGrounded/VerdictProperties.lean | Verdict: exclusivity; Proposition "Adding statements"; Theorem "Soundness" |
| OdrlGrounded/Witness.lean | Definition "Formula of a case"; Lemma "Formula and valuations" for a case of atomic constraints |
| OdrlGrounded/Disjuncts.lean | Cases, with or, xone and negated constraints; Lemma "Formula and valuations" for a constraint set |
| OdrlGrounded/Decision.lean | Proposition "Three checks": the checks of R ∪ B ∪ {¬W} and R ∪ B ∪ {W} |
| OdrlGrounded/Factoring.lean | Verdict for several left operands, Proposition "Verdict by left operand" |
| OdrlGrounded/Collapse.lean | Structure, against the preorders used elsewhere: the same consistency and the same verdicts; Theorem "Soundness" for a structure |
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

Output on 2026-11-19 with Lean 4.34.1 (`leanprover/lean4:v4.34.1`, Lake
5.0.0), after `lake clean` and `lake build`. No other axiom, no error and no
`sorry`:

    info: OdrlGrounded/Audit.lean:26:0: 'OdrlGrounded.not_compatible_and_incompatible' does not depend on any axioms
    info: OdrlGrounded/Audit.lean:27:0: 'OdrlGrounded.verdict_compatible_mono' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:28:0: 'OdrlGrounded.verdict_incompatible_mono' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:29:0: 'OdrlGrounded.sound_compatible' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:30:0: 'OdrlGrounded.sound_incompatible' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:31:0: 'OdrlGrounded.admits_atoms_iff' depends on axioms: [propext, Quot.sound]
    info: OdrlGrounded/Audit.lean:32:0: 'OdrlGrounded.admits_iff_exists_witness' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:33:0: 'OdrlGrounded.verdict_compatible_iff_witness' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:34:0: 'OdrlGrounded.verdict_incompatible_iff_witness' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:35:0: 'OdrlGrounded.factoring' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:36:0: 'OdrlGrounded.verdict_eq_structVerdict' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:37:0: 'OdrlGrounded.Example.language_unknown' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:38:0: 'OdrlGrounded.Example.language_declared_verdict' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:39:0: 'OdrlGrounded.Example.Purpose.purpose_verdict' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:40:0: 'OdrlGrounded.Example.Spatial.spatial_verdict' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:41:0: 'OdrlGrounded.Example.three_verdicts_occur' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:42:0: 'OdrlGrounded.Example.contradictory_verdict' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:43:0: 'OdrlGrounded.ConceptOrder.not_le_of_disjoint' does not depend on any axioms
    info: OdrlGrounded/Audit.lean:44:0: 'OdrlGrounded.ConceptOrder.not_eqv_of_disjoint' does not depend on any axioms
    info: OdrlGrounded/Audit.lean:45:0: 'OdrlGrounded.checkedVerdict_eq_none_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:46:0: 'OdrlGrounded.checkedVerdict_of_consistent' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:47:0: 'OdrlGrounded.Example.contradictory_checkedVerdict' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:48:0: 'OdrlGrounded.ConstraintSet.xoneOk_of_wellSorted' depends on axioms: [propext]
    info: OdrlGrounded/Audit.lean:49:0: 'OdrlGrounded.groundedVerdict_of_left_none' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:50:0: 'OdrlGrounded.groundedVerdict_of_right_none' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:51:0: 'OdrlGrounded.consistent_iff_structConsistent' depends on axioms: [propext, Quot.sound]
    info: OdrlGrounded/Audit.lean:52:0: 'OdrlGrounded.verdict_eq_compatible_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:53:0: 'OdrlGrounded.verdict_eq_incompatible_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:54:0: 'OdrlGrounded.verdict_eq_unknown_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:55:0: 'OdrlGrounded.groundedVerdict_eq_struct' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:56:0: 'OdrlGrounded.groundedVerdict_compatible_mono' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:57:0: 'OdrlGrounded.groundedVerdict_incompatible_mono' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:58:0: 'OdrlGrounded.satSet_iff_disj' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:59:0: 'OdrlGrounded.negLit_isAnyOf_iff' depends on axioms: [propext]
    info: OdrlGrounded/Audit.lean:60:0: 'OdrlGrounded.exactlyOne_iff_index' depends on axioms: [propext, Quot.sound]
    info: OdrlGrounded/Audit.lean:61:0: 'OdrlGrounded.ConceptOrder.witness_iff' depends on axioms: [propext]
    info: OdrlGrounded/Audit.lean:62:0: 'OdrlGrounded.admits_iff_pairWitness' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:63:0: 'OdrlGrounded.Structure.sound_compatible' depends on axioms: [propext, Classical.choice, Quot.sound]
    info: OdrlGrounded/Audit.lean:64:0: 'OdrlGrounded.Structure.sound_incompatible' depends on axioms: [propext, Classical.choice, Quot.sound]

## Paper to Lean

| Paper | Lean | File |
|---|---|---|
| Well-sortedness | `Srt`, `Atom.wellSorted`, `Item.wellSorted`, `ConstraintSet.wellSorted`, `Item.xoneOk`, `ConstraintSet.xoneOk_of_wellSorted` | Syntax.lean |
| Binding (statements and declarations) | `Statement`: an order, identity, distinctness or disjointness statement; a list `T` holds the statements R of the binding together with the declarations B | Model.lean |
| Structure | `Structure`, `Structure.sat`; as a preorder on the concepts, `ConceptOrder`, `ConceptOrder.sat` | Collapse.lean, Model.lean |
| Disjointness excludes identity and order | `ConceptOrder.not_le_of_disjoint`, `ConceptOrder.not_eqv_of_disjoint` | Model.lean |
| Grounding | `Grounding`, `Grounding.range`, `ConstraintSet.ground`, `groundedVerdict`, `groundedVerdict_of_left_none`, `groundedVerdict_of_right_none` | Grounding.lean |
| The concept set of the left operand (Grounding); not the N of Definition "Formula of a case" | `N` | Semantics.lean, Grounding.lean |
| Denotation | `Atom.denot`, `Structure.sem` | Semantics.lean, Collapse.lean |
| Satisfaction of constraints | `ConceptOrder.satAtom`, `ConceptOrder.satItem`, `ConceptOrder.satSet`, `ConceptOrder.admits` | Semantics.lean |
| Models | `Mod`, `Consistent`, `Structure.Models`, `StructConsistent`, `consistent_iff_structConsistent` | Model.lean, Collapse.lean |
| Verdict | `Compatible`, `Incompatible`, `verdict`, `verdict_eq_compatible_iff`, `verdict_eq_incompatible_iff`, `verdict_eq_unknown_iff`, `not_compatible_and_incompatible` | Verdict.lean, VerdictProperties.lean |
| Verdict, defined only for consistent statements | `checkedVerdict`, `checkedVerdict_eq_none_iff`, `checkedVerdict_of_consistent` | Verdict.lean |
| Verdict over structures | `structVerdict`, `verdict_eq_structVerdict`, `groundedVerdict_eq_struct` | Collapse.lean |
| Verdict for several left operands | `MCompatible`, `MIncompatible`, `mverdict` | Factoring.lean |
| Proposition "Verdict by left operand" | `factoring` | Factoring.lean |
| Proposition "Adding statements" | `verdict_compatible_mono`, `verdict_incompatible_mono`, `groundedVerdict_compatible_mono`, `groundedVerdict_incompatible_mono` | VerdictProperties.lean |
| Theorem "Soundness" | `sound_compatible`, `sound_incompatible`; for a structure `I`, `Structure.sound_compatible`, `Structure.sound_incompatible` | VerdictProperties.lean, Collapse.lean |
| Cases | `setDisj`, `Item.disj`, `xoneDisj`, `Atom.negLit`, `satSet_iff_disj`, `negLit_isAnyOf_iff`, `exactlyOne_iff_index` | Disjuncts.lean |
| Definition "Formula of a case" | `ConceptOrder.witness`, the formula W(K) of a case K; `ConceptOrder.cand`; `ConceptOrder.pairWitness`, the formula W of the two constraint sets | Witness.lean, Decision.lean |
| Lemma "Formula and valuations" | `ConceptOrder.witness_iff`, `admits_atoms_iff`, `admits_iff_exists_witness`, `admits_iff_pairWitness` | Witness.lean, Disjuncts.lean, Decision.lean |
| Proposition "Three checks" | `checkedVerdict_eq_none_iff`, `verdict_compatible_iff_witness`, `verdict_incompatible_iff_witness` | Verdict.lean, Decision.lean |
| Running example | `language_unknown`, `language_declared_verdict`, `purpose_verdict`, `spatial_verdict` | Examples/ |
| All three verdicts, inconsistent statements | `three_verdicts_occur`, `contradictory_verdict`, `contradictory_checkedVerdict` | Examples/Verdicts.lean |

Generality. The theorems hold for any finite list of statements, and therefore
for every binding with declarations. Well-sortedness and grounding are checks on
the input, and a theorem assumes only the part it needs (`xoneOk`).

Hypotheses. `Consistent T` is needed for exclusivity, for the Incompatible
check of Proposition "Three checks", and for the Incompatible case of monotonicity
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

Not mechanised. The termination claim of Proposition "Three checks" is argued
in the paper and is not mechanised. The encoding of the two queries into TPTP,
SMT-LIB or the Bernays-Schönfinkel fragment and its decidability, the reading of
ODRL policies and resource files into constraint sets and statements, and the
content of the vocabularies themselves. The folder `crosscheck/` and the
benchmark check these outside Lean.

Build. The toolchain is pinned in `lean-toolchain` and there are no
dependencies. A clean build takes under a minute, and the axiom check prints one
line per audited theorem.
