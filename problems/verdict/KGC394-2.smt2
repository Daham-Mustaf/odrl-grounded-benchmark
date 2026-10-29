; -------------------------------------------------------------------------
; File     : KGC394-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isAnyOf {PublicBenefit, NonCommercialResearch} against eq ImproveTransportMobility, declared distinct (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC394-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_public_benefit () Concept)
(declare-fun dpv_non_commercial_research () Concept)
(declare-fun dpv_improve_transport_mobility () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq dpv_improve_transport_mobility dpv_public_benefit) :named res_dpv_improve_transport_mobility_below_dpv_public_benefit))
; Declared distinctness this problem adopts, named as the TPTP
; side names it.
(assert (! (not (= dpv_improve_transport_mobility dpv_public_benefit)) :named bg_dist_dpv_improve_transport_mobility_dpv_public_benefit))
(assert (! (not (= dpv_improve_transport_mobility dpv_non_commercial_research)) :named bg_dist_dpv_improve_transport_mobility_dpv_non_commercial_research))
; witness condition negated
(assert (! (not (and (or (= dpv_public_benefit dpv_improve_transport_mobility) (= dpv_non_commercial_research dpv_improve_transport_mobility) (= dpv_improve_transport_mobility dpv_improve_transport_mobility)) (or (and (= dpv_public_benefit dpv_improve_transport_mobility) (or (= dpv_public_benefit dpv_public_benefit) (= dpv_public_benefit dpv_non_commercial_research))) (and (= dpv_non_commercial_research dpv_improve_transport_mobility) (or (= dpv_non_commercial_research dpv_public_benefit) (= dpv_non_commercial_research dpv_non_commercial_research))) (and (= dpv_improve_transport_mobility dpv_improve_transport_mobility) (or (= dpv_improve_transport_mobility dpv_public_benefit) (= dpv_improve_transport_mobility dpv_non_commercial_research)))))) :named w_kgc394))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
