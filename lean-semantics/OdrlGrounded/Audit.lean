import OdrlGrounded.VerdictProperties
import OdrlGrounded.Witness
import OdrlGrounded.Decision
import OdrlGrounded.Factoring
import OdrlGrounded.Collapse
import OdrlGrounded.Examples.Language
import OdrlGrounded.Examples.Purpose
import OdrlGrounded.Examples.Spatial
import OdrlGrounded.Examples.Verdicts

set_option autoImplicit false

/-!
# Axiom audit

`#print axioms` lists every axiom a theorem depends on. Building this file
prints one line per theorem. A theorem proved without `sorry` and without a
`Lean.ofReduceBool` or custom axiom shows only the three core axioms
`propext`, `Classical.choice` and `Quot.sound`, or fewer.

    lake build OdrlGrounded.Audit 2>&1 | grep -E "axioms|error|sorry"

The file does not import the root module, so the root can import it.
-/

#print axioms OdrlGrounded.not_compatible_and_incompatible
#print axioms OdrlGrounded.verdict_compatible_mono
#print axioms OdrlGrounded.verdict_incompatible_mono
#print axioms OdrlGrounded.sound_compatible
#print axioms OdrlGrounded.sound_incompatible
#print axioms OdrlGrounded.admits_atoms_iff
#print axioms OdrlGrounded.admits_iff_exists_witness
#print axioms OdrlGrounded.verdict_compatible_iff_witness
#print axioms OdrlGrounded.verdict_incompatible_iff_witness
#print axioms OdrlGrounded.factoring
#print axioms OdrlGrounded.verdict_eq_structVerdict
#print axioms OdrlGrounded.Example.language_unknown
#print axioms OdrlGrounded.Example.language_declared_verdict
#print axioms OdrlGrounded.Example.Purpose.purpose_verdict
#print axioms OdrlGrounded.Example.Spatial.spatial_verdict
#print axioms OdrlGrounded.Example.three_verdicts_occur
#print axioms OdrlGrounded.Example.contradictory_verdict
#print axioms OdrlGrounded.ConceptOrder.not_le_of_disjoint
#print axioms OdrlGrounded.ConceptOrder.not_eqv_of_disjoint
#print axioms OdrlGrounded.checkedVerdict_eq_none_iff
#print axioms OdrlGrounded.checkedVerdict_of_consistent
#print axioms OdrlGrounded.Example.contradictory_checkedVerdict
#print axioms OdrlGrounded.ConstraintSet.xoneOk_of_wellSorted
#print axioms OdrlGrounded.groundedVerdict_of_left_none
#print axioms OdrlGrounded.groundedVerdict_of_right_none
#print axioms OdrlGrounded.consistent_iff_structConsistent
#print axioms OdrlGrounded.verdict_eq_compatible_iff
#print axioms OdrlGrounded.verdict_eq_incompatible_iff
#print axioms OdrlGrounded.verdict_eq_unknown_iff
#print axioms OdrlGrounded.groundedVerdict_eq_struct
#print axioms OdrlGrounded.groundedVerdict_compatible_mono
#print axioms OdrlGrounded.groundedVerdict_incompatible_mono
#print axioms OdrlGrounded.satSet_iff_disj
#print axioms OdrlGrounded.negLit_isAnyOf_iff
#print axioms OdrlGrounded.exactlyOne_iff_index
#print axioms OdrlGrounded.ConceptOrder.witness_iff
#print axioms OdrlGrounded.admits_iff_pairWitness
