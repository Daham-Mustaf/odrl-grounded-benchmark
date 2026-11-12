import OdrlGrounded.Disjuncts
import OdrlGrounded.VerdictProperties

set_option autoImplicit false

/-!
# Computing verdicts

Paper: Section (Computing Compatibility Verdicts), the reduction of the verdict to
the checks of R ∪ B ∪ {¬W} and R ∪ B ∪ {W}.

`ConceptOrder.pairWitness` says that the formula W holds in `M` for the pair:
`M` satisfies W(K) for some case K of the two constraint sets. A pair is
`Compatible` exactly when the statements `T` entail W, that is, when
R ∪ B ∪ {¬W} has no model. It is `Incompatible` exactly when the statements
entail ¬W, that is, when R ∪ B ∪ {W} has no model. The results are semantic:
"entail" is truth in every model of the statements.
-/

namespace OdrlGrounded

/-- W for the pair, in the concept order `M`. -/
def ConceptOrder.pairWitness {C : Type} (M : ConceptOrder C) (N : C → Prop)
    (t t' : ConstraintSet C) : Prop :=
  ∃ K ∈ setDisj M (t ++ t'), M.witness N K

section

variable {C : Type} {T : List (Statement C)} {N : C → Prop}
  {t t' : ConstraintSet C}

theorem admits_iff_pairWitness (M : ConceptOrder C) (N : C → Prop)
    (hx : ConstraintSet.xoneOk (t ++ t')) :
    M.admits N (t ++ t') ↔ M.pairWitness N t t' :=
  admits_iff_exists_witness M N (t ++ t') hx

theorem compatible_iff_witness (hx : ConstraintSet.xoneOk (t ++ t')) :
    Compatible T N t t' ↔ ∀ M : ConceptOrder C, Mod T M → M.pairWitness N t t' := by
  constructor
  · intro h M hM
    exact (admits_iff_pairWitness M N hx).mp (h M hM)
  · intro h M hM
    exact (admits_iff_pairWitness M N hx).mpr (h M hM)

theorem incompatible_iff_witness (hx : ConstraintSet.xoneOk (t ++ t')) :
    Incompatible T N t t' ↔
      ∀ M : ConceptOrder C, Mod T M → ¬ M.pairWitness N t t' := by
  constructor
  · intro h M hM hw
    exact h M hM ((admits_iff_pairWitness M N hx).mpr hw)
  · intro h M hM ha
    exact h M hM ((admits_iff_pairWitness M N hx).mp ha)

/-- The verdict is `Compatible` exactly when the statements entail W. -/
theorem verdict_compatible_iff_witness (hx : ConstraintSet.xoneOk (t ++ t')) :
    verdict T N t t' = Verdict.compatible ↔
      ∀ M : ConceptOrder C, Mod T M → M.pairWitness N t t' :=
  Iff.trans verdict_eq_compatible_iff (compatible_iff_witness hx)

/-- The verdict is `Incompatible` exactly when the statements entail the
negation of W. -/
theorem verdict_incompatible_iff_witness (hT : Consistent T)
    (hx : ConstraintSet.xoneOk (t ++ t')) :
    verdict T N t t' = Verdict.incompatible ↔
      ∀ M : ConceptOrder C, Mod T M → ¬ M.pairWitness N t t' :=
  Iff.trans (verdict_eq_incompatible_iff hT) (incompatible_iff_witness hx)

end

end OdrlGrounded
