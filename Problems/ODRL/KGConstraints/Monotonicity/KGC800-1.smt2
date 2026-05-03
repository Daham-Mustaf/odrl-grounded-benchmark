; --------------------------------------------------------------------------
; File     : KGC800-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: Conflict preservation under concept addition [GeoNames-like]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC800-1.smt2
; Status   : unsat
; Verdict  : MonotonicityConflict
; Comments : Verdict: MonotonicityConflict  Category: Monotonicity  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC800 SMT cross-check: Conflict preservation under concept addition.
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
; Concrete constants for KGC800
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
(declare-fun gn_spain   () Concept)
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_germany))
(assert (in_concepts_R gn_france))
(assert (disjoint_R gn_germany gn_france))

; ============================================================
; R' extension: gn_spain is R'-only
; ============================================================
(assert (in_concepts_R_prime gn_spain))
(assert (not (in_concepts_R gn_spain)))
(assert (disjoint_R_prime gn_spain gn_germany))
(assert (disjoint_R_prime gn_spain gn_france))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_france gn_spain))

; ============================================================
; Witness search: hypothetical x in [c1]_R' \cap [c2]_R'
; c1 = c_ispartof(gn_germany), denotation = {x : leq_R_prime(x, gn_germany)}
; c2 = c_ispartof(gn_france),  denotation = {x : leq_R_prime(x, gn_france)}
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_R_prime x))
(assert (leq_R_prime x gn_germany))
(assert (leq_R_prime x gn_france))

; Expected: unsat. The closure axiom lifts disjoint_R(germany, france)
; to disjoint_R_prime(germany, france); the propagation axiom then
; refutes the witness.
(check-sat)
(exit)
