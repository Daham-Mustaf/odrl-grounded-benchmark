; --------------------------------------------------------------------------
; File     : KGC421-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : isPartOf / Compatible: isPartOf gn:Europe x eq gn:France
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC421-1.smt2
; Status   : sat
; Verdict  : Compatible
; Comments : Verdict: Compatible  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
(assert (kge_leq gn_france gn_europe))
(declare-fun x () Concept)
(assert (= x gn_france))
(assert (kge_leq x gn_europe))
(check-sat)
(exit)
