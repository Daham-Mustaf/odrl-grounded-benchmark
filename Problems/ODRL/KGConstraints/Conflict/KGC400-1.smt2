; --------------------------------------------------------------------------
; File     : KGC400-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : eq / Conflict: bcp:de x bcp:fr
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC400-1.smt2
; Status   : unsat
; Verdict  : Conflict
; Comments : Verdict: Conflict  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000: disjointness symmetry/irreflexivity.
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
; Negation of Conflict: witness x in both eq denotations.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))
(check-sat)
(exit)
