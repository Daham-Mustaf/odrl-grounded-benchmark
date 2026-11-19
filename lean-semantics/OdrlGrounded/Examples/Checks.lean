import OdrlGrounded.VerdictProperties

set_option autoImplicit false

/-!
# Example (Checks)

Offer: German or French, `or (eq de, eq fr)`. Request: any language except
Italian, `neq it`. Concepts from the BCP 47 binding. Published statements: none.

* Without a declaration the verdict is `Unknown`.
* Under the declaration `de ≠ fr` the verdict is `Compatible`.
* Under the same declaration, each alternative of the offer taken alone
  (`eq de` against `neq it`, `eq fr` against `neq it`) has the verdict
  `Unknown`. The verdict of the offer is therefore not obtained by combining the
  verdicts of the alternatives.
-/

namespace OdrlGrounded.Example.Checks

abbrev L := Fin 3
abbrev de : L := 0
abbrev fr : L := 1
abbrev it : L := 2

/-- The concept set: the binding's whole set of concepts. -/
def N : L → Prop := fun _ => True

def offer : ConstraintSet L := [.or [.eq de, .eq fr]]
def offerDe : ConstraintSet L := [.atom (.eq de)]
def offerFr : ConstraintSet L := [.atom (.eq fr)]
def request : ConstraintSet L := [.atom (.neq it)]

/-- The participants' declaration `de ≠ fr`. -/
def decl : List (Statement L) := [Statement.distinct de fr]

/-- A concept order in which two concepts are one element exactly when a key
gives them the same number. -/
def byKey (f : L → Nat) : ConceptOrder L where
  le := fun a b => f a = f b
  refl := fun _ => rfl
  trans := fun h₁ h₂ => Eq.trans h₁ h₂

theorem byKey_eqv (f : L → Nat) (a b : L) : (byKey f).eqv a b ↔ f a = f b :=
  ⟨fun h => h.1, fun h => ⟨h, h.symm⟩⟩

/-- A one-value valuation satisfies `eq g` when the value and `g` are one element. -/
theorem sat_eq_single (M : ConceptOrder L) (x g : L) (h : M.eqv x g) :
    M.satAtom [x] (Atom.eq g) := by
  show ∀ y, M.elems [x] y → M.eqv y g
  intro y hy
  obtain ⟨z, hz, hzy⟩ := hy
  simp at hz
  subst hz
  exact M.eqv_trans (M.eqv_symm hzy) h

/-- A one-value valuation satisfies `neq g` when the value and `g` are two elements. -/
theorem sat_neq_single (M : ConceptOrder L) (x g : L) (h : ¬ M.eqv x g) :
    M.satAtom [x] (Atom.neq g) := by
  show ∀ y, M.elems [x] y → ¬ M.eqv y g
  intro y hy hyg
  obtain ⟨z, hz, hzy⟩ := hy
  simp at hz
  subst hz
  exact h (M.eqv_trans hzy hyg)

/-- Every value of a valuation that satisfies `neq g` is a different element from `g`. -/
theorem neq_of_sat (M : ConceptOrder L) (x : L) (xs : List L) (g : L)
    (h : M.satAtom (x :: xs) (Atom.neq g)) : ¬ M.eqv x g := by
  have h' : ∀ y, M.elems (x :: xs) y → ¬ M.eqv y g := h
  exact h' x ⟨x, by simp, M.eqv_refl x⟩

/-- Every value of a valuation that satisfies `eq g` is the same element as `g`. -/
theorem eq_of_sat (M : ConceptOrder L) (x : L) (xs : List L) (g : L)
    (h : M.satAtom (x :: xs) (Atom.eq g)) : M.eqv x g := by
  have h' : ∀ y, M.elems (x :: xs) y → M.eqv y g := h
  exact h' x ⟨x, by simp, M.eqv_refl x⟩

/-! ## The offer with both alternatives -/

/-- Under `de ≠ fr`, every concept order admits a common valuation: German when
`de` and `it` are two elements, French otherwise. -/
theorem declared_compatible : Compatible decl N offer request := by
  intro M hM
  have hd : ¬ M.eqv de fr := hM (Statement.distinct de fr) (by simp [decl])
  by_cases h : M.eqv de it
  · have hfr : ¬ M.eqv fr it := fun h2 => hd (M.eqv_trans h (M.eqv_symm h2))
    refine ⟨[fr], by simp, by simp [N], ?_⟩
    intro i hi
    simp only [offer, request, List.mem_append, List.mem_singleton] at hi
    rcases hi with rfl | rfl
    · exact ⟨Atom.eq fr, by simp, sat_eq_single M fr fr (M.eqv_refl fr)⟩
    · exact sat_neq_single M fr it hfr
  · refine ⟨[de], by simp, by simp [N], ?_⟩
    intro i hi
    simp only [offer, request, List.mem_append, List.mem_singleton] at hi
    rcases hi with rfl | rfl
    · exact ⟨Atom.eq de, by simp, sat_eq_single M de de (M.eqv_refl de)⟩
    · exact sat_neq_single M de it h

