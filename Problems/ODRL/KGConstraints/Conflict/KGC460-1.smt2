; --------------------------------------------------------------------------
; File     : KGC460-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : isNoneOf / Conflict: isNoneOf {bcp:de, bcp:fr} x eq bcp:de
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC460-1.smt2
; Status   : unsat
; Verdict  : Conflict
; Comments : Verdict: Conflict  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(assert (distinct bcp_de bcp_fr))
; Negation of Conflict: witness x in both denotations.
; [[c_offer]]   = C \ {bcp_de, bcp_fr}, so x must NOT be in the list
; [[c_request]] = {bcp_de}, so x = bcp_de
; bcp_de is on the excluded list; constraints unsatisfiable.
(declare-fun x () Concept)
(assert (and (distinct x bcp_de) (distinct x bcp_fr)))
(assert (= x bcp_de))
(check-sat)
(exit)
