; --------------------------------------------------------------------------
; File     : KGC301-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : purpose: isA dpv:NonCommercialPurpose x eq dpv:ScientificResearch -> Unknown
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC301-1.smt2
; Status   : sat
; Verdict  : Unknown
; Comments : Verdict: Unknown  Category: Conflict  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
; Reflexivity of leq.
(assert (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose))
(assert (kge_leq dpv_scientific_research    dpv_scientific_research))
; DPV is silent on the relation between SR and NCP.
; Open-world: do NOT assert (not (kge_leq ...)) or (not (kge_disjoint ...)).
; Solver freely chooses; sat means the silence is consistent.
(check-sat)
(check-sat)
(exit)
