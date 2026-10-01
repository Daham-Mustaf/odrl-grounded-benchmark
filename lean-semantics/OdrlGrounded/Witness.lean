import OdrlGrounded.Semantics

set_option autoImplicit false

/-!
# Witness lemma, for a conjunction of atomic constraints

Paper: Lemma (Witness), the condition W(K) with the candidate set `N`.

Each atomic constraint is a literal on the set of elements that a valuation
denotes. `within S`: every denoted element lies in `S` (every subset-mode
operator). `covers F`: every `g` in `F` is denoted (`isAllOf`). `meets T`:
some denoted element lies in `T` (`isAnyOf`).

`Model.cand` is the largest set of elements a valuation could denote: the
elements of values in `N` that satisfy every `within` literal. `Model.witness`
is W(K): the largest set is nonempty, contains every `covers` set, and meets
every `meets` set.

`witness_iff` says that a valuation exists exactly when W(K) holds. The
`within` predicates must be closed under identity of elements (`Lit.closed`).
Disjunction, `xone` and negation come in the next step.
-/

namespace OdrlGrounded

/-- A literal on the set of elements a valuation denotes. -/
inductive Lit (C : Type) where
  | within (S : C → Prop)
  | covers (F : List C)
  | meets (T : C → Prop)

namespace Lit

variable {C : Type}

/-- A `within` predicate respects identity of elements. -/
def closed (M : Model C) : Lit C → Prop
  | .within S => ∀ x y, M.eqv x y → S x → S y
  | .covers _ => True
  | .meets _ => True

/-- What a literal allows an element of the largest set to be. -/
def allows : Lit C → C → Prop
  | .within S, y => S y
  | .covers _, _ => True
  | .meets _, _ => True

/-- What a literal demands of the largest set `D`. -/
def needs (D : C → Prop) : Lit C → Prop
  | .within _ => True
  | .covers F => ∀ g ∈ F, D g
  | .meets T => ∃ y, D y ∧ T y

/-- The literal is met by a finite list of seed elements. -/
def seeded (ys : List C) : Lit C → Prop
  | .within _ => True
  | .covers F => ∀ g ∈ F, g ∈ ys
  | .meets T => ∃ y ∈ ys, T y

theorem seeded_mono {ys ys' : List C} (h : ∀ y, y ∈ ys → y ∈ ys') :
    ∀ l : Lit C, l.seeded ys → l.seeded ys' := by
  intro l hl
  cases l with
  | within _ => exact True.intro
  | covers _ =>
    intro g hg
    exact h g (hl g hg)
  | meets _ =>
    obtain ⟨y, hy, hT⟩ := hl
    exact ⟨y, h y hy, hT⟩

end Lit

/-- If the largest set meets every demand, finitely many seeds meet them all. -/
theorem seeds_exist {C : Type} (D : C → Prop) :
    ∀ K : List (Lit C), (∀ l ∈ K, l.needs D) →
      ∃ ys : List C, (∀ y ∈ ys, D y) ∧ ∀ l ∈ K, l.seeded ys := by
  intro K
  induction K with
  | nil =>
    intro _
    exact ⟨[], fun y hy => by simp at hy, fun l hl => by simp at hl⟩
  | cons l K ih =>
    intro hn
    obtain ⟨ys, hD, hs⟩ := ih (fun l' hl' => hn l' (by simp [hl']))
    have hl : l.needs D := hn l (by simp)
    cases l with
    | within _ =>
      refine ⟨ys, hD, ?_⟩
      intro l' hl'
      rcases List.mem_cons.mp hl' with h | h
      · rw [h]
        exact True.intro
      · exact hs l' h
    | covers F =>
      have hF : ∀ g ∈ F, D g := hl
      refine ⟨F ++ ys, ?_, ?_⟩
      · intro y hy
        rcases List.mem_append.mp hy with h | h
        · exact hF y h
        · exact hD y h
      · intro l' hl'
        rcases List.mem_cons.mp hl' with h | h
        · rw [h]
          intro g hg
          exact List.mem_append.mpr (Or.inl hg)
        · exact Lit.seeded_mono (fun y hy => List.mem_append.mpr (Or.inr hy))
            l' (hs l' h)
    | meets _ =>
      obtain ⟨y, hDy, hT⟩ := hl
      refine ⟨y :: ys, ?_, ?_⟩
      · intro z hz
        rcases List.mem_cons.mp hz with h | h
        · rw [h]
          exact hDy
        · exact hD z h
      · intro l' hl'
        rcases List.mem_cons.mp hl' with h | h
        · rw [h]
          exact ⟨y, by simp, hT⟩
        · exact Lit.seeded_mono (fun z hz => List.mem_cons.mpr (Or.inr hz))
            l' (hs l' h)

namespace Model

variable {C : Type}

/-- Satisfaction of a literal by a valuation. -/
def satLit (M : Model C) (ρ : List C) : Lit C → Prop
  | .within S => ∀ y, M.elems ρ y → S y
  | .covers F => ∀ g ∈ F, M.elems ρ g
  | .meets T => ∃ y, M.elems ρ y ∧ T y

