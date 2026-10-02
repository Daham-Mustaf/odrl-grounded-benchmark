import OdrlGrounded.Disjuncts
import OdrlGrounded.VerdictProperties

set_option autoImplicit false

/-!
# Computing verdicts

Paper: Section (Computing Verdicts), the reduction of the verdict to two
satisfiability queries.

`Model.pairWitness` says that W holds in `M` for the pair: some disjunct of
the conjunction of the two constraint sets satisfies W. A pair is `Compatible`
exactly when the theory entails W, which is the first query (the theory with
the negation of W is unsatisfiable). It is `Incompatible` exactly when the
theory entails the negation of W, which is the second query (the theory with W
is unsatisfiable). The statements are semantic: "entails" is truth in every
model of the theory.
-/

namespace OdrlGrounded

/-- W for the pair, in the model `M`. -/
def Model.pairWitness {C : Type} (M : Model C) (N : C → Prop)
    (t t' : ConstraintSet C) : Prop :=
  ∃ K ∈ setDisj M (t ++ t'), M.witness N K

section

variable {C : Type} {T : List (Assertion C)} {N : C → Prop}
  {t t' : ConstraintSet C}

theorem admits_iff_pairWitness (M : Model C) (N : C → Prop)
    (hx : ConstraintSet.xoneOk (t ++ t')) :
    M.admits N (t ++ t') ↔ M.pairWitness N t t' :=
  admits_iff_exists_witness M N (t ++ t') hx

theorem compatible_iff_witness (hx : ConstraintSet.xoneOk (t ++ t')) :
    Compatible T N t t' ↔ ∀ M : Model C, Mod T M → M.pairWitness N t t' := by
  constructor
  · intro h M hM
    exact (admits_iff_pairWitness M N hx).mp (h M hM)
  · intro h M hM
    exact (admits_iff_pairWitness M N hx).mpr (h M hM)

theorem incompatible_iff_witness (hx : ConstraintSet.xoneOk (t ++ t')) :
    Incompatible T N t t' ↔
      ∀ M : Model C, Mod T M → ¬ M.pairWitness N t t' := by
  constructor
  · intro h M hM hw
    exact h M hM ((admits_iff_pairWitness M N hx).mpr hw)
  · intro h M hM ha
    exact h M hM ((admits_iff_pairWitness M N hx).mp ha)

/-- The verdict is `Compatible` exactly when the theory entails W. -/
theorem verdict_compatible_iff_witness (hx : ConstraintSet.xoneOk (t ++ t')) :
    verdict T N t t' = Verdict.compatible ↔
      ∀ M : Model C, Mod T M → M.pairWitness N t t' :=
  Iff.trans verdict_eq_compatible_iff (compatible_iff_witness hx)

/-- The verdict is `Incompatible` exactly when the theory entails the
negation of W. -/
theorem verdict_incompatible_iff_witness (hT : Consistent T)
    (hx : ConstraintSet.xoneOk (t ++ t')) :
    verdict T N t t' = Verdict.incompatible ↔
      ∀ M : Model C, Mod T M → ¬ M.pairWitness N t t' :=
  Iff.trans (verdict_eq_incompatible_iff hT) (incompatible_iff_witness hx)

end

end OdrlGrounded
