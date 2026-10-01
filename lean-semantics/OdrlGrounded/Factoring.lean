import OdrlGrounded.VerdictProperties

set_option autoImplicit false

/-!
# Operand-wise factoring

Paper: Assumption (Operand independence), Corollary (Operand-wise factoring).

Operands are indexed by `ι`. Each operand `ℓ` has its own theory `T ℓ`,
candidate set `N ℓ`, and constraint sets `t ℓ` and `t' ℓ`. Each Logical
Constraint stays on one operand, so a constraint set on several operands is
one constraint set per operand.

Assumption (Operand independence) says that a structure for the union is an
independent choice of one structure per operand. This is built into the types
here: a model of all the theories is a family `M : ι → Model C` with `M ℓ` a
model of `T ℓ`. The concept type `C` is shared only for convenience, and each
operand interprets its own copy, so the concept sets are disjoint. A joint
valuation gives each operand its own valuation. Only the operands in `ls`,
those that occur in one of the two constraint sets, take part.

The ungrounded clause is not restated. It makes the whole verdict `Unknown`
before any factoring, as in the definition of the verdict. This file covers
the other case, where every value is grounded.
-/

namespace OdrlGrounded

/-! ## The order Incompatible < Unknown < Compatible -/

/-- The minimum of two verdicts. -/
def Verdict.meet : Verdict → Verdict → Verdict
  | .incompatible, _ => .incompatible
  | _, .incompatible => .incompatible
  | .unknown, _ => .unknown
  | _, .unknown => .unknown
  | .compatible, .compatible => .compatible

/-- The minimum of a list of verdicts. -/
def minVerdict (vs : List Verdict) : Verdict :=
  vs.foldr Verdict.meet Verdict.compatible

theorem Verdict.meet_eq_compatible_iff (a b : Verdict) :
    Verdict.meet a b = Verdict.compatible ↔
      a = Verdict.compatible ∧ b = Verdict.compatible := by
  cases a <;> cases b <;> decide

theorem Verdict.meet_eq_incompatible_iff (a b : Verdict) :
    Verdict.meet a b = Verdict.incompatible ↔
      a = Verdict.incompatible ∨ b = Verdict.incompatible := by
  cases a <;> cases b <;> decide

theorem minVerdict_eq_compatible_iff (vs : List Verdict) :
    minVerdict vs = Verdict.compatible ↔ ∀ v ∈ vs, v = Verdict.compatible := by
  induction vs with
  | nil => simp [minVerdict]
  | cons v vs ih =>
    have h : minVerdict (v :: vs) = Verdict.meet v (minVerdict vs) := rfl
    rw [h, Verdict.meet_eq_compatible_iff, ih]
    simp

theorem minVerdict_eq_incompatible_iff (vs : List Verdict) :
    minVerdict vs = Verdict.incompatible ↔ ∃ v ∈ vs, v = Verdict.incompatible := by
  induction vs with
  | nil => simp [minVerdict]
  | cons v vs ih =>
    have h : minVerdict (v :: vs) = Verdict.meet v (minVerdict vs) := rfl
    rw [h, Verdict.meet_eq_incompatible_iff, ih]
    constructor
    · rintro (h1 | ⟨w, hw, hwi⟩)
      · exact ⟨v, List.mem_cons.mpr (Or.inl rfl), h1⟩
      · exact ⟨w, List.mem_cons.mpr (Or.inr hw), hwi⟩
    · rintro ⟨w, hw, hwi⟩
      rcases List.mem_cons.mp hw with hwv | hw'
      · rw [hwv] at hwi
        exact Or.inl hwi
      · exact Or.inr ⟨w, hw', hwi⟩

/-- A verdict is determined by whether it is `Compatible` and whether it is
`Incompatible`. -/
theorem Verdict.ext_of_iff (x y : Verdict)
    (h1 : x = Verdict.compatible ↔ y = Verdict.compatible)
    (h2 : x = Verdict.incompatible ↔ y = Verdict.incompatible) : x = y := by
  cases x <;> cases y <;> simp_all

