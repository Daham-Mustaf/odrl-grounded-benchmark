; -------------------------------------------------------------------------
; File     : KGC395-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, or(isA PublicBenefit, isA NonCommercialResearch) against eq ImproveTransportMobility (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC395-2.smt2
; Status   : unsat
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
; witness condition negated
(assert (! (not (or (or (and (kge_leq dpv_public_benefit dpv_public_benefit) (= dpv_public_benefit dpv_improve_transport_mobility)) (and (kge_leq dpv_non_commercial_research dpv_public_benefit) (= dpv_non_commercial_research dpv_improve_transport_mobility)) (and (kge_leq dpv_improve_transport_mobility dpv_public_benefit) (= dpv_improve_transport_mobility dpv_improve_transport_mobility))) (or (and (kge_leq dpv_public_benefit dpv_non_commercial_research) (= dpv_public_benefit dpv_improve_transport_mobility)) (and (kge_leq dpv_non_commercial_research dpv_non_commercial_research) (= dpv_non_commercial_research dpv_improve_transport_mobility)) (and (kge_leq dpv_improve_transport_mobility dpv_non_commercial_research) (= dpv_improve_transport_mobility dpv_improve_transport_mobility))))) :named w_kgc395))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
