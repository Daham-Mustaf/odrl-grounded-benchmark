; --------------------------------------------------------------------------
; File     : KGC806-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: denotation growth under concept addition [GeoNames]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC806-1.smt2
; Status   : unsat
; Verdict  : MonotonicityDenotation
; Comments : Verdict: MonotonicityDenotation  Category: Monotonicity  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC806 SMT cross-check: denotation growth under concept addition.
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

; ============================================================
; Concrete constants for KGC806
; ============================================================
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun gn_spain  () Concept)
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_france))
(assert (leq_R gn_france gn_europe))

; ============================================================
; R' extension: spain R'-only with new edge to europe
; ============================================================
(assert (in_concepts_R_prime gn_spain))
(assert (not (in_concepts_R gn_spain)))
(assert (leq_R_prime gn_spain gn_europe))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_spain))

; ============================================================
; Witness search: hypothetical x that is in [c_ispartof(europe)]_R
; but NOT in [c_ispartof(europe)]_R'.
; In SMT terms: leq_R(x, europe) AND NOT leq_R_prime(x, europe).
; The closure axiom extension_leq forces this contradiction.
; Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (leq_R x gn_europe))
(assert (not (leq_R_prime x gn_europe)))
(check-sat)
(exit)
