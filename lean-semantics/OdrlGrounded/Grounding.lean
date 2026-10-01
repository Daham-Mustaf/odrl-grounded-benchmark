import OdrlGrounded.Verdict

set_option autoImplicit false

/-!
# Grounding

Paper: Definition (Grounding), and the ungrounded clause of Definition
(Verdict).

A policy names concepts by values of type `V`. A grounding is a partial
function from values to concepts. A value outside its domain names no concept
of the binding. A constraint set that contains such a value has no denotation,
so the verdict is `Unknown`, whatever the theory says.

The candidate set `N` is the range of the grounding, because `γ` is onto the
binding's concept set `C_β`.
-/

namespace OdrlGrounded

/-- A grounding maps a value to a concept, or is undefined on it. -/
abbrev Grounding (V C : Type) := V → Option C

/-- Candidate set: the concepts that some value grounds to. -/
def Grounding.range {V C : Type} (γ : Grounding V C) : C → Prop :=
  fun c => ∃ v, γ v = some c

/-- Ground one atomic constraint. It is undefined when one of its values is. -/
def Atom.ground {V C : Type} (γ : Grounding V C) : Atom V → Option (Atom C)
  | .eq g => Option.map Atom.eq (γ g)
  | .neq g => Option.map Atom.neq (γ g)
  | .isAnyOf gs => Option.map Atom.isAnyOf (List.mapM γ gs)
  | .isAllOf gs => Option.map Atom.isAllOf (List.mapM γ gs)
  | .isNoneOf gs => Option.map Atom.isNoneOf (List.mapM γ gs)
  | .isA g => Option.map Atom.isA (γ g)
  | .isPartOf g => Option.map Atom.isPartOf (γ g)
  | .hasPart g => Option.map Atom.hasPart (γ g)

/-- Ground one member of a constraint set. -/
def Item.ground {V C : Type} (γ : Grounding V C) : Item V → Option (Item C)
  | .atom a => Option.map Item.atom (Atom.ground γ a)
  | .or alts => Option.map Item.or (List.mapM (Atom.ground γ) alts)
  | .xone alts => Option.map Item.xone (List.mapM (Atom.ground γ) alts)

/-- Ground a constraint set. One ungrounded value anywhere leaves the whole set
without a denotation. -/
def ConstraintSet.ground {V C : Type} (γ : Grounding V C)
    (t : ConstraintSet V) : Option (ConstraintSet C) :=
  List.mapM (Item.ground γ) t

/-- Definition (Verdict) with the ungrounded clause. If either side has an
ungrounded value the verdict is `Unknown`. Otherwise it is the verdict of the
grounded sets, with the range of `γ` as candidate set. -/
noncomputable def groundedVerdict {V C : Type} (γ : Grounding V C)
    (T : List (Assertion C)) (t t' : ConstraintSet V) : Verdict :=
  match ConstraintSet.ground γ t, ConstraintSet.ground γ t' with
  | some g, some g' => verdict T (Grounding.range γ) g g'
  | _, _ => Verdict.unknown

theorem groundedVerdict_of_left_none {V C : Type} (γ : Grounding V C)
    (T : List (Assertion C)) (t t' : ConstraintSet V)
    (h : ConstraintSet.ground γ t = none) :
    groundedVerdict γ T t t' = Verdict.unknown := by
  unfold groundedVerdict
  simp [h]

theorem groundedVerdict_of_right_none {V C : Type} (γ : Grounding V C)
    (T : List (Assertion C)) (t t' : ConstraintSet V)
    (h : ConstraintSet.ground γ t' = none) :
    groundedVerdict γ T t t' = Verdict.unknown := by
  unfold groundedVerdict
  cases hl : ConstraintSet.ground γ t with
  | none => rfl
  | some g => simp [h]

theorem groundedVerdict_of_some {V C : Type} (γ : Grounding V C)
    (T : List (Assertion C)) (t t' : ConstraintSet V)
    (g g' : ConstraintSet C)
    (h : ConstraintSet.ground γ t = some g)
    (h' : ConstraintSet.ground γ t' = some g') :
    groundedVerdict γ T t t' = verdict T (Grounding.range γ) g g' := by
  unfold groundedVerdict
  simp [h, h']

end OdrlGrounded
