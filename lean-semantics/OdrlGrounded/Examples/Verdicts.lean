import OdrlGrounded.Examples.Language
import OdrlGrounded.Examples.Purpose
import OdrlGrounded.Examples.Spatial

set_option autoImplicit false

/-!
# The three verdicts, consistency, and the correctness precondition

The rows of the running example give all three verdicts: purpose is `Compatible`
(Purpose.lean), the language row is `Unknown` without the declaration and
`Incompatible` with it (Language.lean). This file adds three things.

* Every list of statements used in the examples is consistent, so the verdicts are
  exclusive and the soundness theorem applies to them.
* Inconsistent statements make `Compatible` and `Incompatible` hold together.
  This is why the paper assumes consistency, and why the correctness assumption
  matters.
* `Unknown` is not final: adding the declaration turns it into `Incompatible`.
-/

namespace OdrlGrounded.Example

/-! ## Consistency of the example statements -/

theorem discrete_models_decl : Mod decl discrete := by
  intro a ha
  simp [decl] at ha
  subst ha
  simp [ConceptOrder.sat, ConceptOrder.eqv, discrete]

theorem decl_consistent : Consistent decl := ⟨discrete, discrete_models_decl⟩

theorem empty_consistent : Consistent ([] : List (Statement L)) :=
  ⟨discrete, by simp [Mod]⟩

/-! ## All three verdicts occur, each under consistent statements -/

theorem three_verdicts_occur :
    (Consistent Purpose.published ∧
      verdict Purpose.published Purpose.N Purpose.offer Purpose.request =
        Verdict.compatible) ∧
    (Consistent decl ∧
      verdict decl N offer request = Verdict.incompatible) ∧
    (Consistent ([] : List (Statement L)) ∧
      verdict ([] : List (Statement L)) N offer request = Verdict.unknown) :=
  ⟨⟨Purpose.purpose_consistent, Purpose.purpose_verdict⟩,
   ⟨decl_consistent, language_declared_verdict⟩,
   ⟨empty_consistent, language_unknown⟩⟩

/-! ## Unknown is not final -/

/-- The declaration extends the empty resource. The verdict moves from
`Unknown` to `Incompatible`, as the paper's monotonicity proposition allows:
only a definite verdict is preserved by extension. -/
theorem unknown_becomes_incompatible :
    verdict ([] : List (Statement L)) N offer request = Verdict.unknown ∧
    (∀ a ∈ ([] : List (Statement L)), a ∈ decl) ∧
    verdict decl N offer request = Verdict.incompatible :=
  ⟨language_unknown, by simp, language_declared_verdict⟩

/-! ## Inconsistent statements -/

/-- The statements `de = fr` and `de ≠ fr` together. -/
def contradictory : List (Statement L) :=
  [Statement.identity de fr, Statement.distinct de fr]

theorem contradictory_not_consistent : ¬ Consistent contradictory := by
  rintro ⟨M, hM⟩
  have h1 : M.eqv de fr := hM (Statement.identity de fr) (by simp [contradictory])
  have h2 : ¬ M.eqv de fr :=
    hM (Statement.distinct de fr) (by simp [contradictory])
  exact h2 h1

/-- With no model, both definite verdicts hold, vacuously. -/
theorem contradictory_compatible : Compatible contradictory N offer request :=
  fun M hM => absurd ⟨M, hM⟩ contradictory_not_consistent

theorem contradictory_incompatible : Incompatible contradictory N offer request :=
  fun M hM => absurd ⟨M, hM⟩ contradictory_not_consistent

/-- The verdict function tests `Compatible` first, so it reports `Compatible`
for these statements. The result carries no information, which is why the
exclusivity theorem needs `Consistent`. -/
theorem contradictory_verdict :
    verdict contradictory N offer request = Verdict.compatible :=
  verdict_eq_compatible_iff.mpr contradictory_compatible

/-- The procedure reports no verdict for these statements, because they have
no model. -/
theorem contradictory_checkedVerdict :
    checkedVerdict contradictory N offer request = none :=
  (checkedVerdict_eq_none_iff contradictory N offer request).mpr
    contradictory_not_consistent

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
