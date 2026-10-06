import OdrlGrounded.Examples.Language
import OdrlGrounded.Examples.Purpose
import OdrlGrounded.Examples.Spatial

set_option autoImplicit false

/-!
# The three verdicts, consistency, and the correctness precondition

The rows of Figure 1 give all three verdicts: purpose is `Compatible`
(Purpose.lean), the language row is `Unknown` without the declaration and
`Incompatible` with it (Language.lean). This file adds three things.

* Every theory used in the examples is consistent, so the verdicts are
  exclusive and the soundness theorem applies to them.
* An inconsistent theory makes `Compatible` and `Incompatible` hold together.
  This is why the paper assumes consistency, and why the correctness assumption
  matters.
* `Unknown` is not final: adding the declaration turns it into `Incompatible`.
-/

namespace OdrlGrounded.Example

/-! ## Consistency of the example theories -/

theorem discrete_models_decl : Mod decl discrete := by
  intro a ha
  simp [decl] at ha
  subst ha
  simp [Model.sat, Model.eqv, discrete]

theorem decl_consistent : Consistent decl := ⟨discrete, discrete_models_decl⟩

theorem empty_consistent : Consistent ([] : List (Assertion L)) :=
  ⟨discrete, by simp [Mod]⟩

/-! ## All three verdicts occur, each under a consistent theory -/

theorem three_verdicts_occur :
    (Consistent Purpose.published ∧
      verdict Purpose.published Purpose.N Purpose.library Purpose.researcher =
        Verdict.compatible) ∧
    (Consistent decl ∧
      verdict decl N offer request = Verdict.incompatible) ∧
    (Consistent ([] : List (Assertion L)) ∧
      verdict ([] : List (Assertion L)) N offer request = Verdict.unknown) :=
  ⟨⟨Purpose.purpose_consistent, Purpose.purpose_verdict⟩,
   ⟨decl_consistent, language_declared_verdict⟩,
   ⟨empty_consistent, language_unknown⟩⟩

/-! ## Unknown is not final -/

/-- The declaration extends the empty resource. The verdict moves from
`Unknown` to `Incompatible`, as the paper's monotonicity proposition allows:
only a definite verdict is preserved by extension. -/
theorem unknown_becomes_incompatible :
    verdict ([] : List (Assertion L)) N offer request = Verdict.unknown ∧
    (∀ a ∈ ([] : List (Assertion L)), a ∈ decl) ∧
    verdict decl N offer request = Verdict.incompatible :=
  ⟨language_unknown, by simp, language_declared_verdict⟩

/-! ## An inconsistent theory -/

/-- The assertions `de = fr` and `de ≠ fr` together. -/
def contradictory : List (Assertion L) :=
  [Assertion.same de fr, Assertion.distinct de fr]

theorem contradictory_not_consistent : ¬ Consistent contradictory := by
  rintro ⟨M, hM⟩
  have h1 : M.eqv de fr := hM (Assertion.same de fr) (by simp [contradictory])
  have h2 : ¬ M.eqv de fr :=
    hM (Assertion.distinct de fr) (by simp [contradictory])
  exact h2 h1

/-- With no model, both definite verdicts hold, vacuously. -/
theorem contradictory_compatible : Compatible contradictory N offer request :=
  fun M hM => absurd ⟨M, hM⟩ contradictory_not_consistent

theorem contradictory_incompatible : Incompatible contradictory N offer request :=
  fun M hM => absurd ⟨M, hM⟩ contradictory_not_consistent

/-- The verdict function tests `Compatible` first, so it reports `Compatible`
for this theory. The result carries no information, which is why the
exclusivity theorem needs `Consistent`. -/
theorem contradictory_verdict :
    verdict contradictory N offer request = Verdict.compatible :=
  verdict_eq_compatible_iff.mpr contradictory_compatible

/-! ## Signature: sorts restrict operators -/

/-- Both language constraint sets are well sorted at the identity sort. -/
theorem language_wellSorted : ConstraintSet.wellSorted Srt.nom (offer ++ request) := by
  intro it hit
  simp only [offer, request, List.mem_append, List.mem_singleton] at hit
  rcases hit with rfl | rfl <;> exact True.intro

/-- `isA` is not allowed at the identity sort. -/
theorem language_isA_not_wellSorted :
    ¬ ConstraintSet.wellSorted Srt.nom ([Item.atom (Atom.isA de)] : ConstraintSet L) := by
  intro h
  have h' : Srt.nom = Srt.tax := h (Item.atom (Atom.isA de)) (by simp)
  cases h'

end OdrlGrounded.Example
