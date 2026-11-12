import OdrlGrounded.Semantics

set_option autoImplicit false

/-!
# Verdicts

Paper: Definition (Verdict), restricted to one operand. The ungrounded clause
(an ungrounded value means the input is rejected) is a layer above this one, and the theorems
(exclusivity, monotonicity, soundness) are in VerdictProperties.lean.
-/

namespace OdrlGrounded

inductive Verdict where
  | compatible
  | incompatible
  | unknown
  deriving DecidableEq, Repr

section

variable {C : Type}

/-- Every model of the statements `T` admits a common valuation for `t` and `t'`. -/
def Compatible (T : List (Statement C)) (N : C → Prop) (t t' : ConstraintSet C) : Prop :=
  ∀ M : ConceptOrder C, Mod T M → M.admits N (t ++ t')

/-- No model of the statements `T` admits a common valuation for `t` and `t'`. -/
def Incompatible (T : List (Statement C)) (N : C → Prop) (t t' : ConstraintSet C) : Prop :=
  ∀ M : ConceptOrder C, Mod T M → ¬ M.admits N (t ++ t')

open Classical in
noncomputable def verdict (T : List (Statement C)) (N : C → Prop)
    (t t' : ConstraintSet C) : Verdict :=
  if Compatible T N t t' then Verdict.compatible
  else if Incompatible T N t t' then Verdict.incompatible
  else Verdict.unknown

open Classical in
/-- The verdict as the procedure reports it: no verdict when the statements
`T` (R together with B) have no model. -/
noncomputable def checkedVerdict (T : List (Statement C)) (N : C → Prop)
    (t t' : ConstraintSet C) : Option Verdict :=
  if Consistent T then some (verdict T N t t') else none

theorem checkedVerdict_eq_none_iff (T : List (Statement C)) (N : C → Prop)
    (t t' : ConstraintSet C) :
    checkedVerdict T N t t' = none ↔ ¬ Consistent T := by
  unfold checkedVerdict
  by_cases h : Consistent T <;> simp [h]

theorem checkedVerdict_of_consistent {T : List (Statement C)}
    (hT : Consistent T) (N : C → Prop) (t t' : ConstraintSet C) :
    checkedVerdict T N t t' = some (verdict T N t t') := by
  unfold checkedVerdict
  simp [hT]

end

end OdrlGrounded
