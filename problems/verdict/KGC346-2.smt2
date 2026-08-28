; -------------------------------------------------------------------------
; File     : KGC346-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : consent status, xone(isA ValidForProcessing, isA InvalidForProcessing) against eq ConsentGiven (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC346-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_consent_status_valid_for_processing () Concept)
(declare-fun dpv_consent_status_invalid_for_processing () Concept)
(declare-fun dpv_consent_given () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq dpv_consent_given dpv_consent_status_valid_for_processing) :named res_dpv_consent_given_below_dpv_consent_status_valid_for_processing))
; witness condition negated
(assert (! (not (or (and (or (and (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status_valid_for_processing) (= dpv_consent_status_valid_for_processing dpv_consent_given)) (and (kge_leq dpv_consent_status_invalid_for_processing dpv_consent_status_valid_for_processing) (= dpv_consent_status_invalid_for_processing dpv_consent_given)) (and (kge_leq dpv_consent_given dpv_consent_status_valid_for_processing) (= dpv_consent_given dpv_consent_given))) (or (and (and (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status_valid_for_processing) (= dpv_consent_status_valid_for_processing dpv_consent_given)) (not (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status_invalid_for_processing))) (and (and (kge_leq dpv_consent_status_invalid_for_processing dpv_consent_status_valid_for_processing) (= dpv_consent_status_invalid_for_processing dpv_consent_given)) (not (kge_leq dpv_consent_status_invalid_for_processing dpv_consent_status_invalid_for_processing))) (and (and (kge_leq dpv_consent_given dpv_consent_status_valid_for_processing) (= dpv_consent_given dpv_consent_given)) (not (kge_leq dpv_consent_given dpv_consent_status_invalid_for_processing))))) (and (or (and (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status_invalid_for_processing) (= dpv_consent_status_valid_for_processing dpv_consent_given)) (and (kge_leq dpv_consent_status_invalid_for_processing dpv_consent_status_invalid_for_processing) (= dpv_consent_status_invalid_for_processing dpv_consent_given)) (and (kge_leq dpv_consent_given dpv_consent_status_invalid_for_processing) (= dpv_consent_given dpv_consent_given))) (or (and (and (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status_invalid_for_processing) (= dpv_consent_status_valid_for_processing dpv_consent_given)) (not (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status_valid_for_processing))) (and (and (kge_leq dpv_consent_status_invalid_for_processing dpv_consent_status_invalid_for_processing) (= dpv_consent_status_invalid_for_processing dpv_consent_given)) (not (kge_leq dpv_consent_status_invalid_for_processing dpv_consent_status_valid_for_processing))) (and (and (kge_leq dpv_consent_given dpv_consent_status_invalid_for_processing) (= dpv_consent_given dpv_consent_given)) (not (kge_leq dpv_consent_given dpv_consent_status_valid_for_processing))))))) :named w_kgc346))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
