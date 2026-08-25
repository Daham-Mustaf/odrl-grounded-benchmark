; -------------------------------------------------------------------------
; File     : KGC341-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : consent status, or(eq ConsentGiven, eq RenewedConsentGiven) against eq RenewedConsentGiven (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC341-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_consent_given () Concept)
(declare-fun dpv_renewed_consent_given () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; witness condition asserted
(assert (! (or (or (and (= dpv_consent_given dpv_consent_given) (= dpv_consent_given dpv_renewed_consent_given)) (and (= dpv_renewed_consent_given dpv_consent_given) (= dpv_renewed_consent_given dpv_renewed_consent_given))) (or (and (= dpv_consent_given dpv_renewed_consent_given) (= dpv_consent_given dpv_renewed_consent_given)) (and (= dpv_renewed_consent_given dpv_renewed_consent_given) (= dpv_renewed_consent_given dpv_renewed_consent_given)))) :named w_kgc341))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
