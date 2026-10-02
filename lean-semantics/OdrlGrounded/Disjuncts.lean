import OdrlGrounded.Witness

set_option autoImplicit false

/-!
# Constraint sets as disjuncts

Paper: Lemma (Reduction of a constraint set), then the witness lemma.

A constraint set is a conjunction of members. A member is an atom, an `or`, or
an `xone`. Distributing the conjunction over the alternatives gives a list of
disjuncts, each a list of literals, and `M` admits a valuation exactly when
some disjunct satisfies W.

`or` contributes one disjunct per alternative. `xone` contributes one disjunct
per position: that alternative holds and every other one fails. A failing
alternative is a negated literal. A negated subset-mode atom is a `meets`
literal. A negated `isAnyOf` is a `within` literal, which is `isNoneOf`
(`negLit_isAnyOf_iff`). A negated `isAllOf` is not a literal but a
disjunction, which is why `xone` alternatives may not be `isAllOf`, as
required by well-sortedness.
-/

namespace OdrlGrounded

/-! ## Negated literals -/

theorem not_within_iff {C : Type} (M : Model C) (ρ : List C) (S : C → Prop) :
    ¬ (∀ y, M.elems ρ y → S y) ↔ ∃ y, M.elems ρ y ∧ ¬ S y := by
  constructor
  · intro h
    refine Classical.byContradiction fun hcon => h ?_
    intro y hy
    exact Classical.byContradiction fun hn => hcon ⟨y, hy, hn⟩
  · rintro ⟨y, hy, hn⟩ h
    exact hn (h y hy)

theorem not_meets_iff {C : Type} (M : Model C) (ρ : List C) (T : C → Prop) :
    ¬ (∃ y, M.elems ρ y ∧ T y) ↔ ∀ y, M.elems ρ y → ¬ T y := by
  constructor
  · intro h y hy hT
    exact h ⟨y, hy, hT⟩
  · rintro h ⟨y, hy, hT⟩
    exact h y hy hT

namespace Atom

variable {C : Type}

/-- The literal for the negation of an atomic constraint. For `isAllOf` there
is none, and the value here is never used, because well-sortedness excludes
`isAllOf` under `xone`. -/
def negLit (M : Model C) : Atom C → Lit C
  | .isAnyOf gs => .within (fun y => ¬ (Atom.isAnyOf gs).denot M y)
  | .isAllOf _ => .meets (fun _ => False)
  | a => .meets (fun y => ¬ a.denot M y)

theorem negLit_closed (M : Model C) (a : Atom C) :
    (Atom.negLit M a).closed M := by
  cases a with
  | eq _ => exact True.intro
  | neq _ => exact True.intro
  | isAnyOf gs =>
    intro x y hxy hx hy
    exact hx (Atom.denot_closed M (Atom.isAnyOf gs) y x (M.eqv_symm hxy) hy)
  | isAllOf _ => exact True.intro
  | isNoneOf _ => exact True.intro
  | isA _ => exact True.intro
  | isPartOf _ => exact True.intro
  | hasPart _ => exact True.intro

end Atom

/-- A negated atomic constraint holds exactly when its negated literal does. -/
theorem satAtom_neg_iff {C : Type} (M : Model C) (ρ : List C) (a : Atom C)
    (h : a.isAllOfAtom = false) :
    ¬ M.satAtom ρ a ↔ M.satLit ρ (Atom.negLit M a) := by
  cases a with
  | eq g => exact not_within_iff M ρ ((Atom.eq g).denot M)
  | neq g => exact not_within_iff M ρ ((Atom.neq g).denot M)
  | isAnyOf gs => exact not_meets_iff M ρ ((Atom.isAnyOf gs).denot M)
  | isAllOf _ => simp [Atom.isAllOfAtom] at h
  | isNoneOf gs => exact not_within_iff M ρ ((Atom.isNoneOf gs).denot M)
  | isA g => exact not_within_iff M ρ ((Atom.isA g).denot M)
  | isPartOf g => exact not_within_iff M ρ ((Atom.isPartOf g).denot M)
  | hasPart g => exact not_within_iff M ρ ((Atom.hasPart g).denot M)

