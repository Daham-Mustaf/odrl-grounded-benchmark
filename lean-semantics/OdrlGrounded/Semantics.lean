import OdrlGrounded.Syntax

set_option autoImplicit false

/-!
# Denotation and satisfaction

Paper: Definition (Denotation), Definition (Satisfaction of constraints).

A valuation is a nonempty list of concepts, all in the concept set `N`
(`N = C_β`, the binding's whole concept set). Lists stand for finite sets.
Satisfaction uses the elements the values denote, as in the paper.
-/

namespace OdrlGrounded

/-- Satisfaction mode: `meets` for `isAnyOf`, `superset` for `isAllOf`,
`subset` for every other operator. -/
inductive Mode where
  | meets
  | superset
  | subset

namespace Atom

variable {C : Type}

def mode : Atom C → Mode
  | .isAnyOf _ => .meets
  | .isAllOf _ => .superset
  | .eq _ => .subset
  | .neq _ => .subset
  | .isNoneOf _ => .subset
  | .isA _ => .subset
  | .isPartOf _ => .subset
  | .hasPart _ => .subset

/-- Definition (Denotation), as a predicate on concepts. -/
def denot (M : ConceptOrder C) : Atom C → C → Prop
  | .eq g, x => M.eqv x g
  | .neq g, x => ¬ M.eqv x g
  | .isAnyOf gs, x => ∃ g ∈ gs, M.eqv x g
  | .isAllOf gs, x => ∃ g ∈ gs, M.eqv x g
  | .isNoneOf gs, x => ∀ g ∈ gs, ¬ M.eqv x g
  | .isA g, x => M.le x g
  | .isPartOf g, x => M.le x g
  | .hasPart g, x => M.le g x

end Atom

namespace ConceptOrder

variable {C : Type}

/-- The elements denoted by the values of a valuation. -/
def elems (M : ConceptOrder C) (ρ : List C) (y : C) : Prop :=
  ∃ x ∈ ρ, M.eqv x y

/-- Definition (Satisfaction of constraints), one atomic constraint. -/
def satAtom (M : ConceptOrder C) (ρ : List C) (a : Atom C) : Prop :=
  match a.mode with
  | .meets => ∃ y, M.elems ρ y ∧ a.denot M y
  | .superset => ∀ y, a.denot M y → M.elems ρ y
  | .subset => ∀ y, M.elems ρ y → a.denot M y

/-- One member of a constraint set. `xone` holds when exactly one
alternative, counted by position, is satisfied. -/
def satItem (M : ConceptOrder C) (ρ : List C) : Item C → Prop
  | .atom a => M.satAtom ρ a
  | .or alts => ∃ a ∈ alts, M.satAtom ρ a
  | .xone alts =>
      ∃ (i : Nat) (hi : i < alts.length),
        M.satAtom ρ alts[i] ∧
        ∀ (j : Nat) (hj : j < alts.length), j ≠ i → ¬ M.satAtom ρ alts[j]

/-- A constraint set is satisfied when every member is. -/
def satSet (M : ConceptOrder C) (ρ : List C) (t : ConstraintSet C) : Prop :=
  ∀ it ∈ t, M.satItem ρ it

/-- `M` admits a valuation that satisfies the constraint set. The valuation is nonempty
and its values lie in the concept set `N`. -/
def admits (M : ConceptOrder C) (N : C → Prop) (t : ConstraintSet C) : Prop :=
  ∃ ρ : List C, ρ ≠ [] ∧ (∀ x ∈ ρ, N x) ∧ M.satSet ρ t

end ConceptOrder

end OdrlGrounded
