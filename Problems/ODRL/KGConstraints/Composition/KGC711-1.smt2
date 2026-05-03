; --------------------------------------------------------------------------
; File     : KGC711-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 2 (or): one cross-pair Compatible [BCP47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC711-1.smt2
; Status   : sat
; Verdict  : OrCompatible
; Comments : Verdict: OrCompatible  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
;
; Witness: req_lang = bcp_de satisfies both d1 (in or for r1) and
; d1p (= bcp_de for r2). rule_or = compatible. Z3 returns sat.
(declare-fun req_lang () Concept)
(assert (or (= req_lang bcp_de) (= req_lang bcp_fr)))
(assert (= req_lang bcp_de))
(check-sat)
(exit)
