import OdrlGrounded.Model

set_option autoImplicit false

/-!
# Grounded constraints and constraint sets

Paper: Definition (Signature and well-sortedness), Table (signature).

Atoms are already grounded: their arguments are concepts, so the grounding
`γ` has been applied. Ungrounded values are handled at the verdict level, not
here. The arity of each operator is part of the type. Logical Constraints
compose atomic constraints and do not nest. ODRL IM 2.5.2 requires the
operand values of a Logical Constraint to be Constraint instances and does
not mention nesting.
-/

namespace OdrlGrounded

/-- The three sorts: identity, subsumption, parthood. -/
inductive Srt where
  | nom
  | tax
  | mer
  deriving DecidableEq, Repr

/-- A grounded atomic constraint. -/
inductive Atom (C : Type) where
  | eq (g : C)
  | neq (g : C)
  | isAnyOf (gs : List C)
  | isAllOf (gs : List C)
  | isNoneOf (gs : List C)
  | isA (g : C)
  | isPartOf (g : C)
  | hasPart (g : C)
  deriving DecidableEq, Repr

/-- Table (signature). `isA` only at `tax`, `isPartOf` and `hasPart` only at
`mer`, every other operator at every sort. A set operator needs a nonempty set
of values. -/
def Atom.wellSorted {C : Type} (σ : Srt) : Atom C → Prop
  | .isA _ => σ = Srt.tax
  | .isPartOf _ => σ = Srt.mer
  | .hasPart _ => σ = Srt.mer
  | .isAnyOf gs | .isAllOf gs | .isNoneOf gs => gs ≠ []
  | _ => True

/-- `true` exactly for an `isAllOf` constraint. -/
def Atom.isAllOfAtom {C : Type} : Atom C → Bool
  | .isAllOf _ => true
  | _ => false

/-- One member of a constraint set: a constraint, or a Logical Constraint over
atomic constraints. An `odrl:and` needs no constructor, because its atoms are
members of the list. `xone` is by position, not by content. -/
inductive Item (C : Type) where
  | atom (a : Atom C)
  | or (alts : List (Atom C))
  | xone (alts : List (Atom C))
  deriving DecidableEq, Repr

/-- The constraints of one rule on one operand, conjoined. -/
abbrev ConstraintSet (C : Type) := List (Item C)

/-- Definition (Signature and well-sortedness). Every constraint is well
sorted, a Logical Constraint has at least one alternative, and no `xone`
alternative is an `isAllOf`. -/
def Item.wellSorted {C : Type} (σ : Srt) : Item C → Prop
  | .atom a => a.wellSorted σ
  | .or alts => alts ≠ [] ∧ ∀ a ∈ alts, a.wellSorted σ
  | .xone alts =>
      alts ≠ [] ∧ (∀ a ∈ alts, a.wellSorted σ) ∧
        ∀ a ∈ alts, a.isAllOfAtom = false

def ConstraintSet.wellSorted {C : Type} (σ : Srt) (t : ConstraintSet C) : Prop :=
  ∀ it ∈ t, it.wellSorted σ

end OdrlGrounded
