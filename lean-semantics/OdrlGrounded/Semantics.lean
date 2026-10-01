import OdrlGrounded.Syntax

set_option autoImplicit false

/-!
# Denotation and satisfaction

Paper: Definition (Denotation), Table (denotation), Definition (Valuation and
satisfaction).

A valuation is a nonempty list of concepts, all in the candidate set `N`
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

/-- Table (denotation), as a predicate on concepts. -/
def denot (M : Model C) : Atom C → C → Prop
  | .eq g, x => M.eqv x g
  | .neq g, x => ¬ M.eqv x g
  | .isAnyOf gs, x => ∃ g ∈ gs, M.eqv x g
  | .isAllOf gs, x => ∃ g ∈ gs, M.eqv x g
  | .isNoneOf gs, x => ∀ g ∈ gs, ¬ M.eqv x g
  | .isA g, x => M.le x g
  | .isPartOf g, x => M.le x g
  | .hasPart g, x => M.le g x

end Atom

namespace Model

variable {C : Type}

/-- The elements denoted by the values of a valuation. -/
def elems (M : Model C) (ρ : List C) (y : C) : Prop :=
  ∃ x ∈ ρ, M.eqv x y

/-- Definition (Valuation and satisfaction), one atomic constraint. -/
def satAtom (M : Model C) (ρ : List C) (a : Atom C) : Prop :=
  match a.mode with
  | .meets => ∃ y, M.elems ρ y ∧ a.denot M y
  | .superset => ∀ y, a.denot M y → M.elems ρ y
  | .subset => ∀ y, M.elems ρ y → a.denot M y

/-- One member of a constraint set. `xone` holds when exactly one
alternative, counted by position, is satisfied. -/
def satItem (M : Model C) (ρ : List C) : Item C → Prop
  | .atom a => M.satAtom ρ a
  | .or alts => ∃ a ∈ alts, M.satAtom ρ a
  | .xone alts =>
      ∃ (i : Nat) (hi : i < alts.length),
        M.satAtom ρ alts[i] ∧
        ∀ (j : Nat) (hj : j < alts.length), j ≠ i → ¬ M.satAtom ρ alts[j]

/-- A constraint set is satisfied when every member is. -/
def satSet (M : Model C) (ρ : List C) (t : ConstraintSet C) : Prop :=
  ∀ it ∈ t, M.satItem ρ it

/-- `M` admits a valuation that satisfies the constraint set. The valuation is nonempty
and its values lie in the candidate set `N`. -/
def admits (M : Model C) (N : C → Prop) (t : ConstraintSet C) : Prop :=
  ∃ ρ : List C, ρ ≠ [] ∧ (∀ x ∈ ρ, N x) ∧ M.satSet ρ t

end Model

end OdrlGrounded