theorem declared_verdict : verdict decl N offer request = Verdict.compatible :=
  verdict_eq_compatible_iff.mpr declared_compatible

/-- With all three concepts one element, no valuation satisfies `neq it`. -/
theorem not_compatible : ¬ Compatible [] N offer request := by
  intro h
  obtain ⟨ρ, hne, _, hsat⟩ := h (byKey fun _ => 0) (by simp [Mod])
  cases ρ with
  | nil => exact absurd rfl hne
  | cons x xs =>
    have h2 : (byKey fun _ => 0).satAtom (x :: xs) (Atom.neq it) :=
      hsat (Item.atom (Atom.neq it)) (by simp [offer, request])
    exact neq_of_sat _ x xs it h2 ((byKey_eqv _ x it).mpr rfl)

/-- With three different elements, German satisfies the offer and the request. -/
theorem not_incompatible : ¬ Incompatible [] N offer request := by
  intro h
  refine h (byKey fun a => a.val) (by simp [Mod]) ⟨[de], by simp, by simp [N], ?_⟩
  intro i hi
  simp only [offer, request, List.mem_append, List.mem_singleton] at hi
  rcases hi with rfl | rfl
  · exact ⟨Atom.eq de, by simp, sat_eq_single _ de de (ConceptOrder.eqv_refl _ de)⟩
  · refine sat_neq_single _ de it ?_
    intro h
    exact absurd ((byKey_eqv _ de it).mp h) (by decide)

theorem undeclared_verdict : verdict [] N offer request = Verdict.unknown := by
  unfold verdict
  simp [not_compatible, not_incompatible]

/-! ## Each alternative alone, under the declaration `de ≠ fr` -/

/-- Key that makes `de` and `it` one element and keeps `fr` apart. -/
def keyDeIt : L → Nat := fun a => if a = fr then 1 else 0

/-- Key that makes `fr` and `it` one element and keeps `de` apart. -/
def keyFrIt : L → Nat := fun a => if a = de then 1 else 0

theorem mod_decl_of_key (f : L → Nat) (h : f de ≠ f fr) : Mod decl (byKey f) := by
  intro a ha
  simp [decl] at ha
  subst ha
  exact fun e => h ((byKey_eqv f de fr).mp e)

/-- `eq g` against `neq it` is not `Compatible` when some model of the declaration
makes `g` and `it` one element. -/
theorem alone_not_compatible (g : L) (f : L → Nat) (hf : f de ≠ f fr)
    (hg : f g = f it) : ¬ Compatible decl N [.atom (.eq g)] request := by
  intro h
  obtain ⟨ρ, hne, _, hsat⟩ := h (byKey f) (mod_decl_of_key f hf)
  cases ρ with
  | nil => exact absurd rfl hne
  | cons x xs =>
    have h1 : (byKey f).satAtom (x :: xs) (Atom.eq g) :=
      hsat (Item.atom (Atom.eq g)) (by simp [request])
    have h2 : (byKey f).satAtom (x :: xs) (Atom.neq it) :=
      hsat (Item.atom (Atom.neq it)) (by simp [request])
    have e1 : (byKey f).eqv x g := eq_of_sat _ x xs g h1
    have e2 : (byKey f).eqv g it := (byKey_eqv f g it).mpr hg
    exact neq_of_sat _ x xs it h2 (ConceptOrder.eqv_trans _ e1 e2)

/-- `eq g` against `neq it` is not `Incompatible` when some model of the
declaration keeps `g` and `it` apart. -/
theorem alone_not_incompatible (g : L) (f : L → Nat) (hf : f de ≠ f fr)
    (hg : f g ≠ f it) : ¬ Incompatible decl N [.atom (.eq g)] request := by
  intro h
  refine h (byKey f) (mod_decl_of_key f hf) ⟨[g], by simp, by simp [N], ?_⟩
  intro i hi
  simp only [request, List.cons_append, List.nil_append, List.mem_cons,
    List.not_mem_nil, or_false] at hi
  rcases hi with rfl | rfl
  · exact sat_eq_single _ g g (ConceptOrder.eqv_refl _ g)
  · exact sat_neq_single _ g it (fun e => hg ((byKey_eqv f g it).mp e))

theorem german_alone_verdict : verdict decl N offerDe request = Verdict.unknown := by
  have h1 : ¬ Compatible decl N offerDe request :=
    alone_not_compatible de keyDeIt (by decide) (by decide)
  have h2 : ¬ Incompatible decl N offerDe request :=
    alone_not_incompatible de (fun a => a.val) (by decide) (by decide)
  unfold verdict
  simp [h1, h2]

theorem french_alone_verdict : verdict decl N offerFr request = Verdict.unknown := by
  have h1 : ¬ Compatible decl N offerFr request :=
    alone_not_compatible fr keyFrIt (by decide) (by decide)
  have h2 : ¬ Incompatible decl N offerFr request :=
    alone_not_incompatible fr (fun a => a.val) (by decide) (by decide)
  unfold verdict
  simp [h1, h2]

end OdrlGrounded.Example.Checks
