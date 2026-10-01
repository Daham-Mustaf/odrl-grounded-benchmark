import OdrlGrounded.Grounding

set_option autoImplicit false

/-!
# Properties of the verdict

Paper: Definition (Models) and the consistency assumption, Proposition
(Monotonicity under extension), Theorem (Soundness).

`Compatible` and `Incompatible` both hold when the theory has no model, so
the verdicts are exclusive only for a consistent theory, which the paper
assumes throughout. Monotonicity and soundness need no further assumption
beyond that.
-/

namespace OdrlGrounded

section

variable {C : Type} {T T' : List (Assertion C)} {N : C → Prop}
  {t t' : ConstraintSet C}

/-- For a consistent theory the two definite cases exclude each other. -/
theorem not_compatible_and_incompatible (hT : Consistent T) :
    ¬ (Compatible T N t t' ∧ Incompatible T N t t') := by
  rintro ⟨hc, hi⟩
  obtain ⟨M, hM⟩ := hT
  exact hi M hM (hc M hM)

theorem verdict_eq_compatible_iff :
    verdict T N t t' = Verdict.compatible ↔ Compatible T N t t' := by
  unfold verdict
  by_cases h : Compatible T N t t'
  · simp [h]
  · by_cases h' : Incompatible T N t t' <;> simp [h, h']

theorem verdict_eq_incompatible_iff (hT : Consistent T) :
    verdict T N t t' = Verdict.incompatible ↔ Incompatible T N t t' := by
  unfold verdict
  by_cases h : Compatible T N t t'
  · have hn : ¬ Incompatible T N t t' :=
      fun hi => not_compatible_and_incompatible hT ⟨h, hi⟩
    simp [h, hn]
  · by_cases h' : Incompatible T N t t' <;> simp [h, h']

theorem verdict_eq_unknown_iff :
    verdict T N t t' = Verdict.unknown ↔
      ¬ Compatible T N t t' ∧ ¬ Incompatible T N t t' := by
  unfold verdict
  by_cases h : Compatible T N t t'
  · simp [h]
  · by_cases h' : Incompatible T N t t' <;> simp [h, h']

/-- Adding assertions shrinks the class of models. -/
theorem compatible_mono (hsub : ∀ a ∈ T, a ∈ T') :
    Compatible T N t t' → Compatible T' N t t' := by
  intro h M hM
  exact h M (fun a ha => hM a (hsub a ha))

theorem incompatible_mono (hsub : ∀ a ∈ T, a ∈ T') :
    Incompatible T N t t' → Incompatible T' N t t' := by
  intro h M hM
  exact h M (fun a ha => hM a (hsub a ha))

/-- Proposition (Monotonicity under extension), Compatible case. -/
theorem verdict_compatible_mono (hsub : ∀ a ∈ T, a ∈ T')
    (h : verdict T N t t' = Verdict.compatible) :
    verdict T' N t t' = Verdict.compatible :=
  verdict_eq_compatible_iff.mpr
    (compatible_mono hsub (verdict_eq_compatible_iff.mp h))

/-- Proposition (Monotonicity under extension), Incompatible case. -/
theorem verdict_incompatible_mono (hsub : ∀ a ∈ T, a ∈ T')
    (hT' : Consistent T')
    (h : verdict T N t t' = Verdict.incompatible) :
    verdict T' N t t' = Verdict.incompatible := by
  have hT : Consistent T := by
    obtain ⟨M, hM⟩ := hT'
    exact ⟨M, fun a ha => hM a (hsub a ha)⟩
  exact (verdict_eq_incompatible_iff hT').mpr
    (incompatible_mono hsub ((verdict_eq_incompatible_iff hT).mp h))

/-- Theorem (Soundness), Compatible case. `I` is the intended interpretation,
a model of the theory. -/
theorem sound_compatible (I : Model C) (hI : Mod T I)
    (h : verdict T N t t' = Verdict.compatible) : I.admits N (t ++ t') :=
  (verdict_eq_compatible_iff.mp h) I hI

/-- Theorem (Soundness), Incompatible case. -/
theorem sound_incompatible (I : Model C) (hI : Mod T I)
    (h : verdict T N t t' = Verdict.incompatible) :
    ¬ I.admits N (t ++ t') := by
  have hT : Consistent T := ⟨I, hI⟩
  exact ((verdict_eq_incompatible_iff hT).mp h) I hI

end

section

variable {V C : Type} {T T' : List (Assertion C)}

/-- Monotonicity for the verdict with the ungrounded clause. The grounding
does not depend on the theory, so an ungrounded pair stays `Unknown`. -/
theorem groundedVerdict_compatible_mono (γ : Grounding V C)
    (hsub : ∀ a ∈ T, a ∈ T') (t t' : ConstraintSet V)
    (h : groundedVerdict γ T t t' = Verdict.compatible) :
    groundedVerdict γ T' t t' = Verdict.compatible := by
  cases hg : ConstraintSet.ground γ t with
  | none =>
    rw [groundedVerdict_of_left_none γ T t t' hg] at h
    cases h
  | some g =>
    cases hg' : ConstraintSet.ground γ t' with
    | none =>
      rw [groundedVerdict_of_right_none γ T t t' hg'] at h
      cases h
    | some g' =>
      rw [groundedVerdict_of_some γ T t t' g g' hg hg'] at h
      rw [groundedVerdict_of_some γ T' t t' g g' hg hg']
      exact verdict_compatible_mono hsub h

theorem groundedVerdict_incompatible_mono (γ : Grounding V C)
    (hsub : ∀ a ∈ T, a ∈ T') (hT' : Consistent T') (t t' : ConstraintSet V)
    (h : groundedVerdict γ T t t' = Verdict.incompatible) :
    groundedVerdict γ T' t t' = Verdict.incompatible := by
  cases hg : ConstraintSet.ground γ t with
  | none =>
    rw [groundedVerdict_of_left_none γ T t t' hg] at h
    cases h
  | some g =>
    cases hg' : ConstraintSet.ground γ t' with
    | none =>
      rw [groundedVerdict_of_right_none γ T t t' hg'] at h
      cases h
    | some g' =>
      rw [groundedVerdict_of_some γ T t t' g g' hg hg'] at h
      rw [groundedVerdict_of_some γ T' t t' g g' hg hg']
      exact verdict_incompatible_mono hsub hT' h

end

end OdrlGrounded
