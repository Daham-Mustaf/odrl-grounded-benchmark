; --------------------------------------------------------------------------
; File     : KGC705-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 2 (and): three-operand all-Compatible [GeoNames+DPV+BCP47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC705-1.smt2
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
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
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
; BCP47: distinct tags.
(assert (distinct gn_europe gn_france
                  dpv_scientific_research dpv_purpose
                  bcp_de bcp_fr))
;
; Each operand-pair admits a witness:
;   spatial:  gn_france in [c1_off] (kge_leq France Europe) and [c1_req].
;   purpose:  dpv_scientific_research in [c2_off] (eq) and [c2_req] (kge_leq SR Purpose).
;   language: bcp_de in [c3_off] and [c3_req] (eq de in {de, fr}).
; No Conflict can be derived. Z3 returns sat.
(check-sat)
(exit)
