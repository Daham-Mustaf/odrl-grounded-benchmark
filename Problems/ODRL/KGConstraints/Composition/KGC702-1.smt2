; --------------------------------------------------------------------------
; File     : KGC702-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 2 (and): Strong Kleene Unknown propagation [GeoNames, DPV]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC702-1.smt2
; Status   : sat
; Verdict  : AndUnknown
; Comments : Verdict: AndUnknown  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_marketing           () Concept)
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
; DPV: no edge or disjointness between SR and Marketing.
(assert (distinct gn_europe gn_france
                  dpv_scientific_research dpv_marketing))
;
; Theorem 2's rule_and = unknown derivation lives in FOL via COMPOSE000.
; SMT side confirms resource consistency.
(check-sat)
(exit)
