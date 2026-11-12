import OdrlGrounded.Verdict

set_option autoImplicit false

/-!
# Running example, language row

Offer `eq de`, request `eq fr`, concepts from the BCP 47 binding.
Published statements: none. Without a declaration the verdict is `Unknown`.
Under the declaration `de ≠ fr` it is `Incompatible`.
-/

namespace OdrlGrounded.Example

abbrev L := Fin 2
abbrev de : L := 0
abbrev fr : L := 1

/-- The concept set: the binding's whole set of concepts. -/
def N : L → Prop := fun _ => True

def offer : ConstraintSet L := [.atom (.eq de)]
def request : ConstraintSet L := [.atom (.eq fr)]

/-- Identity only: every concept is its own element. -/
def discrete : ConceptOrder L where
  le := fun a b => a = b
  refl := fun _ => rfl
  trans := fun h₁ h₂ => Eq.trans h₁ h₂

/-- All concepts are one element. -/
def collapsed : ConceptOrder L where
  le := fun _ _ => True
  refl := fun _ => trivial
  trans := fun _ _ => trivial

/-- Any concept order that admits a common valuation identifies `de` and `fr`. -/
theorem admits_imp_eqv (M : ConceptOrder L) (h : M.admits N (offer ++ request)) :
    M.eqv de fr := by
  obtain ⟨ρ, hne, _, hsat⟩ := h
  cases ρ with
  | nil => exact absurd rfl hne
  | cons x xs =>
    have hs : ∀ it ∈ offer ++ request, M.satItem (x :: xs) it := hsat
    have h1 := hs (Item.atom (Atom.eq de)) (by simp [offer])
    have h2 := hs (Item.atom (Atom.eq fr)) (by simp [request])
    simp only [ConceptOrder.satItem, ConceptOrder.satAtom, Atom.mode, Atom.denot,
      ConceptOrder.elems] at h1 h2
    have a1 := h1 x ⟨x, by simp, M.eqv_refl x⟩
    have a2 := h2 x ⟨x, by simp, M.eqv_refl x⟩
    exact M.eqv_trans (M.eqv_symm a1) a2

theorem collapsed_admits : collapsed.admits N (offer ++ request) := by
  refine ⟨[de], by simp, by simp [N], ?_⟩
  intro it hit
  simp only [offer, request, List.mem_append, List.mem_singleton] at hit
  rcases hit with rfl | rfl <;>
    simp [ConceptOrder.satItem, ConceptOrder.satAtom, Atom.mode, Atom.denot,
      ConceptOrder.elems, ConceptOrder.eqv, collapsed]

theorem discrete_not_admits : ¬ discrete.admits N (offer ++ request) := by
  intro h
  have := admits_imp_eqv discrete h
  simp [ConceptOrder.eqv, discrete] at this

/-- No published statement. -/
theorem language_not_compatible : ¬ Compatible [] N offer request := by
  intro h
  exact discrete_not_admits (h discrete (by simp [Mod]))

theorem language_not_incompatible : ¬ Incompatible [] N offer request := by
  intro h
  exact h collapsed (by simp [Mod]) collapsed_admits

theorem language_unknown : verdict [] N offer request = Verdict.unknown := by
  unfold verdict
  simp [language_not_compatible, language_not_incompatible]

/-- The parties' declaration `de ≠ fr`. -/
def decl : List (Statement L) := [Statement.distinct de fr]

theorem language_declared_incompatible : Incompatible decl N offer request := by
  intro M hM him
  have hd : ¬ M.eqv de fr := hM (Statement.distinct de fr) (by simp [decl])
  exact hd (admits_imp_eqv M him)

theorem language_declared_not_compatible : ¬ Compatible decl N offer request := by
  intro h
  have hmod : Mod decl discrete := by
    intro a ha
    simp [decl] at ha
    subst ha
    simp [ConceptOrder.sat, ConceptOrder.eqv, discrete]
  exact discrete_not_admits (h discrete hmod)

theorem language_declared_verdict :
    verdict decl N offer request = Verdict.incompatible := by
  unfold verdict
  simp [language_declared_not_compatible, language_declared_incompatible]

end OdrlGrounded.Example
