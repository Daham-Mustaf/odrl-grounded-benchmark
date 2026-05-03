; --------------------------------------------------------------------------
; File     : KGC807-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: denotation growth under edge addition [GeoNames]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC807-1.smt2
; Status   : unsat
; Verdict  : MonotonicityDenotation
; Comments : Verdict: MonotonicityDenotation  Category: Monotonicity  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC807 SMT cross-check: denotation growth under edge addition.
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
; Concrete constants for KGC807
; ============================================================
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun gn_germany () Concept)
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_france))
(assert (in_concepts_R gn_germany))
(assert (leq_R gn_france gn_europe))

; ============================================================
; R' extension: new edge germany leq_R' europe (germany was
; already in R; the edge is the new fact).
; ============================================================
(assert (leq_R_prime gn_germany gn_europe))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_germany))

; ============================================================
; Witness search: hypothetical x in [c]_R but not in [c]_R'.
; In SMT terms: leq_R(x, europe) AND NOT leq_R_prime(x, europe).
; Closure axiom extension_leq forces contradiction.
; Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (leq_R x gn_europe))
(assert (not (leq_R_prime x gn_europe)))
(check-sat)
(exit)
