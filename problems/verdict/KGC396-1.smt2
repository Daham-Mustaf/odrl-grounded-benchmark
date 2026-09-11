; -------------------------------------------------------------------------
; File     : KGC396-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isAnyOf {RnD, Marketing} against isAllOf {RnD, ServiceProvision} (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC396-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_research_and_development () Concept)
(declare-fun dpv_marketing () Concept)
(declare-fun dpv_service_provision () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; witness condition asserted
(assert (! (and true true (or (and true (or (= dpv_research_and_development dpv_research_and_development) (= dpv_research_and_development dpv_marketing))) (and true (or (= dpv_marketing dpv_research_and_development) (= dpv_marketing dpv_marketing))) (and true (or (= dpv_service_provision dpv_research_and_development) (= dpv_service_provision dpv_marketing))))) :named w_kgc396))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
