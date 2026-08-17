; -------------------------------------------------------------------------
; File     : KGC312-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isA dpv:NCP against eq dpv:SR (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC312-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_research_and_development () Concept)
(declare-fun dpv_purpose () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three axioms as KGE000-0.ax, so the
; two encodings are the same theory.  Requires UF, not QF_UF.
(assert (forall ((x Concept)) (kge_leq x x)))
(assert (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))))
(assert (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))))
; Resource: what DPV publishes about these concepts.  Note that it relates
; scientific research to research and development, and not to the offered
; purpose in either direction.
(assert (kge_leq dpv_scientific_research dpv_research_and_development))
(assert (kge_leq dpv_research_and_development dpv_purpose))
(assert (kge_leq dpv_non_commercial_purpose dpv_purpose))
; witness condition asserted
(assert (or (and (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose) (= dpv_non_commercial_purpose dpv_scientific_research))
    (and (kge_leq dpv_scientific_research  dpv_non_commercial_purpose) (= dpv_scientific_research  dpv_scientific_research))))
(check-sat)
(exit)