/-- A negated `isAnyOf` is read as `isNoneOf`. -/
theorem negLit_isAnyOf_iff {C : Type} (M : Model C) (ρ : List C) (gs : List C) :
    M.satLit ρ (Atom.negLit M (Atom.isAnyOf gs)) ↔
      M.satLit ρ (Atom.lit M (Atom.isNoneOf gs)) := by
  constructor
  · intro h y hy g hg hyg
    exact h y hy ⟨g, hg, hyg⟩
  · intro h y hy hex
    obtain ⟨g, hg, hyg⟩ := hex
    exact h y hy g hg hyg

/-! ## Exactly one, by position -/

/-- Exactly one element satisfies `P`, counted by position. -/
def ExactlyOne {α : Type} (P : α → Prop) : List α → Prop
  | [] => False
  | a :: rest => (P a ∧ ∀ b ∈ rest, ¬ P b) ∨ (¬ P a ∧ ExactlyOne P rest)

/-- The recursive form agrees with the index form used in the semantics. -/
theorem exactlyOne_iff_index {α : Type} (P : α → Prop) :
    ∀ alts : List α, ExactlyOne P alts ↔
      ∃ (i : Nat) (hi : i < alts.length), P alts[i] ∧
        ∀ (j : Nat) (hj : j < alts.length), j ≠ i → ¬ P alts[j] := by
  intro alts
  induction alts with
  | nil =>
    constructor
    · intro h
      simp [ExactlyOne] at h
    · rintro ⟨i, hi, _⟩
      simp at hi
  | cons a rest ih =>
    simp only [ExactlyOne]
    constructor
    · rintro (⟨hPa, hrest⟩ | ⟨hna, hex⟩)
      · refine ⟨0, (by simp), (by simpa using hPa), ?_⟩
        intro j hj hne
        cases j with
        | zero => exact absurd rfl hne
        | succ j' =>
          have hj' : j' < rest.length := by
            simp only [List.length_cons] at hj
            omega
          have hmem : rest[j'] ∈ rest := by simp
          simpa using hrest _ hmem
      · obtain ⟨i, hi, hPi, hoth⟩ := ih.mp hex
        refine ⟨i + 1, (by simp only [List.length_cons]; omega),
          (by simpa using hPi), ?_⟩
        intro j hj hne
        cases j with
        | zero => simpa using hna
        | succ j' =>
          have hj' : j' < rest.length := by
            simp only [List.length_cons] at hj
            omega
          have hne' : j' ≠ i := fun h => hne (by rw [h])
          simpa using hoth j' hj' hne'
    · rintro ⟨i, hi, hPi, hoth⟩
      cases i with
      | zero =>
        left
        refine ⟨by simpa using hPi, ?_⟩
        intro b hb
        obtain ⟨j', hj', rfl⟩ := List.mem_iff_getElem.mp hb
        have h1 := hoth (j' + 1) (by simp only [List.length_cons]; omega)
          (by omega)
        simpa using h1
      | succ i' =>
        right
        refine ⟨?_, ?_⟩
        · have h0 := hoth 0 (by simp) (by omega)
          simpa using h0
        · refine ih.mpr ⟨i', ?_, ?_, ?_⟩
          · simp only [List.length_cons] at hi
            omega
          · simpa using hPi
          · intro j hj hne
            have h1 := hoth (j + 1) (by simp only [List.length_cons]; omega)
              (by omega)
            simpa using h1

/-! ## Disjuncts -/

/-- Disjuncts of an `xone`: for each position, that alternative holds and the
others fail. -/
def xoneDisj {C : Type} (M : Model C) : List (Atom C) → List (List (Lit C))
  | [] => []
  | a :: rest =>
      (Atom.lit M a :: rest.map (Atom.negLit M)) ::
        (xoneDisj M rest).map (fun l => Atom.negLit M a :: l)

/-- Disjuncts of one member of a constraint set. -/
def Item.disj {C : Type} (M : Model C) : Item C → List (List (Lit C))
  | .atom a => [[Atom.lit M a]]
  | .or alts => alts.map (fun a => [Atom.lit M a])
  | .xone alts => xoneDisj M alts

/-- Disjuncts of a constraint set: the conjunction is distributed over the
alternatives of its members. -/
def setDisj {C : Type} (M : Model C) : List (Item C) → List (List (Lit C))
  | [] => [[]]
  | it :: rest =>
      (Item.disj M it).flatMap fun K => (setDisj M rest).map fun K' => K ++ K'

theorem xone_disj_iff {C : Type} (M : Model C) (ρ : List C) :
    ∀ alts : List (Atom C), (∀ a ∈ alts, a.isAllOfAtom = false) →
      (ExactlyOne (M.satAtom ρ) alts ↔
        ∃ K ∈ xoneDisj M alts, ∀ l ∈ K, M.satLit ρ l) := by
  intro alts
  induction alts with
  | nil =>
    intro _
    simp [ExactlyOne, xoneDisj]
  | cons a rest ih =>
    intro hno
    have ha : a.isAllOfAtom = false := hno a (by simp)
    have hrest : ∀ b ∈ rest, b.isAllOfAtom = false :=
      fun b hb => hno b (by simp [hb])
    have ih' := ih hrest
    simp only [ExactlyOne, xoneDisj]
    constructor
    · rintro (⟨hPa, hothers⟩ | ⟨hna, hex⟩)
      · refine ⟨Atom.lit M a :: rest.map (Atom.negLit M), (by simp), ?_⟩
        intro l hl
        rcases List.mem_cons.mp hl with h | h
        · rw [h]
          exact (satAtom_iff_satLit M ρ a).mp hPa
        · obtain ⟨b, hb, rfl⟩ := List.mem_map.mp h
          exact (satAtom_neg_iff M ρ b (hrest b hb)).mp (hothers b hb)
      · obtain ⟨K, hK, hsK⟩ := ih'.mp hex
        refine ⟨Atom.negLit M a :: K, ?_, ?_⟩
        · exact List.mem_cons.mpr (Or.inr (List.mem_map.mpr ⟨K, hK, rfl⟩))
        · intro l hl
          rcases List.mem_cons.mp hl with h | h
          · rw [h]
            exact (satAtom_neg_iff M ρ a ha).mp hna
          · exact hsK l h
    · rintro ⟨K, hK, hsK⟩
      rcases List.mem_cons.mp hK with h | h
      · left
        rw [h] at hsK
        refine ⟨(satAtom_iff_satLit M ρ a).mpr (hsK _ (by simp)), ?_⟩
        intro b hb
        exact (satAtom_neg_iff M ρ b (hrest b hb)).mpr
          (hsK _ (List.mem_cons.mpr (Or.inr (List.mem_map.mpr ⟨b, hb, rfl⟩))))
      · right
        obtain ⟨K', hK', rfl⟩ := List.mem_map.mp h
        refine ⟨(satAtom_neg_iff M ρ a ha).mpr (hsK _ (by simp)), ?_⟩
        exact ih'.mpr ⟨K', hK', fun l hl =>
          hsK l (List.mem_cons.mpr (Or.inr hl))⟩

theorem satItem_iff_disj {C : Type} (M : Model C) (ρ : List C)
    (it : Item C) (h : it.xoneOk) :
    M.satItem ρ it ↔ ∃ K ∈ Item.disj M it, ∀ l ∈ K, M.satLit ρ l := by
  cases it with
  | atom a =>
    constructor
    · intro hs
      refine ⟨[Atom.lit M a], (by simp [Item.disj]), ?_⟩
      intro l hl
      have hl' : l = Atom.lit M a := by simpa using hl
      rw [hl']
      exact (satAtom_iff_satLit M ρ a).mp hs
    · rintro ⟨K, hK, hsK⟩
      have hK' : K = [Atom.lit M a] := by simpa [Item.disj] using hK
      rw [hK'] at hsK
      exact (satAtom_iff_satLit M ρ a).mpr (hsK _ (by simp))
  | or alts =>
    constructor
    · rintro ⟨a, ha, hs⟩
      refine ⟨[Atom.lit M a], ?_, ?_⟩
      · show [Atom.lit M a] ∈ alts.map (fun a => [Atom.lit M a])
        exact List.mem_map.mpr ⟨a, ha, rfl⟩
      · intro l hl
        have hl' : l = Atom.lit M a := by simpa using hl
        rw [hl']
        exact (satAtom_iff_satLit M ρ a).mp hs
    · rintro ⟨K, hK, hsK⟩
      have hK2 : K ∈ alts.map (fun a => [Atom.lit M a]) := hK
      obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hK2
      exact ⟨a, ha, (satAtom_iff_satLit M ρ a).mpr (hsK _ (by simp))⟩
  | xone alts =>
    have hno : ∀ a ∈ alts, a.isAllOfAtom = false := by
      simp only [Item.xoneOk] at h
      exact h
    exact (exactlyOne_iff_index (M.satAtom ρ) alts).symm.trans
      (xone_disj_iff M ρ alts hno)

theorem satSet_iff_disj {C : Type} (M : Model C) (ρ : List C) :
    ∀ t : List (Item C), (∀ it ∈ t, it.xoneOk) →
      (M.satSet ρ t ↔ ∃ K ∈ setDisj M t, ∀ l ∈ K, M.satLit ρ l) := by
  intro t
  induction t with
  | nil =>
    intro _
    constructor
    · intro _
      exact ⟨[], (by simp [setDisj]), fun l hl => by simp at hl⟩
    · intro _ it hit
      simp at hit
  | cons it rest ih =>
    intro ht
    have hit : it.xoneOk := ht it (by simp)
    have hrest : ∀ x ∈ rest, x.xoneOk := fun x hx => ht x (by simp [hx])
    have ih' := ih hrest
    simp only [setDisj]
    constructor
    · intro h
      obtain ⟨K1, hK1, hs1⟩ :=
        (satItem_iff_disj M ρ it hit).mp (h it (by simp))
      obtain ⟨K2, hK2, hs2⟩ := ih'.mp (fun x hx => h x (by simp [hx]))
      refine ⟨K1 ++ K2, ?_, ?_⟩
      · exact List.mem_flatMap.mpr ⟨K1, hK1, List.mem_map.mpr ⟨K2, hK2, rfl⟩⟩
      · intro l hl
        rcases List.mem_append.mp hl with h' | h'
        · exact hs1 l h'
        · exact hs2 l h'
    · rintro ⟨K, hK, hs⟩
      obtain ⟨K1, hK1, hK'⟩ := List.mem_flatMap.mp hK
      obtain ⟨K2, hK2, rfl⟩ := List.mem_map.mp hK'
      have hitsat : M.satItem ρ it :=
        (satItem_iff_disj M ρ it hit).mpr
          ⟨K1, hK1, fun l hl => hs l (List.mem_append.mpr (Or.inl hl))⟩
      have hrestsat : M.satSet ρ rest :=
        ih'.mpr ⟨K2, hK2, fun l hl => hs l (List.mem_append.mpr (Or.inr hl))⟩
      intro x hx
      rcases List.mem_cons.mp hx with h | h
      · rw [h]
        exact hitsat
      · exact hrestsat x h

/-! ## Closure of the literals -/

theorem xoneDisj_closed {C : Type} (M : Model C) :
    ∀ alts : List (Atom C), ∀ K ∈ xoneDisj M alts, ∀ l ∈ K, l.closed M := by
  intro alts
  induction alts with
  | nil =>
    intro K hK
    simp [xoneDisj] at hK
  | cons a rest ih =>
    intro K hK l hl
    simp only [xoneDisj] at hK
    rcases List.mem_cons.mp hK with h | h
    · rw [h] at hl
      rcases List.mem_cons.mp hl with h' | h'
      · rw [h']
        exact Atom.lit_closed M a
      · obtain ⟨b, _, rfl⟩ := List.mem_map.mp h'
        exact Atom.negLit_closed M b
    · obtain ⟨K', hK', rfl⟩ := List.mem_map.mp h
      rcases List.mem_cons.mp hl with h' | h'
      · rw [h']
        exact Atom.negLit_closed M a
      · exact ih K' hK' l h'

theorem Item.disj_closed {C : Type} (M : Model C) (it : Item C) :
    ∀ K ∈ Item.disj M it, ∀ l ∈ K, l.closed M := by
  cases it with
  | atom a =>
    intro K hK l hl
    have hK' : K = [Atom.lit M a] := by simpa [Item.disj] using hK
    rw [hK'] at hl
    have hl' : l = Atom.lit M a := by simpa using hl
    rw [hl']
    exact Atom.lit_closed M a
  | or alts =>
    intro K hK l hl
    have hK2 : K ∈ alts.map (fun a => [Atom.lit M a]) := hK
    obtain ⟨a, _, rfl⟩ := List.mem_map.mp hK2
    have hl' : l = Atom.lit M a := by simpa using hl
    rw [hl']
    exact Atom.lit_closed M a
  | xone alts => exact xoneDisj_closed M alts

theorem setDisj_closed {C : Type} (M : Model C) :
    ∀ t : List (Item C), ∀ K ∈ setDisj M t, ∀ l ∈ K, l.closed M := by
  intro t
  induction t with
  | nil =>
    intro K hK l hl
    have hK' : K = [] := by simpa [setDisj] using hK
    rw [hK'] at hl
    simp at hl
  | cons it rest ih =>
    intro K hK l hl
    simp only [setDisj] at hK
    obtain ⟨K1, hK1, hK'⟩ := List.mem_flatMap.mp hK
    obtain ⟨K2, hK2, rfl⟩ := List.mem_map.mp hK'
    rcases List.mem_append.mp hl with h | h
    · exact Item.disj_closed M it K1 hK1 l h
    · exact ih K2 hK2 l h

/-! ## The reduction -/

/-- A model admits a valuation for a constraint set exactly when some disjunct
satisfies W. The set needs no `isAllOf` under `xone`, which well-sortedness
gives (`ConstraintSet.xoneOk_of_wellSorted`). -/
theorem admits_iff_exists_witness {C : Type} (M : Model C) (N : C → Prop)
    (t : ConstraintSet C) (ht : t.xoneOk) :
    M.admits N t ↔ ∃ K ∈ setDisj M t, M.witness N K := by
  constructor
  · rintro ⟨ρ, hne, hN, hsat⟩
    obtain ⟨K, hK, hsK⟩ := (satSet_iff_disj M ρ t ht).mp hsat
    exact ⟨K, hK, (Model.witness_iff M N K (setDisj_closed M t K hK)).mp
      ⟨ρ, hne, hN, hsK⟩⟩
  · rintro ⟨K, hK, hw⟩
    obtain ⟨ρ, hne, hN, hsK⟩ :=
      (Model.witness_iff M N K (setDisj_closed M t K hK)).mpr hw
    exact ⟨ρ, hne, hN, (satSet_iff_disj M ρ t ht).mpr ⟨K, hK, hsK⟩⟩

end OdrlGrounded
