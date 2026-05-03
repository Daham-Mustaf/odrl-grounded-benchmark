; --------------------------------------------------------------------------
; File     : KGC802-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: Conflict preservation under disjointness addition [GeoNames+SDA]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC802-1.smt2
; Status   : unsat
; Verdict  : MonotonicityConflict
; Comments : Verdict: MonotonicityConflict  Category: Monotonicity  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC802 SMT cross-check: Conflict preservation under disjointness addition.
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
; Concrete constants for KGC802
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_italy   () Concept)
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_germany))
(assert (in_concepts_R gn_france))
(assert (in_concepts_R gn_bayern))
(assert (leq_R gn_bayern gn_germany))
(assert (disjoint_R gn_germany gn_france))

; ============================================================
; R' extension: italy with new disjointness fact, unrelated to
; the original Conflict pair (germany, france).
; ============================================================
(assert (in_concepts_R_prime gn_italy))
(assert (not (in_concepts_R gn_italy)))
(assert (disjoint_R_prime gn_italy gn_france))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_france gn_bayern gn_italy))

; ============================================================
; Witness search: hypothetical x in [c1]_R' \cap [c2]_R'
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_R_prime x))
(assert (leq_R_prime x gn_germany))
(assert (leq_R_prime x gn_france))

; Expected: unsat. The new disjoint_R_prime(italy, france) is
; irrelevant; the original disjointness lifts via closure and
; refutes the witness through propagation.
(check-sat)
(exit)
