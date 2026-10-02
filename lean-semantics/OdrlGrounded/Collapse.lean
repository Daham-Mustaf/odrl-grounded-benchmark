import OdrlGrounded.Grounding

set_option autoImplicit false

/-!
# Collapse: structures against preorders

Paper: Definition (Structure), Definition (Models).

The paper's structure is a partial order on an arbitrary carrier `P`, with an
interpretation `h : C → P`. The carrier may hold elements that no concept
names. Everything else in this development uses preorders on `C` (`Model`),
where mutual order means identity and disjointness quantifies over `C` only.
This file shows that the two give the same consistency and the same verdicts.

The structure side is written literally as in the paper, not by pushing atoms
forward along `h` and reusing `Model.satSet`. Denotations are sets of elements
of `P`, complements are taken in `P`, and the elements a valuation denotes are
`h x` for its values `x`. The theorems below then compare that reading with the
eqv-form on `C` that the earlier files use.

What is proved.

* `Structure.induced`: a structure gives a preorder on `C` by
  `a ≤ b` iff `h a ≤ h b`. Its mutual order is `h a = h b`, by antisymmetry.
* `Structure.sat_induced`: if a structure satisfies an assertion, so does its
  induced preorder.
* `Model.lift`: a preorder gives a structure whose elements are the down-sets
  of concepts. Every element is named. `Model.lift_induced` says the lift
  induces the preorder it came from, and `Model.sat_lift` says it satisfies
  whatever the preorder does.
* `Structure.admits_iff`: a structure admits a valuation for a constraint set
  iff its induced preorder does.
* `consistent_iff_structConsistent`, `compatible_iff_structCompatible`,
  `incompatible_iff_structIncompatible`, `verdict_eq_structVerdict` and
  `groundedVerdict_eq_struct`.

What is not claimed. A structure and its induced preorder need not satisfy the
same assertions. A structure with an unnamed element below both `h a` and
`h b` fails `a ⊥ b`, while its induced preorder looks only at named concepts
and can satisfy it. So `sat_induced` is an implication, and only the lift
preserves satisfaction exactly. The two sets of models differ, but each model on
one side has a partner on the other that admits the same valuations, and that is
all a verdict uses.
-/

namespace OdrlGrounded

/-- Definition (Structure): a partial order on a carrier `P` with an
interpretation `h` giving each concept an element. `P` may hold elements that no
concept names. -/
structure Structure (C : Type) where
  P : Type
  le : P → P → Prop
  refl : ∀ u, le u u
  trans : ∀ {u v w}, le u v → le v w → le u w
  antisymm : ∀ {u v}, le u v → le v u → u = v
  h : C → P

namespace Structure

variable {C : Type}

/-- Satisfaction of an assertion, as in Definition (Structure). Disjointness
quantifies over the whole carrier, unnamed elements included. -/
def sat (S : Structure C) : Assertion C → Prop
  | .below a b => S.le (S.h a) (S.h b)
  | .same a b => S.h a = S.h b
  | .distinct a b => S.h a ≠ S.h b
  | .disjoint a b => ∀ u : S.P, ¬ (S.le u (S.h a) ∧ S.le u (S.h b))

/-- `S.Models T`: the structure satisfies every assertion of `T = R ∪ B`. -/
def Models (S : Structure C) (T : List (Assertion C)) : Prop :=
  ∀ a ∈ T, S.sat a

/-- Table (denotation) in a structure: the elements a constraint accepts.
Complements are taken in the whole carrier. -/
def sem (S : Structure C) : Atom C → S.P → Prop
  | .eq g, u => u = S.h g
  | .neq g, u => u ≠ S.h g
  | .isAnyOf gs, u => ∃ g ∈ gs, u = S.h g
  | .isAllOf gs, u => ∃ g ∈ gs, u = S.h g
  | .isNoneOf gs, u => ∀ g ∈ gs, u ≠ S.h g
  | .isA g, u => S.le u (S.h g)
  | .isPartOf g, u => S.le u (S.h g)
  | .hasPart g, u => S.le (S.h g) u

/-- The elements the values of a valuation denote, `h x` for each value `x`. -/
def vals (S : Structure C) (ρ : List C) (u : S.P) : Prop :=
  ∃ x ∈ ρ, S.h x = u

