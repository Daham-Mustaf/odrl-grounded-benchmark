import OdrlGrounded.VerdictProperties

set_option autoImplicit false

/-!
# Running example, place row

The library policy permits `isPartOf Europe`. The researcher policy asks for `eq France`.
The binding is GeoNames at the mereological sort, and the resource publishes
that France is part of Europe. The verdict is `Compatible`.

Two concepts are enough: `france` and `europe`. Every model of the published
assertion has `france ⪯ europe`, so the valuation `{france}` satisfies both
constraint sets in every model.
-/

namespace OdrlGrounded.Example.Spatial

abbrev G := Fin 2
abbrev france : G := 0
abbrev europe : G := 1

/-- Candidate set: the binding's whole concept set. -/
def N : G → Prop := fun _ => True

def library : ConstraintSet G := [.atom (.isPartOf europe)]
def researcher : ConstraintSet G := [.atom (.eq france)]

/-- The assertion the GeoNames resource publishes: `France ⪯ Europe`. -/
def published : List (Assertion G) := [Assertion.below france europe]

/-- The order `france ⪯ europe`: concepts ordered by their index. -/
def chain : Model G where
  le := fun a b => Fin.val a ≤ Fin.val b
  refl := fun a => Nat.le_refl (Fin.val a)
  trans := fun h₁ h₂ => Nat.le_trans h₁ h₂

theorem chain_models : Mod published chain := by
  intro a ha
  simp only [published, List.mem_singleton] at ha
  subst ha
  show Fin.val france ≤ Fin.val europe
  decide

/-- The published assertion has a model. -/
theorem spatial_consistent : Consistent published := ⟨chain, chain_models⟩

/-- In every model of the published assertion, `{france}` satisfies both
constraint sets. -/
theorem spatial_compatible : Compatible published N library researcher := by
  intro M hM
  have hle : M.le france europe :=
    hM (Assertion.below france europe) (by simp [published])
  refine ⟨[france], by simp, by simp [N], ?_⟩
  intro it hit
  simp only [library, researcher, List.mem_append, List.mem_singleton] at hit
  rcases hit with rfl | rfl
  · show ∀ y, M.elems [france] y → M.le y europe
    intro y hy
    obtain ⟨x, hx, hxy⟩ := hy
    obtain rfl := List.mem_singleton.mp hx
    exact M.trans hxy.2 hle
  · show ∀ y, M.elems [france] y → M.eqv y france
    intro y hy
    obtain ⟨x, hx, hxy⟩ := hy
    obtain rfl := List.mem_singleton.mp hx
    exact M.eqv_symm hxy

theorem spatial_verdict :
    verdict published N library researcher = Verdict.compatible :=
  verdict_eq_compatible_iff.mpr spatial_compatible

/-- The witness in the chain model. -/
theorem spatial_witness :
    ∃ M, Mod published M ∧ M.admits N (library ++ researcher) :=
  ⟨chain, chain_models, spatial_compatible chain chain_models⟩

/-- Soundness: the intended structure, here the chain, admits a common
valuation. -/
theorem spatial_sound : chain.admits N (library ++ researcher) :=
  sound_compatible chain chain_models spatial_verdict

/-- Both policies are well sorted at the mereological sort. -/
theorem spatial_wellSorted :
    ConstraintSet.wellSorted Srt.mer (library ++ researcher) := by
  intro it hit
  simp only [library, researcher, List.mem_append, List.mem_singleton] at hit
  rcases hit with rfl | rfl
  · exact rfl
  · exact True.intro

end OdrlGrounded.Example.Spatial
