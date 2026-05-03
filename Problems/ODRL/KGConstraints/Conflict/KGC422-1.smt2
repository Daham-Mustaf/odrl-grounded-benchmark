; --------------------------------------------------------------------------
; File     : KGC422-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : isPartOf / Unknown: isPartOf gn:Germany x eq gn:Strasbourg
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC422-1.smt2
; Status   : sat
; Verdict  : Unknown
; Comments : Verdict: Unknown  Category: Conflict  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_germany    () Concept)
(declare-fun gn_strasbourg () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; GeoNames silent on (Strasbourg, Germany): no parentFeature, no disjointness.
(assert (distinct gn_germany gn_strasbourg))
(check-sat)
(exit)
