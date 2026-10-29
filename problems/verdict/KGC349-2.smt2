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
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Declared distinctness this problem adopts, named as the TPTP
; side names it.
(assert (! (not (= dpv_consent_expired dpv_consent_withdrawn)) :named bg_dist_dpv_consent_expired_dpv_consent_withdrawn))
(assert (! (not (= dpv_consent_expired dpv_consent_revoked)) :named bg_dist_dpv_consent_expired_dpv_consent_revoked))
; witness condition negated
(assert (! (not (or (and (and (not (= dpv_consent_withdrawn dpv_consent_withdrawn)) (not (= dpv_consent_withdrawn dpv_consent_revoked))) (= dpv_consent_withdrawn dpv_consent_expired)) (and (and (not (= dpv_consent_revoked dpv_consent_withdrawn)) (not (= dpv_consent_revoked dpv_consent_revoked))) (= dpv_consent_revoked dpv_consent_expired)) (and (and (not (= dpv_consent_expired dpv_consent_withdrawn)) (not (= dpv_consent_expired dpv_consent_revoked))) (= dpv_consent_expired dpv_consent_expired)))) :named w_kgc349))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
