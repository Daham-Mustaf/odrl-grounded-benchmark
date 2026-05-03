; --------------------------------------------------------------------------
; File     : KGC803-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 1: Compatible preservation under concept addition [GeoNames]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC803-1.smt2
; Status   : sat
; Verdict  : MonotonicityCompatible
; Comments : Verdict: MonotonicityCompatible  Category: Monotonicity  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
; KGC803 SMT cross-check: Compatible preservation under concept addition.
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
; Concrete constants for KGC803
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
; R' extension: spain is R'-only, with leq_R_prime(spain, europe)
; ============================================================
(assert (in_concepts_R_prime gn_spain))
(assert (not (in_concepts_R gn_spain)))
(assert (leq_R_prime gn_spain gn_europe))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_spain))

; ============================================================
; Compatible verification: gn_france is in both denotations
; under R'. [c_ispartof(europe)]_R' contains gn_france because
; leq_R_prime(france, europe) (lifted from R via closure).
; [c_eq(france)]_R' is the singleton {gn_france}.
;
; The SMT side checks consistency: the model must exist where
; france is the witness. Expected: sat.
;
; No contradiction is asserted; the resource is consistent and a
; satisfying model exists.
(check-sat)
(exit)
