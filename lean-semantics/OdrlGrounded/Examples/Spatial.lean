import OdrlGrounded.VerdictProperties

set_option autoImplicit false

/-!
# Running example, place row

The offer permits `isPartOf Europe`. The request asks for `eq France`.
The binding is GeoNames at the mereological sort, and the resource publishes
that France is part of Europe. The verdict is `Compatible`.

Two concepts are enough: `france` and `europe`. Every model of the published
statement has `france ⪯ europe`, so the valuation `{france}` satisfies both
constraint sets in every model.
-/

namespace OdrlGrounded.Example.Spatial

abbrev G := Fin 2
abbrev france : G := 0
abbrev europe : G := 1

/-- The concept set: the binding's whole set of concepts. -/
def N : G → Prop := fun _ => True

def offer : ConstraintSet G := [.atom (.isPartOf europe)]
def request : ConstraintSet G := [.atom (.eq france)]

/-- The statement the GeoNames resource publishes: `France ⪯ Europe`. -/
def published : List (Statement G) := [Statement.order france europe]

/-- The order `france ⪯ europe`: concepts ordered by their index. -/
def chain : ConceptOrder G where
  le := fun a b => Fin.val a ≤ Fin.val b
  refl := fun a => Nat.le_refl (Fin.val a)
  trans := fun h₁ h₂ => Nat.le_trans h₁ h₂

theorem chain_models : Mod published chain := by
  intro a ha
  simp only [published, List.mem_singleton] at ha
  subst ha
  show Fin.val france ≤ Fin.val europe
  decide

/-- The published statement has a model. -/
theorem spatial_consistent : Consistent published := ⟨chain, chain_models⟩

/-- In every model of the published statement, `{france}` satisfies both
constraint sets. -/
theorem spatial_compatible : Compatible published N offer request := by
  intro M hM
  have hle : M.le france europe :=
    hM (Statement.order france europe) (by simp [published])
  refine ⟨[france], by simp, by simp [N], ?_⟩
  intro it hit
  simp only [offer, request, List.mem_append, List.mem_singleton] at hit
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
    verdict published N offer request = Verdict.compatible :=
  verdict_eq_compatible_iff.mpr spatial_compatible

/-- The chain model has a valuation that satisfies both constraint sets. -/
theorem spatial_witness :
    ∃ M, Mod published M ∧ M.admits N (offer ++ request) :=
  ⟨chain, chain_models, spatial_compatible chain chain_models⟩

/-- Soundness: the intended structure, here the chain, admits a common
valuation. -/
theorem spatial_sound : chain.admits N (offer ++ request) :=
  sound_compatible chain chain_models spatial_verdict

/-- Both policies are well sorted at the mereological sort. -/
theorem spatial_wellSorted :
    ConstraintSet.wellSorted Srt.mer (offer ++ request) := by
  intro it hit
  simp only [offer, request, List.mem_append, List.mem_singleton] at hit
  rcases hit with rfl | rfl
  · exact rfl
  · exact True.intro

end OdrlGrounded.Example.Spatial
