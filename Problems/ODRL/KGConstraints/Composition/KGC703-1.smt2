; --------------------------------------------------------------------------
; File     : KGC703-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 5 (and): disjoint operand sets [GeoNames | BCP47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC703-1.smt2
; Status   : sat
; Verdict  : AndCompatibleNonConflict
; Comments : Verdict: AndCompatibleNonConflict  Category: Composition  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun bcp_de    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; Identity.
(assert (distinct gn_europe bcp_de))
;
; Disjoint operand sets: spatial and language are unrelated.
; No shared operand to compare; rule-level Conflict cannot derive.
; Z3 returns sat (consistent model exists with no conflict).
(check-sat)
(exit)
