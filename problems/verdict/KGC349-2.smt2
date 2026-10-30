; -------------------------------------------------------------------------
; File     : KGC349-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : consent status, isNoneOf {ConsentWithdrawn, ConsentRevoked} against eq ConsentExpired, states declared distinct (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC349-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_consent_withdrawn () Concept)
(declare-fun dpv_consent_revoked () Concept)
(declare-fun dpv_consent_expired () Concept)
(declare-fun dpv_consent_given () Concept)
(declare-fun dpv_consent_invalidated () Concept)
(declare-fun dpv_consent_refused () Concept)
(declare-fun dpv_consent_request_deferred () Concept)
(declare-fun dpv_consent_requested () Concept)
(declare-fun dpv_consent_status () Concept)
(declare-fun dpv_consent_status_invalid_for_processing () Concept)
(declare-fun dpv_consent_status_valid_for_processing () Concept)
(declare-fun dpv_consent_unknown () Concept)
(declare-fun dpv_renewed_consent_given () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq dpv_consent_expired dpv_consent_status_invalid_for_processing) :named res_dpv_consent_expired_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_consent_given dpv_consent_status_valid_for_processing) :named res_dpv_consent_given_below_dpv_consent_status_valid_for_processing))
(assert (! (kge_leq dpv_consent_invalidated dpv_consent_status_invalid_for_processing) :named res_dpv_consent_invalidated_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_consent_refused dpv_consent_status_invalid_for_processing) :named res_dpv_consent_refused_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_consent_request_deferred dpv_consent_status_invalid_for_processing) :named res_dpv_consent_request_deferred_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_consent_requested dpv_consent_status_invalid_for_processing) :named res_dpv_consent_requested_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_consent_revoked dpv_consent_status_invalid_for_processing) :named res_dpv_consent_revoked_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_consent_status_invalid_for_processing dpv_consent_status) :named res_dpv_consent_status_invalid_for_processing_below_dpv_consent_status))
(assert (! (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status) :named res_dpv_consent_status_valid_for_processing_below_dpv_consent_status))
(assert (! (kge_leq dpv_consent_unknown dpv_consent_status_invalid_for_processing) :named res_dpv_consent_unknown_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_consent_withdrawn dpv_consent_status_invalid_for_processing) :named res_dpv_consent_withdrawn_below_dpv_consent_status_invalid_for_processing))
(assert (! (kge_leq dpv_renewed_consent_given dpv_consent_status_valid_for_processing) :named res_dpv_renewed_consent_given_below_dpv_consent_status_valid_for_processing))
; Declarations: https://w3id.org/odrl-kb/dpv-consent/declared
(assert (! (not (= dpv_consent_withdrawn dpv_consent_revoked)) :named bg_dist_dpv_consent_withdrawn_dpv_consent_revoked))
(assert (! (not (= dpv_consent_withdrawn dpv_consent_expired)) :named bg_dist_dpv_consent_withdrawn_dpv_consent_expired))
(assert (! (not (= dpv_consent_revoked dpv_consent_expired)) :named bg_dist_dpv_consent_revoked_dpv_consent_expired))
; witness condition negated
(assert (! (not (and (not (= dpv_consent_expired dpv_consent_withdrawn)) (not (= dpv_consent_expired dpv_consent_revoked)))) :named w_kgc349))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
