; --------------------------------------------------------------------------
; File     : KGC420-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : isPartOf / Conflict: isPartOf bcp:de x eq bcp:fr
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC420-1.smt2
; Status   : unsat
; Verdict  : Conflict
; Comments : Verdict: Conflict  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000: reflexivity, disjointness symmetry/irreflexivity, propagation.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
; Negation of Conflict: witness x in both denotations.
; [[c_offer]]   = downward cone of bcp_de (isPartOf)
; [[c_request]] = {bcp_fr}
(declare-fun x () Concept)
(assert (kge_leq x bcp_de))
(assert (= x bcp_fr))
(check-sat)
(exit)
