; --------------------------------------------------------------------------
; File     : KGC812-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: Assumption 1 violation [boundary — inconsistent extension]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC812-1.smt2
; Status   : unsat
; Verdict  : MonotonicityAssumption1Boundary
; Comments : Verdict: MonotonicityAssumption1Boundary  Category: Monotonicity  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
; KGC812 SMT cross-check: Assumption 1 violation.
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
; Concrete constants for KGC812
; ============================================================
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_z  () Concept)
; ============================================================
; R-facts: two disjoint concepts.
; ============================================================
(assert (in_concepts_R bcp_de))
(assert (in_concepts_R bcp_fr))
(assert (disjoint_R bcp_de bcp_fr))

; ============================================================
; R' extension: ASSUMPTION 1 VIOLATION
; bcp_z is a common subordinate of two disjoint concepts.
; ============================================================
(assert (in_concepts_R_prime bcp_z))
(assert (not (in_concepts_R bcp_z)))
(assert (leq_R_prime bcp_z bcp_de))
(assert (leq_R_prime bcp_z bcp_fr))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct bcp_de bcp_fr bcp_z))

; Closure axiom + propagation axiom in R' force unsat.
; Expected: unsat.
(check-sat)
(exit)
