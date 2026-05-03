; --------------------------------------------------------------------------
; File     : KGC402-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : eq / Unknown: dpv:ScientificResearch x dpv:CommercialResearch
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC402-1.smt2
; Status   : sat
; Verdict  : Unknown
; Comments : Verdict: Unknown  Category: Conflict  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_scientific_research      () Concept)
(declare-fun dpv_commercial_research      () Concept)
(declare-fun dpv_research_and_development () Concept)
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
; DPV asserts both concepts share the parent ResearchAndDevelopment,
; but NEITHER ScientificResearch <= CommercialResearch NOR disjointness.
(assert (kge_leq dpv_scientific_research dpv_research_and_development))
(assert (kge_leq dpv_commercial_research dpv_research_and_development))
; Identity (the three concepts are distinct as IRIs).
(assert (distinct dpv_scientific_research
                  dpv_commercial_research
                  dpv_research_and_development))
(check-sat)
(exit)
