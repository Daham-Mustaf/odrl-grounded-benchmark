import OdrlGrounded.Semantics

set_option autoImplicit false

/-!
# Verdicts

Paper: Definition (Verdict), restricted to one operand. The ungrounded clause
(`γ` undefined gives `Unknown`) is a layer above this one, and the theorems
(exclusivity, monotonicity, soundness) come in a later step.
-/

namespace OdrlGrounded

inductive Verdict where
  | compatible
  | incompatible
  | unknown
  deriving DecidableEq, Repr

section

variable {C : Type}

/-- Every model of the theory admits a common valuation for `t` and `t'`. -/
def Compatible (T : List (Assertion C)) (N : C → Prop) (t t' : ConstraintSet C) : Prop :=
  ∀ M : Model C, Mod T M → M.admits N (t ++ t')

/-- No model of the theory admits a common valuation for `t` and `t'`. -/
def Incompatible (T : List (Assertion C)) (N : C → Prop) (t t' : ConstraintSet C) : Prop :=
  ∀ M : Model C, Mod T M → ¬ M.admits N (t ++ t')

open Classical in
noncomputable def verdict (T : List (Assertion C)) (N : C → Prop)
    (t t' : ConstraintSet C) : Verdict :=
  if Compatible T N t t' then Verdict.compatible
  else if Incompatible T N t t' then Verdict.incompatible
  else Verdict.unknown

end

end OdrlGrounded
