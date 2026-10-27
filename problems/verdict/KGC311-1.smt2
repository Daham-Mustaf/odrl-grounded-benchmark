; -------------------------------------------------------------------------
; File     : KGC311-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isA dpv:Purpose against eq dpv:NCR (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC311-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_purpose () Concept)
(declare-fun dpv_non_commercial_research () Concept)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_research_and_development () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq dpv_non_commercial_purpose dpv_purpose) :named res_dpv_non_commercial_purpose_below_dpv_purpose))
(assert (! (kge_leq dpv_non_commercial_research dpv_non_commercial_purpose) :named res_dpv_non_commercial_research_below_dpv_non_commercial_purpose))
(assert (! (kge_leq dpv_non_commercial_research dpv_research_and_development) :named res_dpv_non_commercial_research_below_dpv_research_and_development))
(assert (! (kge_leq dpv_research_and_development dpv_purpose) :named res_dpv_research_and_development_below_dpv_purpose))
; witness condition asserted
(assert (! (or (and (kge_leq dpv_purpose dpv_purpose) (= dpv_purpose dpv_non_commercial_research)) (and (kge_leq dpv_non_commercial_research dpv_purpose) (= dpv_non_commercial_research dpv_non_commercial_research))) :named w_kgc311))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
