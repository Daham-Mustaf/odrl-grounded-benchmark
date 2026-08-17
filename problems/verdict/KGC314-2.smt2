; -------------------------------------------------------------------------
; File     : KGC314-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, eq dpv:Marketing against eq dpv:SR, under a declared distinctness (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC314-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_marketing () Concept)
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
; Resource: unchanged from KGC313.
(assert (kge_leq dpv_marketing dpv_purpose))
(assert (kge_leq dpv_scientific_research dpv_research_and_development))
(assert (kge_leq dpv_research_and_development dpv_purpose))
; Background theory: the declaration, and the only difference from KGC313.
(assert (distinct dpv_marketing dpv_scientific_research))
; witness condition negated
(assert (not (or (and (= dpv_marketing dpv_marketing) (= dpv_marketing dpv_scientific_research))
    (and (= dpv_scientific_research dpv_marketing) (= dpv_scientific_research dpv_scientific_research)))))
(check-sat)
(exit)
