; --------------------------------------------------------------------------
; File     : KGC900-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 2: Conflict transport in aligned subdomain [GeoNames ↔ ISO 3166, ADM1]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC900-1.smt2
; Status   : unsat
; Verdict  : AlignmentConflict
; Comments : Verdict: AlignmentConflict  Category: Alignment  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC900 SMT cross-check: alignment preserves Conflict at ADM1 level.
; ============================================================
; Single-sort `Concept`. R_A and R_B membership tracked by
; in_concepts_A/1 and in_concepts_B/1. Alignment relation
; align/2 connects R_A to R_B.
; ============================================================
(declare-sort Concept 0)
(declare-fun in_concepts_A (Concept) Bool)
(declare-fun in_concepts_B (Concept) Bool)
(declare-fun leq_A         (Concept Concept) Bool)
(declare-fun leq_B         (Concept Concept) Bool)
(declare-fun disjoint_A    (Concept Concept) Bool)
(declare-fun disjoint_B    (Concept Concept) Bool)
(declare-fun grounded_as_A (Concept Concept) Bool)
(declare-fun grounded_as_B (Concept Concept) Bool)
(declare-fun align         (Concept Concept) Bool)
(declare-fun align_dom     (Concept) Bool)
; ============================================================
; KGE axioms for R_A and R_B (transitivity, symmetry, propagation)
; ============================================================
(assert (forall ((c Concept)) (leq_A c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_A a b) (leq_A b c)) (leq_A a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_A a b) (disjoint_A b a))))
(assert (forall ((c Concept)) (not (disjoint_A c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_A a b) (leq_A z a) (leq_A z b)) false)))
(assert (forall ((c Concept)) (leq_B c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_B a b) (leq_B b c)) (leq_B a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_B a b) (disjoint_B b a))))
(assert (forall ((c Concept)) (not (disjoint_B c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_B a b) (leq_B z a) (leq_B z b)) false)))
; ============================================================
; Alignment preservation axioms (subset of ALIGN000 for SMT)
; ============================================================
; Functional
(assert (forall ((c Concept) (d1 Concept) (d2 Concept))
    (=> (and (align c d1) (align c d2)) (= d1 d2))))
; One-to-one (injective)
(assert (forall ((c1 Concept) (c2 Concept) (d Concept))
    (=> (and (align c1 d) (align c2 d)) (= c1 c2))))
; Domain intro (one-way)
(assert (forall ((x Concept) (y Concept))
    (=> (align x y) (align_dom x))))
; Order preservation (biconditional)
(assert (forall ((x Concept) (y Concept) (nux Concept) (nuy Concept))
    (=> (and (align x nux) (align y nuy))
        (= (leq_A x y) (leq_B nux nuy)))))
; Disjointness preservation (one-way)
(assert (forall ((x Concept) (y Concept) (nux Concept) (nuy Concept))
    (=> (and (align x nux) (align y nuy) (disjoint_A x y))
        (disjoint_B nux nuy))))
; Grounding preservation (one-way)
(assert (forall ((c Concept) (nuc Concept) (v Concept))
    (=> (and (align c nuc) (grounded_as_A v c))
        (grounded_as_B v nuc))))
; Below preservation: domain closure
(assert (forall ((g Concept) (ga Concept) (xa Concept))
    (=> (and (align g ga) (leq_A xa g)) (align_dom xa))))
; Below preservation: witness existence
(assert (forall ((g Concept) (ga Concept) (yb Concept))
    (=> (and (align g ga) (leq_B yb ga))
        (exists ((xa Concept)) (and (align xa yb) (leq_A xa g))))))
; Above preservation: domain closure
(assert (forall ((g Concept) (ga Concept) (xa Concept))
    (=> (and (align g ga) (leq_A g xa)) (align_dom xa))))
; Above preservation: witness existence
(assert (forall ((g Concept) (ga Concept) (yb Concept))
    (=> (and (align g ga) (leq_B ga yb))
        (exists ((xa Concept)) (and (align xa yb) (leq_A g xa))))))
; ============================================================
; Concrete constants for KGC900
; ============================================================
(declare-fun gn_germany       () Concept)
(declare-fun gn_france        () Concept)
(declare-fun gn_bayern        () Concept)
(declare-fun gn_ile_de_france () Concept)
(declare-fun iso_de           () Concept)
(declare-fun iso_fr           () Concept)
(declare-fun iso_de_by        () Concept)
(declare-fun iso_fr_idf       () Concept)
; ============================================================
; R_A facts
; ============================================================
(assert (in_concepts_A gn_germany))
(assert (in_concepts_A gn_france))
(assert (in_concepts_A gn_bayern))
(assert (in_concepts_A gn_ile_de_france))
(assert (leq_A gn_bayern gn_germany))
(assert (leq_A gn_ile_de_france gn_france))
(assert (disjoint_A gn_germany gn_france))
; ============================================================
; R_B facts (independent ISO 3166-2 hierarchy)
; ============================================================
(assert (in_concepts_B iso_de))
(assert (in_concepts_B iso_fr))
(assert (in_concepts_B iso_de_by))
(assert (in_concepts_B iso_fr_idf))
(assert (leq_B iso_de_by iso_de))
(assert (leq_B iso_fr_idf iso_fr))
; ============================================================
; Alignment α
; ============================================================
(assert (align gn_germany iso_de))
(assert (align gn_france iso_fr))
(assert (align gn_bayern iso_de_by))
(assert (align gn_ile_de_france iso_fr_idf))
; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_france gn_bayern gn_ile_de_france
                  iso_de iso_fr iso_de_by iso_fr_idf))
; ============================================================
; Witness search: hypothetical x in [c_ispartof(iso_de_by)]_B ∩
; [c_ispartof(iso_fr_idf)]_B. The witness would need to satisfy
; leq_B(x, iso_de_by) and leq_B(x, iso_fr_idf), then via
; transitivity leq_B(x, iso_de) and leq_B(x, iso_fr).
; Alignment-derived disjoint_B(iso_de, iso_fr) plus R_B propagation
; refute. Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_B x))
(assert (leq_B x iso_de_by))
(assert (leq_B x iso_fr_idf))
(check-sat)
(exit)
