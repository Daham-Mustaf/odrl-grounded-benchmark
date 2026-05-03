; --------------------------------------------------------------------------
; File     : KGC713-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : xone conservative reduction: xone-Conflict via or-Conflict [BCP47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC713-1.smt2
; Status   : unsat
; Verdict  : XoneConflict
; Comments : Verdict: XoneConflict  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_es () Concept)
(declare-fun bcp_it () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47 registry uniqueness.
(assert (kge_disjoint bcp_de bcp_it))
(assert (kge_disjoint bcp_fr bcp_it))
(assert (kge_disjoint bcp_es bcp_it))
(assert (distinct bcp_de bcp_fr bcp_es bcp_it))
;
; SMT cross-check: a request satisfying r1's xone (any one of the three
; disjuncts) AND r2 (= bcp_it) must equal one of {de, fr, es} AND it.
; All three cases conflict with it; unsat.
(declare-fun req_lang () Concept)
(assert (or (= req_lang bcp_de)
            (= req_lang bcp_fr)
            (= req_lang bcp_es)))
(assert (= req_lang bcp_it))
(check-sat)
(exit)
