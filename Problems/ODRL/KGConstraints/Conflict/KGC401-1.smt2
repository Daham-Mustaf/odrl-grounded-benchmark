; --------------------------------------------------------------------------
; File     : KGC401-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : eq / Compatible: bcp:de x bcp:de
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC401-1.smt2
; Status   : sat
; Verdict  : Compatible
; Comments : Verdict: Compatible  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun x () Concept)
(assert (= x bcp_de))
(check-sat)
(exit)
