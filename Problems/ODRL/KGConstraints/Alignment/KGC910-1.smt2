; --------------------------------------------------------------------------
; File     : KGC910-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 2 second case: below-preservation closure on dom(α) [Munich forced]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC910-1.smt2
; Status   : unsat
; Verdict  : AlignmentLostBoundary
; Comments : Verdict: AlignmentLostBoundary  Category: Alignment  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC910 SMT cross-check: below-preservation forces gn_munich into dom(α).
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
; Concrete constants for KGC910
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_munich  () Concept)
(declare-fun iso_de     () Concept)
(declare-fun iso_de_by  () Concept)
; ============================================================
; R_A facts (GeoNames with city level)
; ============================================================
(assert (in_concepts_A gn_germany))
(assert (in_concepts_A gn_bayern))
(assert (in_concepts_A gn_munich))
(assert (leq_A gn_bayern gn_germany))
(assert (leq_A gn_munich gn_bayern))
; ============================================================
; R_B facts (ISO 3166 — no city codes)
; ============================================================
(assert (in_concepts_B iso_de))
(assert (in_concepts_B iso_de_by))
(assert (leq_B iso_de_by iso_de))
; ============================================================
; Alignment α (Munich not explicitly aligned)
; ============================================================
(assert (align gn_germany iso_de))
(assert (align gn_bayern iso_de_by))
; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_bayern gn_munich iso_de iso_de_by))
; ============================================================
; Boundary check: assume align_dom(gn_munich) is FALSE.
; align_downward_domain forces a contradiction because gn_bayern
; is aligned and gn_munich is below gn_bayern. Expected: unsat.
; ============================================================
(assert (not (align_dom gn_munich)))
(check-sat)
(exit)