/-- The largest set of elements a valuation could denote under `K`. -/
def cand (M : Model C) (N : C → Prop) (K : List (Lit C)) (y : C) : Prop :=
  (∃ x, N x ∧ M.eqv x y) ∧ ∀ l ∈ K, l.allows y

/-- W(K): the largest set is nonempty and meets every demand. -/
def witness (M : Model C) (N : C → Prop) (K : List (Lit C)) : Prop :=
  (∃ y, M.cand N K y) ∧ ∀ l ∈ K, l.needs (M.cand N K)

/-- Every seed has a representative value in `N`, and the representatives
denote exactly the seeds. -/
theorem reps_exist (M : Model C) (N : C → Prop) :
    ∀ ys : List C, (∀ y ∈ ys, ∃ x, N x ∧ M.eqv x y) →
      ∃ xs : List C, (∀ x ∈ xs, N x) ∧ (∀ y ∈ ys, ∃ x ∈ xs, M.eqv x y) ∧
        (∀ x ∈ xs, ∃ y ∈ ys, M.eqv x y) := by
  intro ys
  induction ys with
  | nil =>
    intro _
    exact ⟨[], fun x hx => by simp at hx, fun y hy => by simp at hy,
      fun x hx => by simp at hx⟩
  | cons y ys ih =>
    intro h
    obtain ⟨xs, hN, h1, h2⟩ := ih (fun z hz => h z (by simp [hz]))
    obtain ⟨x, hxN, hxy⟩ := h y (by simp)
    refine ⟨x :: xs, ?_, ?_, ?_⟩
    · intro z hz
      rcases List.mem_cons.mp hz with h' | h'
      · rw [h']
        exact hxN
      · exact hN z h'
    · intro z hz
      rcases List.mem_cons.mp hz with h' | h'
      · rw [h']
        exact ⟨x, by simp, hxy⟩
      · obtain ⟨w, hw, hwz⟩ := h1 z h'
        exact ⟨w, by simp [hw], hwz⟩
    · intro z hz
      rcases List.mem_cons.mp hz with h' | h'
      · rw [h']
        exact ⟨y, by simp, hxy⟩
      · obtain ⟨w, hw, hwz⟩ := h2 z h'
        exact ⟨w, by simp [hw], hwz⟩

/-- Witness lemma. A valuation with values in `N` that satisfies every
literal exists exactly when W(K) holds. -/
theorem witness_iff (M : Model C) (N : C → Prop) (K : List (Lit C))
    (hc : ∀ l ∈ K, l.closed M) :
    (∃ ρ : List C, ρ ≠ [] ∧ (∀ x ∈ ρ, N x) ∧ ∀ l ∈ K, M.satLit ρ l) ↔
      M.witness N K := by
  constructor
  · rintro ⟨ρ, hne, hN, hsat⟩
    have hsub : ∀ y, M.elems ρ y → M.cand N K y := by
      intro y hy
      obtain ⟨x, hx, hxy⟩ := hy
      refine ⟨⟨x, hN x hx, hxy⟩, ?_⟩
      intro l hl
      cases l with
      | within _ => exact hsat _ hl y ⟨x, hx, hxy⟩
      | covers _ => exact True.intro
      | meets _ => exact True.intro
    have hx : ∃ x, x ∈ ρ := by
      cases ρ with
      | nil => exact absurd rfl hne
      | cons x xs => exact ⟨x, by simp⟩
    obtain ⟨x0, hx0⟩ := hx
    refine ⟨⟨x0, hsub x0 ⟨x0, hx0, M.eqv_refl x0⟩⟩, ?_⟩
    intro l hl
    cases l with
    | within _ => exact True.intro
    | covers _ =>
      intro g hg
      exact hsub g (hsat _ hl g hg)
    | meets _ =>
      obtain ⟨y, hy, hT⟩ := hsat _ hl
      exact ⟨y, hsub y hy, hT⟩
  · rintro ⟨⟨y0, hy0⟩, hneeds⟩
    obtain ⟨ys, hD, hs⟩ := seeds_exist (M.cand N K) K hneeds
    have hD0 : ∀ y ∈ y0 :: ys, M.cand N K y := by
      intro y hy
      rcases List.mem_cons.mp hy with h | h
      · rw [h]
        exact hy0
      · exact hD y h
    obtain ⟨xs, hN, h1, h2⟩ :=
      reps_exist M N (y0 :: ys) (fun y hy => (hD0 y hy).1)
    obtain ⟨x0, hx0, _⟩ := h1 y0 (by simp)
    refine ⟨xs, ?_, hN, ?_⟩
    · intro h
      rw [h] at hx0
      simp at hx0
    · intro l hl
      cases l with
      | within S =>
        intro y hy
        obtain ⟨x, hx, hxy⟩ := hy
        obtain ⟨z, hz, hxz⟩ := h2 x hx
        have hSz : S z := (hD0 z hz).2 _ hl
        exact (hc _ hl) z y (M.eqv_trans (M.eqv_symm hxz) hxy) hSz
      | covers _ =>
        intro g hg
        have hg' : g ∈ y0 :: ys := by
          have hgs : g ∈ ys := hs _ hl g hg
          simp [hgs]
        obtain ⟨x, hx, hxg⟩ := h1 g hg'
        exact ⟨x, hx, hxg⟩
      | meets _ =>
        obtain ⟨y, hy, hT⟩ := hs _ hl
        have hy' : y ∈ y0 :: ys := by simp [hy]
        obtain ⟨x, hx, hxy⟩ := h1 y hy'
        exact ⟨y, ⟨x, hx, hxy⟩, hT⟩

end Model

/-! ## From atomic constraints to literals -/

namespace Atom

variable {C : Type}

/-- The literal an atomic constraint stands for, by its mode. -/
def lit (M : Model C) : Atom C → Lit C
  | .isAnyOf gs => .meets ((Atom.isAnyOf gs).denot M)
  | .isAllOf gs => .covers gs
  | a => .within (a.denot M)

/-- Every denotation is closed under identity of elements. -/
theorem denot_closed (M : Model C) (a : Atom C) :
    ∀ x y, M.eqv x y → a.denot M x → a.denot M y := by
  intro x y hxy
  cases a with
  | eq _ =>
    intro h
    exact M.eqv_trans (M.eqv_symm hxy) h
  | neq _ =>
    intro h hyg
    exact h (M.eqv_trans hxy hyg)
  | isAnyOf _ =>
    intro h
    obtain ⟨g, hg, hxg⟩ := h
    exact ⟨g, hg, M.eqv_trans (M.eqv_symm hxy) hxg⟩
  | isAllOf _ =>
    intro h
    obtain ⟨g, hg, hxg⟩ := h
    exact ⟨g, hg, M.eqv_trans (M.eqv_symm hxy) hxg⟩
  | isNoneOf _ =>
    intro h g hg hyg
    exact h g hg (M.eqv_trans hxy hyg)
  | isA _ =>
    intro h
    exact M.trans hxy.2 h
  | isPartOf _ =>
    intro h
    exact M.trans hxy.2 h
  | hasPart _ =>
    intro h
    exact M.trans h hxy.1

theorem lit_closed (M : Model C) (a : Atom C) : (Atom.lit M a).closed M := by
  cases a with
  | eq g => exact Atom.denot_closed M (Atom.eq g)
  | neq g => exact Atom.denot_closed M (Atom.neq g)
  | isAnyOf _ => exact True.intro
  | isAllOf _ => exact True.intro
  | isNoneOf gs => exact Atom.denot_closed M (Atom.isNoneOf gs)
  | isA g => exact Atom.denot_closed M (Atom.isA g)
  | isPartOf g => exact Atom.denot_closed M (Atom.isPartOf g)
  | hasPart g => exact Atom.denot_closed M (Atom.hasPart g)

end Atom

/-- An atomic constraint holds exactly when its literal does. For `isAllOf`
this uses that the denoted elements are closed under identity. -/
theorem satAtom_iff_satLit {C : Type} (M : Model C) (ρ : List C)
    (a : Atom C) : M.satAtom ρ a ↔ M.satLit ρ (Atom.lit M a) := by
  cases a with
  | eq _ => exact Iff.rfl
  | neq _ => exact Iff.rfl
  | isAnyOf _ => exact Iff.rfl
  | isAllOf _ =>
    constructor
    · intro h g hg
      exact h g ⟨g, hg, M.eqv_refl g⟩
    · intro h y hy
      obtain ⟨g, hg, hyg⟩ := hy
      obtain ⟨x, hx, hxg⟩ := h g hg
      exact ⟨x, hx, M.eqv_trans hxg (M.eqv_symm hyg)⟩
  | isNoneOf _ => exact Iff.rfl
  | isA _ => exact Iff.rfl
  | isPartOf _ => exact Iff.rfl
  | hasPart _ => exact Iff.rfl

/-- Witness lemma for a conjunction of atomic constraints. -/
theorem admits_atoms_iff {C : Type} (M : Model C) (N : C → Prop)
    (atoms : List (Atom C)) :
    M.admits N (atoms.map Item.atom) ↔
      M.witness N (atoms.map (Atom.lit M)) := by
  have hc : ∀ l ∈ atoms.map (Atom.lit M), l.closed M := by
    intro l hl
    obtain ⟨a, _, rfl⟩ := List.mem_map.mp hl
    exact Atom.lit_closed M a
  refine Iff.trans ?_ (Model.witness_iff M N _ hc)
  constructor
  · rintro ⟨ρ, hne, hN, hsat⟩
    refine ⟨ρ, hne, hN, ?_⟩
    intro l hl
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hl
    exact (satAtom_iff_satLit M ρ a).mp
      (hsat (Item.atom a) (List.mem_map.mpr ⟨a, ha, rfl⟩))
  · rintro ⟨ρ, hne, hN, hsat⟩
    refine ⟨ρ, hne, hN, ?_⟩
    intro it hit
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hit
    exact (satAtom_iff_satLit M ρ a).mpr
      (hsat _ (List.mem_map.mpr ⟨a, ha, rfl⟩))

end OdrlGrounded
