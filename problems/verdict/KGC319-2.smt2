; -------------------------------------------------------------------------
; File     : KGC319-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, xone(isA RnD, isA Marketing) against eq ScientificResearch (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC319-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_research_and_development () Concept)
(declare-fun dpv_marketing () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq dpv_scientific_research dpv_research_and_development) :named res_dpv_scientific_research_below_dpv_research_and_development))
; witness condition negated
(assert (! (not (or (and (or (and (kge_leq dpv_research_and_development dpv_research_and_development) (= dpv_research_and_development dpv_scientific_research)) (and (kge_leq dpv_marketing dpv_research_and_development) (= dpv_marketing dpv_scientific_research)) (and (kge_leq dpv_scientific_research dpv_research_and_development) (= dpv_scientific_research dpv_scientific_research))) (or (and (and (kge_leq dpv_research_and_development dpv_research_and_development) (= dpv_research_and_development dpv_scientific_research)) (not (kge_leq dpv_research_and_development dpv_marketing))) (and (and (kge_leq dpv_marketing dpv_research_and_development) (= dpv_marketing dpv_scientific_research)) (not (kge_leq dpv_marketing dpv_marketing))) (and (and (kge_leq dpv_scientific_research dpv_research_and_development) (= dpv_scientific_research dpv_scientific_research)) (not (kge_leq dpv_scientific_research dpv_marketing))))) (and (or (and (kge_leq dpv_research_and_development dpv_marketing) (= dpv_research_and_development dpv_scientific_research)) (and (kge_leq dpv_marketing dpv_marketing) (= dpv_marketing dpv_scientific_research)) (and (kge_leq dpv_scientific_research dpv_marketing) (= dpv_scientific_research dpv_scientific_research))) (or (and (and (kge_leq dpv_research_and_development dpv_marketing) (= dpv_research_and_development dpv_scientific_research)) (not (kge_leq dpv_research_and_development dpv_research_and_development))) (and (and (kge_leq dpv_marketing dpv_marketing) (= dpv_marketing dpv_scientific_research)) (not (kge_leq dpv_marketing dpv_research_and_development))) (and (and (kge_leq dpv_scientific_research dpv_marketing) (= dpv_scientific_research dpv_scientific_research)) (not (kge_leq dpv_scientific_research dpv_research_and_development))))))) :named w_kgc319))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
