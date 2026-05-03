; --------------------------------------------------------------------------
; File     : KGC300-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : language: eq bcp:de x eq bcp:fr -> Conflict
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC300-1.smt2
; Status   : unsat
; Verdict  : Conflict
; Comments : Verdict: Conflict  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
; Registry uniqueness: bcp_de and bcp_fr are distinct (kge_disjoint).
(assert (distinct bcp_de bcp_fr))
; Conflict claim: there is no concept X in both denotations.
; [[c_offer]]   = {bcp_de},  [[c_request]] = {bcp_fr}
; Negation: there exists X with X = bcp_de AND X = bcp_fr.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))
(check-sat)
(exit)
