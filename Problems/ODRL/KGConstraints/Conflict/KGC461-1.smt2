; --------------------------------------------------------------------------
; File     : KGC461-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : isNoneOf / Compatible: isNoneOf {bcp:de, bcp:fr} x eq bcp:it
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC461-1.smt2
; Status   : sat
; Verdict  : Compatible
; Comments : Verdict: Compatible  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_it () Concept)
(assert (distinct bcp_de bcp_fr bcp_it))
(declare-fun x () Concept)
(assert (and (distinct x bcp_de) (distinct x bcp_fr)))
(assert (= x bcp_it))
(check-sat)
(exit)
