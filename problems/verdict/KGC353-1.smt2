; -------------------------------------------------------------------------
; File     : KGC353-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : legal basis, isA dpv:LegalBasis against eq A6-1-a-explicit-consent (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC353-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun lb_dpv_legal_basis () Concept)
(declare-fun lb_gdpr_a6_1_a_explicit_consent () Concept)
(declare-fun lb_dpv_consent () Concept)
(declare-fun lb_gdpr_a6_1_a () Concept)
(declare-fun lb_gdpr_consent () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq lb_dpv_consent lb_dpv_legal_basis) :named res_lb_dpv_consent_below_lb_dpv_legal_basis))
(assert (! (kge_leq lb_gdpr_a6_1_a lb_gdpr_consent) :named res_lb_gdpr_a6_1_a_below_lb_gdpr_consent))
(assert (! (kge_leq lb_gdpr_a6_1_a_explicit_consent lb_gdpr_a6_1_a) :named res_lb_gdpr_a6_1_a_explicit_consent_below_lb_gdpr_a6_1_a))
(assert (! (kge_leq lb_gdpr_a6_1_a_explicit_consent lb_gdpr_consent) :named res_lb_gdpr_a6_1_a_explicit_consent_below_lb_gdpr_consent))
(assert (! (kge_leq lb_gdpr_consent lb_dpv_consent) :named res_lb_gdpr_consent_below_lb_dpv_consent))
; witness condition asserted
(assert (! (or (and (kge_leq lb_dpv_legal_basis lb_dpv_legal_basis) (= lb_dpv_legal_basis lb_gdpr_a6_1_a_explicit_consent)) (and (kge_leq lb_gdpr_a6_1_a_explicit_consent lb_dpv_legal_basis) (= lb_gdpr_a6_1_a_explicit_consent lb_gdpr_a6_1_a_explicit_consent))) :named w_kgc353))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
