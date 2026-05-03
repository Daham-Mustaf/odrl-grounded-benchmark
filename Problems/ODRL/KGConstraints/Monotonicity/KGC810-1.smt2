; --------------------------------------------------------------------------
; File     : KGC810-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: complement counterexample [Remark 2 — neq]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC810-1.smt2
; Status   : sat
; Verdict  : MonotonicityComplementBoundary
; Comments : Verdict: MonotonicityComplementBoundary  Category: Monotonicity  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC810 SMT cross-check: complement boundary counterexample.
; ============================================================
; Single-sort `Concept`. Membership in R and R' tracked by
; in_concepts_R/1 and in_concepts_R_prime/1.
; ============================================================
(declare-sort Concept 0)
(declare-fun in_concepts_R       (Concept) Bool)
(declare-fun in_concepts_R_prime (Concept) Bool)
(declare-fun leq_R               (Concept Concept) Bool)
(declare-fun leq_R_prime         (Concept Concept) Bool)
(declare-fun disjoint_R          (Concept Concept) Bool)
(declare-fun disjoint_R_prime    (Concept Concept) Bool)

; ============================================================
; KGE000 axioms (R and R')
; ============================================================
(assert (forall ((c Concept)) (leq_R c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_R a b) (leq_R b c)) (leq_R a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_R a b) (disjoint_R b a))))
(assert (forall ((c Concept)) (not (disjoint_R c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_R a b) (leq_R z a) (leq_R z b))
        false)))

(assert (forall ((c Concept)) (leq_R_prime c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_R_prime a b) (leq_R_prime b c)) (leq_R_prime a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_R_prime a b) (disjoint_R_prime b a))))
(assert (forall ((c Concept)) (not (disjoint_R_prime c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_R_prime a b) (leq_R_prime z a) (leq_R_prime z b))
        false)))

; ============================================================
; MONO000 closure axioms: R-facts propagate to R'
; ============================================================
(assert (forall ((c Concept))
    (=> (in_concepts_R c) (in_concepts_R_prime c))))
(assert (forall ((a Concept) (b Concept))
    (=> (leq_R a b) (leq_R_prime a b))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_R a b) (disjoint_R_prime a b))))

(declare-fun grounded_as_R       (Concept Concept) Bool)
(declare-fun grounded_as_R_prime (Concept Concept) Bool)

; Closure for grounding (MONO000 axiom in SMT form).
(assert (forall ((c Concept) (g Concept))
    (=> (grounded_as_R c g) (grounded_as_R_prime c g))))

; ============================================================
; Concrete constants for KGC810
; ============================================================
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_es () Concept)
; ============================================================
; R-facts: closed-world {bcp_de, bcp_fr}.
; ============================================================
(assert (in_concepts_R bcp_de))
(assert (in_concepts_R bcp_fr))
(assert (grounded_as_R bcp_de bcp_de))
(assert (grounded_as_R bcp_fr bcp_fr))
(assert (forall ((x Concept))
    (=> (in_concepts_R x) (or (= x bcp_de) (= x bcp_fr)))))

; ============================================================
; R' extension: add bcp_es with grounding.
; ============================================================
(assert (in_concepts_R_prime bcp_es))
(assert (not (in_concepts_R bcp_es)))
(assert (grounded_as_R_prime bcp_es bcp_es))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct bcp_de bcp_fr bcp_es))

; ============================================================
; Witness: bcp_es is in [c_neq(de)]_R' \cap [c_neq(fr)]_R'.
; bcp_es is in_concepts_R_prime, != bcp_de, != bcp_fr.
; The resource is consistent with this witness existing.
; Expected: sat.
(check-sat)
(exit)
