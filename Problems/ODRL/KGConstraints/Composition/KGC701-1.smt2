; --------------------------------------------------------------------------
; File     : KGC701-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 2 (and): Compatible does NOT yield Conflict [GeoNames, DPV]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC701-1.smt2
; Status   : sat
; Verdict  : AndCompatibleNonConflict
; Comments : Verdict: AndCompatibleNonConflict  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_purpose             () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; GeoNames: France below Europe.
(assert (kge_leq gn_france gn_europe))
; DPV: SR below Purpose.
(assert (kge_leq dpv_scientific_research dpv_purpose))
; Identity.
(assert (distinct gn_europe gn_france
                  dpv_scientific_research dpv_purpose))
;
; Both operand-pairs admit common satisfiers:
; gn_france in both [c1_off] and [c1_req];
; dpv_scientific_research in both [c2_off] and [c2_req].
; No Conflict can be derived. Z3 returns sat (consistent model exists).
(check-sat)
(exit)