/-- Definition (Valuation and satisfaction), one atomic constraint. -/
def satAtom (S : Structure C) (ρ : List C) (a : Atom C) : Prop :=
  match a.mode with
  | .meets => ∃ u, S.vals ρ u ∧ S.sem a u
  | .superset => ∀ u, S.sem a u → S.vals ρ u
  | .subset => ∀ u, S.vals ρ u → S.sem a u

/-- One member of a constraint set. `xone` is by position, as in
`Model.satItem`. -/
def satItem (S : Structure C) (ρ : List C) : Item C → Prop
  | .atom a => S.satAtom ρ a
  | .or alts => ∃ a ∈ alts, S.satAtom ρ a
  | .xone alts =>
      ∃ (i : Nat) (hi : i < alts.length),
        S.satAtom ρ alts[i] ∧
        ∀ (j : Nat) (hj : j < alts.length), j ≠ i → ¬ S.satAtom ρ alts[j]

def satSet (S : Structure C) (ρ : List C) (t : ConstraintSet C) : Prop :=
  ∀ it ∈ t, S.satItem ρ it

/-- The structure admits a nonempty valuation, with values in the candidate set
`N`, that satisfies the constraint set. -/
def admits (S : Structure C) (N : C → Prop) (t : ConstraintSet C) : Prop :=
  ∃ ρ : List C, ρ ≠ [] ∧ (∀ x ∈ ρ, N x) ∧ S.satSet ρ t

end Structure

section

variable {C : Type}

/-- Definition (Models), over structures: the pair is consistent when some
structure satisfies it. -/
def StructConsistent (T : List (Assertion C)) : Prop :=
  ∃ S : Structure C, S.Models T

