; --------------------------------------------------------------------------
; File     : KGC801-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: Conflict preservation under edge addition [synthetic DPV-shaped]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC801-1.smt2
; Status   : unsat
; Verdict  : MonotonicityConflict
; Comments : Verdict: MonotonicityConflict  Category: Monotonicity  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC801 SMT cross-check: Conflict preservation under edge addition.
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
; Concrete constants for KGC801
; ============================================================
(declare-fun dpv_sr () Concept)
(declare-fun dpv_cr () Concept)
(declare-fun dpv_rd () Concept)
(declare-fun dpv_ar () Concept)
; ============================================================
; R-facts: synthetic DPV-shaped resource.
; ============================================================
(assert (in_concepts_R dpv_sr))
(assert (in_concepts_R dpv_cr))
(assert (in_concepts_R dpv_rd))
(assert (leq_R dpv_sr dpv_rd))
(assert (leq_R dpv_cr dpv_rd))
; Synthetic disjointness (not in real DPV)
(assert (disjoint_R dpv_sr dpv_cr))

; ============================================================
; R' extension: dpv_ar is R'-only, with new edge dpv_sr leq_R' dpv_ar
; ============================================================
(assert (in_concepts_R_prime dpv_ar))
(assert (not (in_concepts_R dpv_ar)))
(assert (leq_R_prime dpv_sr dpv_ar))
(assert (leq_R_prime dpv_ar dpv_rd))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct dpv_sr dpv_cr dpv_rd dpv_ar))

; ============================================================
; Witness search: hypothetical x in [c1]_R' \cap [c2]_R'
; c1 = c_ispartof(dpv_sr), c2 = c_ispartof(dpv_cr)
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_R_prime x))
(assert (leq_R_prime x dpv_sr))
(assert (leq_R_prime x dpv_cr))

; Expected: unsat. Closure lifts disjoint_R(sr, cr) to
; disjoint_R_prime(sr, cr); propagation refutes the witness.
; The new edge leq_R_prime(sr, ar) is irrelevant — it doesn't
; create any common subordinate of sr and cr.
(check-sat)
(exit)