/-! ## Families of models -/

/-- Any concept set with every concept identified. -/
def Model.indiscrete {C : Type} : Model C where
  le := fun _ _ => True
  refl := fun _ => True.intro
  trans := fun _ _ => True.intro

/-- A model of a consistent theory, chosen. -/
noncomputable def Consistent.model {C : Type} {T : List (Assertion C)}
    (h : Consistent T) : Model C :=
  Classical.choose (show ∃ M : Model C, Mod T M from h)

theorem Consistent.model_spec {C : Type} {T : List (Assertion C)}
    (h : Consistent T) : Mod T h.model :=
  Classical.choose_spec (show ∃ M : Model C, Mod T M from h)

section

variable {ι C : Type}

/-- A joint valuation gives each operand in `ls` its own valuation. -/
def MAdmits (ls : List ι) (M : ι → Model C) (N : ι → C → Prop)
    (t t' : ι → ConstraintSet C) : Prop :=
  ∃ ρ : (ℓ : ι) → ℓ ∈ ls → List C, ∀ (ℓ : ι) (hℓ : ℓ ∈ ls),
    ρ ℓ hℓ ≠ [] ∧ (∀ x ∈ ρ ℓ hℓ, N ℓ x) ∧
      (M ℓ).satSet (ρ ℓ hℓ) (t ℓ ++ t' ℓ)

/-- A joint valuation exists exactly when each operand has one. -/
theorem madmits_iff (ls : List ι) (M : ι → Model C) (N : ι → C → Prop)
    (t t' : ι → ConstraintSet C) :
    MAdmits ls M N t t' ↔ ∀ ℓ ∈ ls, (M ℓ).admits (N ℓ) (t ℓ ++ t' ℓ) := by
  constructor
  · rintro ⟨ρ, hρ⟩ ℓ hℓ
    exact ⟨ρ ℓ hℓ, hρ ℓ hℓ⟩
  · intro h
    have hex : ∀ (ℓ : ι) (hℓ : ℓ ∈ ls), ∃ ρ : List C, ρ ≠ [] ∧
        (∀ x ∈ ρ, N ℓ x) ∧ (M ℓ).satSet ρ (t ℓ ++ t' ℓ) :=
      fun ℓ hℓ => h ℓ hℓ
    exact ⟨fun ℓ hℓ => Classical.choose (hex ℓ hℓ),
      fun ℓ hℓ => Classical.choose_spec (hex ℓ hℓ)⟩

/-- Every family of models of the theories admits a joint valuation. -/
def MCompatible (ls : List ι) (T : ι → List (Assertion C))
    (N : ι → C → Prop) (t t' : ι → ConstraintSet C) : Prop :=
  ∀ M : ι → Model C, (∀ ℓ ∈ ls, Mod (T ℓ) (M ℓ)) → MAdmits ls M N t t'

/-- No family of models of the theories admits a joint valuation. -/
def MIncompatible (ls : List ι) (T : ι → List (Assertion C))
    (N : ι → C → Prop) (t t' : ι → ConstraintSet C) : Prop :=
  ∀ M : ι → Model C, (∀ ℓ ∈ ls, Mod (T ℓ) (M ℓ)) → ¬ MAdmits ls M N t t'

open Classical in
noncomputable def mverdict (ls : List ι) (T : ι → List (Assertion C))
    (N : ι → C → Prop) (t t' : ι → ConstraintSet C) : Verdict :=
  if MCompatible ls T N t t' then Verdict.compatible
  else if MIncompatible ls T N t t' then Verdict.incompatible
  else Verdict.unknown

open Classical in
/-- A family of models of the theories with a prescribed model at `ℓ0`. -/
noncomputable def modelFamily (ls : List ι) (T : ι → List (Assertion C))
    (hcons : ∀ ℓ ∈ ls, Consistent (T ℓ)) (ℓ0 : ι) (M0 : Model C) :
    ι → Model C :=
  fun ℓ => if ℓ = ℓ0 then M0 else
    if hℓ : ℓ ∈ ls then (hcons ℓ hℓ).model else M0

theorem modelFamily_self (ls : List ι) (T : ι → List (Assertion C))
    (hcons : ∀ ℓ ∈ ls, Consistent (T ℓ)) (ℓ0 : ι) (M0 : Model C) :
    modelFamily ls T hcons ℓ0 M0 ℓ0 = M0 := by
  simp [modelFamily]

theorem modelFamily_mod (ls : List ι) (T : ι → List (Assertion C))
    (hcons : ∀ ℓ ∈ ls, Consistent (T ℓ)) (ℓ0 : ι) (M0 : Model C)
    (hM0 : Mod (T ℓ0) M0) :
    ∀ ℓ ∈ ls, Mod (T ℓ) (modelFamily ls T hcons ℓ0 M0 ℓ) := by
  intro ℓ hℓ
  by_cases h : ℓ = ℓ0
  · subst h
    simpa [modelFamily] using hM0
  · simp [modelFamily, h, hℓ]
    exact (hcons ℓ hℓ).model_spec

open Classical in
/-- A family of models built from one model per operand in `ls`. -/
noncomputable def pickFamily (ls : List ι) (f : (ℓ : ι) → ℓ ∈ ls → Model C) :
    ι → Model C :=
  fun ℓ => if h : ℓ ∈ ls then f ℓ h else Model.indiscrete

theorem pickFamily_eq (ls : List ι) (f : (ℓ : ι) → ℓ ∈ ls → Model C)
    (ℓ : ι) (hℓ : ℓ ∈ ls) : pickFamily ls f ℓ = f ℓ hℓ := by
  simp [pickFamily, hℓ]

variable {ls : List ι} {T : ι → List (Assertion C)} {N : ι → C → Prop}
  {t t' : ι → ConstraintSet C}

/-- Compatible for the union exactly when Compatible for every operand. -/
theorem mcompatible_iff (hcons : ∀ ℓ ∈ ls, Consistent (T ℓ)) :
    MCompatible ls T N t t' ↔
      ∀ ℓ ∈ ls, Compatible (T ℓ) (N ℓ) (t ℓ) (t' ℓ) := by
  constructor
  · intro h ℓ0 hℓ0 M0 hM0
    have hmod := modelFamily_mod ls T hcons ℓ0 M0 hM0
    have hadm := (madmits_iff ls (modelFamily ls T hcons ℓ0 M0) N t t').mp
      (h (modelFamily ls T hcons ℓ0 M0) hmod) ℓ0 hℓ0
    rw [modelFamily_self] at hadm
    exact hadm
  · intro h M hM
    rw [madmits_iff]
    intro ℓ hℓ
    exact h ℓ hℓ (M ℓ) (hM ℓ hℓ)

/-- Incompatible for the union exactly when Incompatible for some operand. -/
theorem mincompatible_iff :
    MIncompatible ls T N t t' ↔
      ∃ ℓ ∈ ls, Incompatible (T ℓ) (N ℓ) (t ℓ) (t' ℓ) := by
  constructor
  · intro h
    refine Classical.byContradiction fun hne => ?_
    have hex : ∀ (ℓ : ι) (hℓ : ℓ ∈ ls), ∃ M : Model C, Mod (T ℓ) M ∧
        M.admits (N ℓ) (t ℓ ++ t' ℓ) := by
      intro ℓ hℓ
      refine Classical.byContradiction fun hno => hne ⟨ℓ, hℓ, ?_⟩
      intro M hM hadm
      exact hno ⟨M, hM, hadm⟩
    obtain ⟨f, hf⟩ : ∃ f : (ℓ : ι) → ℓ ∈ ls → Model C,
        ∀ (ℓ : ι) (hℓ : ℓ ∈ ls), Mod (T ℓ) (f ℓ hℓ) ∧
          (f ℓ hℓ).admits (N ℓ) (t ℓ ++ t' ℓ) :=
      ⟨fun ℓ hℓ => Classical.choose (hex ℓ hℓ),
        fun ℓ hℓ => Classical.choose_spec (hex ℓ hℓ)⟩
    refine h (pickFamily ls f) ?_ ?_
    · intro ℓ hℓ
      rw [pickFamily_eq ls f ℓ hℓ]
      exact (hf ℓ hℓ).1
    · rw [madmits_iff]
      intro ℓ hℓ
      rw [pickFamily_eq ls f ℓ hℓ]
      exact (hf ℓ hℓ).2
  · rintro ⟨ℓ0, hℓ0, hinc⟩ M hM hadm
    exact hinc (M ℓ0) (hM ℓ0 hℓ0) ((madmits_iff ls M N t t').mp hadm ℓ0 hℓ0)

theorem mverdict_eq_compatible_iff :
    mverdict ls T N t t' = Verdict.compatible ↔ MCompatible ls T N t t' := by
  unfold mverdict
  by_cases h : MCompatible ls T N t t'
  · simp [h]
  · by_cases h' : MIncompatible ls T N t t' <;> simp [h, h']

theorem mverdict_eq_incompatible_iff (hcons : ∀ ℓ ∈ ls, Consistent (T ℓ)) :
    mverdict ls T N t t' = Verdict.incompatible ↔ MIncompatible ls T N t t' := by
  unfold mverdict
  by_cases h : MCompatible ls T N t t'
  · have hn : ¬ MIncompatible ls T N t t' := by
      intro hi
      obtain ⟨ℓ, hℓ, hinc⟩ := mincompatible_iff.mp hi
      exact not_compatible_and_incompatible (hcons ℓ hℓ)
        ⟨(mcompatible_iff hcons).mp h ℓ hℓ, hinc⟩
    simp [h, hn]
  · by_cases h' : MIncompatible ls T N t t' <;> simp [h, h']

/-- Corollary (Operand-wise factoring), for grounded constraint sets. The
verdict of the union is the minimum of the per-operand verdicts, each taken
under that operand's own theory. -/
theorem factoring (hcons : ∀ ℓ ∈ ls, Consistent (T ℓ)) :
    mverdict ls T N t t' =
      minVerdict (ls.map fun ℓ => verdict (T ℓ) (N ℓ) (t ℓ) (t' ℓ)) := by
  apply Verdict.ext_of_iff
  · rw [mverdict_eq_compatible_iff, mcompatible_iff hcons,
      minVerdict_eq_compatible_iff]
    constructor
    · intro h v hv
      obtain ⟨ℓ, hℓ, rfl⟩ := List.mem_map.mp hv
      exact verdict_eq_compatible_iff.mpr (h ℓ hℓ)
    · intro h ℓ hℓ
      exact verdict_eq_compatible_iff.mp
        (h _ (List.mem_map.mpr ⟨ℓ, hℓ, rfl⟩))
  · rw [mverdict_eq_incompatible_iff hcons, mincompatible_iff,
      minVerdict_eq_incompatible_iff]
    constructor
    · rintro ⟨ℓ, hℓ, hi⟩
      exact ⟨verdict (T ℓ) (N ℓ) (t ℓ) (t' ℓ),
        List.mem_map.mpr ⟨ℓ, hℓ, rfl⟩,
        (verdict_eq_incompatible_iff (hcons ℓ hℓ)).mpr hi⟩
    · rintro ⟨v, hv, hvi⟩
      obtain ⟨ℓ, hℓ, rfl⟩ := List.mem_map.mp hv
      exact ⟨ℓ, hℓ, (verdict_eq_incompatible_iff (hcons ℓ hℓ)).mp hvi⟩

end

end OdrlGrounded