/-- Every structure that satisfies `T` admits a common valuation. -/
def StructCompatible (T : List (Assertion C)) (N : C → Prop)
    (t t' : ConstraintSet C) : Prop :=
  ∀ S : Structure C, S.Models T → S.admits N (t ++ t')

/-- No structure that satisfies `T` admits a common valuation. -/
def StructIncompatible (T : List (Assertion C)) (N : C → Prop)
    (t t' : ConstraintSet C) : Prop :=
  ∀ S : Structure C, S.Models T → ¬ S.admits N (t ++ t')

open Classical in
noncomputable def structVerdict (T : List (Assertion C)) (N : C → Prop)
    (t t' : ConstraintSet C) : Verdict :=
  if StructCompatible T N t t' then Verdict.compatible
  else if StructIncompatible T N t t' then Verdict.incompatible
  else Verdict.unknown

end

/-! ## From a structure to a preorder -/

namespace Model

variable {C : Type}

/-- `satAtom` in `subset` mode. -/
theorem satAtom_of_subset (M : Model C) (ρ : List C) (a : Atom C)
    (h : a.mode = Mode.subset) :
    M.satAtom ρ a ↔ ∀ y, M.elems ρ y → a.denot M y := by
  first
    | (simp only [Model.satAtom, h]; done)
    | (unfold Model.satAtom; rw [h]; try exact Iff.rfl)

/-- `satAtom` in `meets` mode. -/
theorem satAtom_of_meets (M : Model C) (ρ : List C) (a : Atom C)
    (h : a.mode = Mode.meets) :
    M.satAtom ρ a ↔ ∃ y, M.elems ρ y ∧ a.denot M y := by
  first
    | (simp only [Model.satAtom, h]; done)
    | (unfold Model.satAtom; rw [h]; try exact Iff.rfl)

/-- `satAtom` in `superset` mode. -/
theorem satAtom_of_superset (M : Model C) (ρ : List C) (a : Atom C)
    (h : a.mode = Mode.superset) :
    M.satAtom ρ a ↔ ∀ y, a.denot M y → M.elems ρ y := by
  first
    | (simp only [Model.satAtom, h]; done)
    | (unfold Model.satAtom; rw [h]; try exact Iff.rfl)

end Model

namespace Structure

variable {C : Type}

theorem satAtom_of_subset (S : Structure C) (ρ : List C) (a : Atom C)
    (h : a.mode = Mode.subset) :
    S.satAtom ρ a ↔ ∀ u, S.vals ρ u → S.sem a u := by
  first
    | (simp only [Structure.satAtom, h]; done)
    | (unfold Structure.satAtom; rw [h]; try exact Iff.rfl)

theorem satAtom_of_meets (S : Structure C) (ρ : List C) (a : Atom C)
    (h : a.mode = Mode.meets) :
    S.satAtom ρ a ↔ ∃ u, S.vals ρ u ∧ S.sem a u := by
  first
    | (simp only [Structure.satAtom, h]; done)
    | (unfold Structure.satAtom; rw [h]; try exact Iff.rfl)

theorem satAtom_of_superset (S : Structure C) (ρ : List C) (a : Atom C)
    (h : a.mode = Mode.superset) :
    S.satAtom ρ a ↔ ∀ u, S.sem a u → S.vals ρ u := by
  first
    | (simp only [Structure.satAtom, h]; done)
    | (unfold Structure.satAtom; rw [h]; try exact Iff.rfl)

/-- The preorder a structure induces on the concepts. -/
def induced (S : Structure C) : Model C where
  le := fun a b => S.le (S.h a) (S.h b)
  refl := fun a => S.refl (S.h a)
  trans := fun h1 h2 => S.trans h1 h2

/-- In the induced preorder, mutual order is equality of denotations. This is
where antisymmetry of the structure is used. -/
theorem induced_eqv (S : Structure C) (a b : C) :
    S.induced.eqv a b ↔ S.h a = S.h b := by
  constructor
  · intro h
    obtain ⟨h1, h2⟩ := h
    have h1' : S.le (S.h a) (S.h b) := h1
    have h2' : S.le (S.h b) (S.h a) := h2
    exact S.antisymm h1' h2'
  · intro h
    have h1 : S.le (S.h a) (S.h b) := by
      rw [h]
      exact S.refl _
    have h2 : S.le (S.h b) (S.h a) := by
      rw [h]
      exact S.refl _
    exact ⟨h1, h2⟩

theorem elems_iff (S : Structure C) (ρ : List C) (y : C) :
    S.induced.elems ρ y ↔ S.vals ρ (S.h y) := by
  constructor
  · rintro ⟨x, hx, hxy⟩
    exact ⟨x, hx, (S.induced_eqv x y).mp hxy⟩
  · rintro ⟨x, hx, hxy⟩
    exact ⟨x, hx, (S.induced_eqv x y).mpr hxy⟩

/-- The eqv-form of Table (denotation) on `C` agrees with the structure's table
on the element a concept denotes. -/
theorem sem_iff (S : Structure C) (a : Atom C) (y : C) :
    a.denot S.induced y ↔ S.sem a (S.h y) := by
  cases a with
  | eq g => exact S.induced_eqv y g
  | neq g =>
    constructor
    · intro h h2
      exact h ((S.induced_eqv y g).mpr h2)
    · intro h h2
      exact h ((S.induced_eqv y g).mp h2)
  | isAnyOf gs =>
    constructor
    · rintro ⟨g, hg, h⟩
      exact ⟨g, hg, (S.induced_eqv y g).mp h⟩
    · rintro ⟨g, hg, h⟩
      exact ⟨g, hg, (S.induced_eqv y g).mpr h⟩
  | isAllOf gs =>
    constructor
    · rintro ⟨g, hg, h⟩
      exact ⟨g, hg, (S.induced_eqv y g).mp h⟩
    · rintro ⟨g, hg, h⟩
      exact ⟨g, hg, (S.induced_eqv y g).mpr h⟩
  | isNoneOf gs =>
    constructor
    · intro h g hg h2
      exact h g hg ((S.induced_eqv y g).mpr h2)
    · intro h g hg h2
      exact h g hg ((S.induced_eqv y g).mp h2)
  | isA _ => exact Iff.rfl
  | isPartOf _ => exact Iff.rfl
  | hasPart _ => exact Iff.rfl

theorem subset_iff (S : Structure C) (ρ : List C) (a : Atom C) :
    (∀ u, S.vals ρ u → S.sem a u) ↔
      (∀ y, S.induced.elems ρ y → a.denot S.induced y) := by
  constructor
  · intro H y hy
    exact (S.sem_iff a y).mpr (H _ ((S.elems_iff ρ y).mp hy))
  · intro H u hu
    obtain ⟨x, hx, rfl⟩ := hu
    exact (S.sem_iff a x).mp (H x ((S.elems_iff ρ x).mpr ⟨x, hx, rfl⟩))

theorem meets_iff (S : Structure C) (ρ : List C) (a : Atom C) :
    (∃ u, S.vals ρ u ∧ S.sem a u) ↔
      (∃ y, S.induced.elems ρ y ∧ a.denot S.induced y) := by
  constructor
  · rintro ⟨u, ⟨x, hx, rfl⟩, hu⟩
    exact ⟨x, (S.elems_iff ρ x).mpr ⟨x, hx, rfl⟩, (S.sem_iff a x).mpr hu⟩
  · rintro ⟨y, hy, hd⟩
    exact ⟨S.h y, (S.elems_iff ρ y).mp hy, (S.sem_iff a y).mp hd⟩

/-- The `superset` case needs every element of the denotation to be named. It
is, because `isAllOf` denotes a finite set of grounded concepts. -/
theorem superset_iff (S : Structure C) (ρ : List C) (a : Atom C)
    (hn : ∀ u, S.sem a u → ∃ y, S.h y = u) :
    (∀ u, S.sem a u → S.vals ρ u) ↔
      (∀ y, a.denot S.induced y → S.induced.elems ρ y) := by
  constructor
  · intro H y hy
    exact (S.elems_iff ρ y).mpr (H _ ((S.sem_iff a y).mp hy))
  · intro H u hu
    obtain ⟨y, rfl⟩ := hn u hu
    exact (S.elems_iff ρ y).mp (H y ((S.sem_iff a y).mpr hu))

theorem satAtom_iff_of_subset (S : Structure C) (ρ : List C) (a : Atom C)
    (hm : a.mode = Mode.subset) :
    S.satAtom ρ a ↔ S.induced.satAtom ρ a :=
  (S.satAtom_of_subset ρ a hm).trans
    ((S.subset_iff ρ a).trans (S.induced.satAtom_of_subset ρ a hm).symm)

theorem satAtom_iff_of_meets (S : Structure C) (ρ : List C) (a : Atom C)
    (hm : a.mode = Mode.meets) :
    S.satAtom ρ a ↔ S.induced.satAtom ρ a :=
  (S.satAtom_of_meets ρ a hm).trans
    ((S.meets_iff ρ a).trans (S.induced.satAtom_of_meets ρ a hm).symm)

theorem satAtom_iff_of_superset (S : Structure C) (ρ : List C) (a : Atom C)
    (hm : a.mode = Mode.superset)
    (hn : ∀ u, S.sem a u → ∃ y, S.h y = u) :
    S.satAtom ρ a ↔ S.induced.satAtom ρ a :=
  (S.satAtom_of_superset ρ a hm).trans
    ((S.superset_iff ρ a hn).trans (S.induced.satAtom_of_superset ρ a hm).symm)

/-- One atomic constraint is satisfied in a structure iff it is satisfied in
the induced preorder. -/
theorem satAtom_iff (S : Structure C) (ρ : List C) (a : Atom C) :
    S.satAtom ρ a ↔ S.induced.satAtom ρ a := by
  cases a with
  | eq g => exact S.satAtom_iff_of_subset ρ (Atom.eq g) rfl
  | neq g => exact S.satAtom_iff_of_subset ρ (Atom.neq g) rfl
  | isAnyOf gs => exact S.satAtom_iff_of_meets ρ (Atom.isAnyOf gs) rfl
  | isAllOf gs =>
    refine S.satAtom_iff_of_superset ρ (Atom.isAllOf gs) rfl ?_
    intro u hu
    obtain ⟨g, _, hg⟩ := hu
    exact ⟨g, hg.symm⟩
  | isNoneOf gs => exact S.satAtom_iff_of_subset ρ (Atom.isNoneOf gs) rfl
  | isA g => exact S.satAtom_iff_of_subset ρ (Atom.isA g) rfl
  | isPartOf g => exact S.satAtom_iff_of_subset ρ (Atom.isPartOf g) rfl
  | hasPart g => exact S.satAtom_iff_of_subset ρ (Atom.hasPart g) rfl

theorem satItem_iff (S : Structure C) (ρ : List C) (it : Item C) :
    S.satItem ρ it ↔ S.induced.satItem ρ it := by
  cases it with
  | atom a => exact S.satAtom_iff ρ a
  | or alts =>
    constructor
    · rintro ⟨a, ha, h⟩
      exact ⟨a, ha, (S.satAtom_iff ρ a).mp h⟩
    · rintro ⟨a, ha, h⟩
      exact ⟨a, ha, (S.satAtom_iff ρ a).mpr h⟩
  | xone alts =>
    constructor
    · rintro ⟨i, hi, h1, h2⟩
      exact ⟨i, hi, (S.satAtom_iff ρ alts[i]).mp h1,
        fun j hj hne h => h2 j hj hne ((S.satAtom_iff ρ alts[j]).mpr h)⟩
    · rintro ⟨i, hi, h1, h2⟩
      exact ⟨i, hi, (S.satAtom_iff ρ alts[i]).mpr h1,
        fun j hj hne h => h2 j hj hne ((S.satAtom_iff ρ alts[j]).mp h)⟩

theorem satSet_iff (S : Structure C) (ρ : List C) (t : ConstraintSet C) :
    S.satSet ρ t ↔ S.induced.satSet ρ t :=
  ⟨fun h it hit => (S.satItem_iff ρ it).mp (h it hit),
   fun h it hit => (S.satItem_iff ρ it).mpr (h it hit)⟩

/-- A structure admits a valuation for a constraint set iff its induced
preorder does. -/
theorem admits_iff (S : Structure C) (N : C → Prop) (t : ConstraintSet C) :
    S.admits N t ↔ S.induced.admits N t := by
  constructor
  · rintro ⟨ρ, h1, h2, h3⟩
    exact ⟨ρ, h1, h2, (S.satSet_iff ρ t).mp h3⟩
  · rintro ⟨ρ, h1, h2, h3⟩
    exact ⟨ρ, h1, h2, (S.satSet_iff ρ t).mpr h3⟩

/-- What a structure satisfies, its induced preorder satisfies. Disjointness
goes one way only: the structure quantifies over unnamed elements as well. -/
theorem sat_induced (S : Structure C) {a : Assertion C} (h : S.sat a) :
    S.induced.sat a := by
  cases a with
  | below _ _ => exact h
  | same x y => exact (S.induced_eqv x y).mpr h
  | distinct x y => exact fun e => h ((S.induced_eqv x y).mp e)
  | disjoint _ _ =>
    intro z hz
    exact h (S.h z) hz

theorem models_induced (S : Structure C) {T : List (Assertion C)}
    (h : S.Models T) : Mod T S.induced :=
  fun a ha => S.sat_induced (h a ha)

end Structure

/-! ## From a preorder to a structure -/

namespace Model

variable {C : Type}

/-- The down-set of a concept. -/
def down (M : Model C) (c : C) : C → Prop := fun x => M.le x c

/-- The carrier of the lift: the down-sets of concepts. Every element is named. -/
abbrev Carrier (M : Model C) : Type := { s : C → Prop // ∃ c, s = M.down c }

/-- The structure of a preorder: down-sets ordered by inclusion, with each
concept interpreted as its own down-set. -/
def lift (M : Model C) : Structure C where
  P := M.Carrier
  le := fun s t => ∀ x, s.1 x → t.1 x
  refl := fun _ _ hx => hx
  trans := fun h1 h2 x hx => h2 x (h1 x hx)
  antisymm := fun h1 h2 => Subtype.ext (funext fun x => propext ⟨h1 x, h2 x⟩)
  h := fun c => ⟨M.down c, c, rfl⟩

theorem lift_le (M : Model C) (a b : C) :
    M.lift.induced.le a b ↔ M.le a b := by
  constructor
  · intro h
    exact h a (M.refl a)
  · intro h x hx
    have hx' : M.le x a := hx
    exact (M.trans hx' h : M.le x b)

/-- Two preorders with the same order are equal. -/
theorem ext_le {M M' : Model C} (h : ∀ a b, M.le a b ↔ M'.le a b) : M = M' := by
  cases M with
  | mk le refl trans =>
    cases M' with
    | mk le' refl' trans' =>
      have hle : le = le' := funext fun a => funext fun b => propext (h a b)
      subst hle
      rfl

/-- The lift induces the preorder it came from. -/
theorem lift_induced (M : Model C) : M.lift.induced = M :=
  ext_le (fun a b => M.lift_le a b)

theorem lift_h_eq (M : Model C) (x y : C) :
    M.lift.h x = M.lift.h y ↔ M.eqv x y := by
  refine (M.lift.induced_eqv x y).symm.trans ?_
  constructor
  · rintro ⟨e1, e2⟩
    exact ⟨(M.lift_le x y).mp e1, (M.lift_le y x).mp e2⟩
  · rintro ⟨e1, e2⟩
    exact ⟨(M.lift_le x y).mpr e1, (M.lift_le y x).mpr e2⟩

/-- The lift satisfies whatever the preorder does, disjointness included,
because every element of the lift is named. -/
theorem sat_lift (M : Model C) {a : Assertion C} (h : M.sat a) :
    M.lift.sat a := by
  cases a with
  | below x y => exact (M.lift_le x y).mpr h
  | same x y => exact (M.lift_h_eq x y).mpr h
  | distinct x y => exact fun e => h ((M.lift_h_eq x y).mp e)
  | disjoint x y =>
    rintro ⟨s, c, rfl⟩ ⟨h1, h2⟩
    have h1' : M.le c x := h1 c (M.refl c)
    have h2' : M.le c y := h2 c (M.refl c)
    exact h c ⟨h1', h2'⟩

theorem models_lift (M : Model C) {T : List (Assertion C)} (h : Mod T M) :
    M.lift.Models T :=
  fun a ha => M.sat_lift (h a ha)

end Model

/-! ## Collapse -/

section

variable {C : Type}

/-- A theory has a structure model iff it has a preorder model. -/
theorem consistent_iff_structConsistent (T : List (Assertion C)) :
    Consistent T ↔ StructConsistent T := by
  constructor
  · rintro ⟨M, hM⟩
    exact ⟨M.lift, M.models_lift hM⟩
  · rintro ⟨S, hS⟩
    exact ⟨S.induced, S.models_induced hS⟩

theorem compatible_iff_structCompatible (T : List (Assertion C)) (N : C → Prop)
    (t t' : ConstraintSet C) :
    Compatible T N t t' ↔ StructCompatible T N t t' := by
  constructor
  · intro H S hS
    have h1 : S.induced.admits N (t ++ t') := H S.induced (S.models_induced hS)
    exact (S.admits_iff N (t ++ t')).mpr h1
  · intro H M hM
    have h1 : M.lift.admits N (t ++ t') := H M.lift (M.models_lift hM)
    have h2 : M.lift.induced.admits N (t ++ t') :=
      (M.lift.admits_iff N (t ++ t')).mp h1
    rw [M.lift_induced] at h2
    exact h2

theorem incompatible_iff_structIncompatible (T : List (Assertion C)) (N : C → Prop)
    (t t' : ConstraintSet C) :
    Incompatible T N t t' ↔ StructIncompatible T N t t' := by
  constructor
  · intro H S hS hadm
    exact H S.induced (S.models_induced hS) ((S.admits_iff N (t ++ t')).mp hadm)
  · intro H M hM hadm
    have h2 : M.lift.induced.admits N (t ++ t') := by
      rw [M.lift_induced]
      exact hadm
    exact H M.lift (M.models_lift hM) ((M.lift.admits_iff N (t ++ t')).mpr h2)

/-- The verdict over preorders is the verdict over structures. Neither side
assumes that `(R, B)` is consistent. -/
theorem verdict_eq_structVerdict (T : List (Assertion C)) (N : C → Prop)
    (t t' : ConstraintSet C) :
    verdict T N t t' = structVerdict T N t t' := by
  unfold verdict structVerdict
  by_cases hc : Compatible T N t t'
  · have hs : StructCompatible T N t t' :=
      (compatible_iff_structCompatible T N t t').mp hc
    simp [hc, hs]
  · have hs : ¬ StructCompatible T N t t' :=
      fun h => hc ((compatible_iff_structCompatible T N t t').mpr h)
    by_cases hi : Incompatible T N t t'
    · have his : StructIncompatible T N t t' :=
        (incompatible_iff_structIncompatible T N t t').mp hi
      simp [hc, hs, hi, his]
    · have his : ¬ StructIncompatible T N t t' :=
        fun h => hi ((incompatible_iff_structIncompatible T N t t').mpr h)
      simp [hc, hs, hi, his]

end

/-- The grounded verdict over structures: `Unknown` when a value is
ungrounded, otherwise the verdict over structures. -/
noncomputable def groundedStructVerdict {V C : Type} (γ : Grounding V C)
    (T : List (Assertion C)) (t t' : ConstraintSet V) : Verdict :=
  match ConstraintSet.ground γ t, ConstraintSet.ground γ t' with
  | some g, some g' => structVerdict T (Grounding.range γ) g g'
  | _, _ => Verdict.unknown

theorem groundedVerdict_eq_struct {V C : Type} (γ : Grounding V C)
    (T : List (Assertion C)) (t t' : ConstraintSet V) :
    groundedVerdict γ T t t' = groundedStructVerdict γ T t t' := by
  unfold groundedVerdict groundedStructVerdict
  cases hl : ConstraintSet.ground γ t with
  | none => rfl
  | some g =>
    cases hr : ConstraintSet.ground γ t' with
    | none => rfl
    | some g' => exact verdict_eq_structVerdict T (Grounding.range γ) g g'

end OdrlGrounded
