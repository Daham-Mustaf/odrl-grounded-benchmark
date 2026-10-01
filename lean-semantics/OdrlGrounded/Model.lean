set_option autoImplicit false

/-!
# Models and assertions

Paper: Definition (Resource and background theory), Definition (Structure),
Definition (Models).

A model over the concept type `C` is a preorder on `C`. Mutual order means
identity (`eqv`). The paper's structures (a partial order on an arbitrary
carrier plus an interpretation `h`) are related to this form in the collapse
step, not here.
-/

namespace OdrlGrounded

structure Model (C : Type) where
  le : C → C → Prop
  refl : ∀ a, le a a
  trans : ∀ {a b c}, le a b → le b c → le a c

namespace Model

variable {C : Type} (M : Model C)

/-- Two concepts denote the same element. -/
def eqv (a b : C) : Prop := M.le a b ∧ M.le b a

theorem eqv_refl (a : C) : M.eqv a a := ⟨M.refl a, M.refl a⟩

theorem eqv_symm {a b : C} (h : M.eqv a b) : M.eqv b a := ⟨h.2, h.1⟩

theorem eqv_trans {a b c : C} (h₁ : M.eqv a b) (h₂ : M.eqv b c) : M.eqv a c :=
  ⟨M.trans h₁.1 h₂.1, M.trans h₂.2 h₁.2⟩

end Model

/-- Assertions of a resource `R` or a background theory `B`. -/
inductive Assertion (C : Type) where
  | below (a b : C)
  | same (a b : C)
  | distinct (a b : C)
  | disjoint (a b : C)

namespace Model

variable {C : Type}

/-- Satisfaction of an assertion. Disjointness quantifies over the concepts
`C` only. The collapse step shows this loses nothing against the paper's
carrier with unnamed elements. -/
def sat (M : Model C) : Assertion C → Prop
  | .below a b => M.le a b
  | .same a b => M.eqv a b
  | .distinct a b => ¬ M.eqv a b
  | .disjoint a b => ∀ z, ¬ (M.le z a ∧ M.le z b)

end Model

/-- `Mod T M`: `M` is a model of the finite theory `T = R ∪ B`. -/
def Mod {C : Type} (T : List (Assertion C)) (M : Model C) : Prop :=
  ∀ a ∈ T, M.sat a

/-- `(R, B)` is consistent when it has a model. -/
def Consistent {C : Type} (T : List (Assertion C)) : Prop :=
  ∃ M : Model C, Mod T M

end OdrlGrounded
