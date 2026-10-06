import OdrlGrounded.VerdictProperties

set_option autoImplicit false

/-!
# Figure 1, purpose row

The library policy permits `isA R&D`. The researcher policy asks for `eq ScientificResearch`.
The binding is the DPV purpose hierarchy, and the resource publishes
`ScientificResearch ⪯ R&D`. The verdict is `Compatible`.

Two concepts are enough: `sr` stands for `ScientificResearch` and `rd` for `R&D`.
Every model of the published assertion has `sr ⪯ rd`, so the valuation `{sr}`
satisfies both constraint sets in every model. The chain model shows that the
published assertion is consistent.
-/

namespace OdrlGrounded.Example.Purpose

abbrev P := Fin 2
abbrev sr : P := 0
abbrev rd : P := 1

/-- Candidate set: the binding's whole concept set. -/
def N : P → Prop := fun _ => True

def library : ConstraintSet P := [.atom (.isA rd)]
def researcher : ConstraintSet P := [.atom (.eq sr)]

/-- The assertion the DPV resource publishes: `ScientificResearch ⪯ R&D`. -/
def published : List (Assertion P) := [Assertion.below sr rd]

/-- The order `sr ⪯ rd`: concepts ordered by their index. -/
def chain : Model P where
  le := fun a b => Fin.val a ≤ Fin.val b
  refl := fun a => Nat.le_refl (Fin.val a)
  trans := fun h₁ h₂ => Nat.le_trans h₁ h₂

theorem chain_models : Mod published chain := by
  intro a ha
  simp only [published, List.mem_singleton] at ha
  subst ha
  show Fin.val sr ≤ Fin.val rd
  decide

/-- The published assertion has a model. -/
theorem purpose_consistent : Consistent published := ⟨chain, chain_models⟩

/-- In every model of the published assertion, `{sr}` satisfies both
constraint sets. -/
theorem purpose_compatible : Compatible published N library researcher := by
  intro M hM
  have hle : M.le sr rd := hM (Assertion.below sr rd) (by simp [published])
  refine ⟨[sr], by simp, by simp [N], ?_⟩
  intro it hit
  simp only [library, researcher, List.mem_append, List.mem_singleton] at hit
  rcases hit with rfl | rfl
  · show ∀ y, M.elems [sr] y → M.le y rd
    intro y hy
    obtain ⟨x, hx, hxy⟩ := hy
    obtain rfl := List.mem_singleton.mp hx
    exact M.trans hxy.2 hle
  · show ∀ y, M.elems [sr] y → M.eqv y sr
    intro y hy
    obtain ⟨x, hx, hxy⟩ := hy
    obtain rfl := List.mem_singleton.mp hx
    exact M.eqv_symm hxy

theorem purpose_verdict :
    verdict published N library researcher = Verdict.compatible :=
  verdict_eq_compatible_iff.mpr purpose_compatible

/-- The witness in the chain model, the model that the check finds. -/
theorem purpose_witness :
    ∃ M, Mod published M ∧ M.admits N (library ++ researcher) :=
  ⟨chain, chain_models, purpose_compatible chain chain_models⟩

/-- Soundness: the intended structure, here the chain, admits a common
valuation. -/
theorem purpose_sound : chain.admits N (library ++ researcher) :=
  sound_compatible chain chain_models purpose_verdict

/-- Both policies are well sorted at the taxonomic sort. -/
theorem purpose_wellSorted :
    ConstraintSet.wellSorted Srt.tax (library ++ researcher) := by
  intro it hit
  simp only [library, researcher, List.mem_append, List.mem_singleton] at hit
  rcases hit with rfl | rfl
  · exact rfl
  · exact True.intro

end OdrlGrounded.Example.Purpose
