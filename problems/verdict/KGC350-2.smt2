; -------------------------------------------------------------------------
; File     : KGC350-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : legal basis, isAnyOf Article 6(1) against eq dpv:Consent (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC350-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun lb_dpv_consent () Concept)
(declare-fun lb_dpv_contract () Concept)
(declare-fun lb_dpv_legal_obligation () Concept)
(declare-fun lb_dpv_vital_interest () Concept)
(declare-fun lb_dpv_public_interest () Concept)
(declare-fun lb_dpv_official_authority_of_controller () Concept)
(declare-fun lb_dpv_legitimate_interest () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; witness condition negated
(assert (! (not (and (or (= lb_dpv_consent lb_dpv_consent) (= lb_dpv_contract lb_dpv_consent) (= lb_dpv_legal_obligation lb_dpv_consent) (= lb_dpv_vital_interest lb_dpv_consent) (= lb_dpv_public_interest lb_dpv_consent) (= lb_dpv_official_authority_of_controller lb_dpv_consent) (= lb_dpv_legitimate_interest lb_dpv_consent)) (or (and (= lb_dpv_consent lb_dpv_consent) (or (= lb_dpv_consent lb_dpv_consent) (= lb_dpv_consent lb_dpv_contract) (= lb_dpv_consent lb_dpv_legal_obligation) (= lb_dpv_consent lb_dpv_vital_interest) (= lb_dpv_consent lb_dpv_public_interest) (= lb_dpv_consent lb_dpv_official_authority_of_controller) (= lb_dpv_consent lb_dpv_legitimate_interest))) (and (= lb_dpv_contract lb_dpv_consent) (or (= lb_dpv_contract lb_dpv_consent) (= lb_dpv_contract lb_dpv_contract) (= lb_dpv_contract lb_dpv_legal_obligation) (= lb_dpv_contract lb_dpv_vital_interest) (= lb_dpv_contract lb_dpv_public_interest) (= lb_dpv_contract lb_dpv_official_authority_of_controller) (= lb_dpv_contract lb_dpv_legitimate_interest))) (and (= lb_dpv_legal_obligation lb_dpv_consent) (or (= lb_dpv_legal_obligation lb_dpv_consent) (= lb_dpv_legal_obligation lb_dpv_contract) (= lb_dpv_legal_obligation lb_dpv_legal_obligation) (= lb_dpv_legal_obligation lb_dpv_vital_interest) (= lb_dpv_legal_obligation lb_dpv_public_interest) (= lb_dpv_legal_obligation lb_dpv_official_authority_of_controller) (= lb_dpv_legal_obligation lb_dpv_legitimate_interest))) (and (= lb_dpv_vital_interest lb_dpv_consent) (or (= lb_dpv_vital_interest lb_dpv_consent) (= lb_dpv_vital_interest lb_dpv_contract) (= lb_dpv_vital_interest lb_dpv_legal_obligation) (= lb_dpv_vital_interest lb_dpv_vital_interest) (= lb_dpv_vital_interest lb_dpv_public_interest) (= lb_dpv_vital_interest lb_dpv_official_authority_of_controller) (= lb_dpv_vital_interest lb_dpv_legitimate_interest))) (and (= lb_dpv_public_interest lb_dpv_consent) (or (= lb_dpv_public_interest lb_dpv_consent) (= lb_dpv_public_interest lb_dpv_contract) (= lb_dpv_public_interest lb_dpv_legal_obligation) (= lb_dpv_public_interest lb_dpv_vital_interest) (= lb_dpv_public_interest lb_dpv_public_interest) (= lb_dpv_public_interest lb_dpv_official_authority_of_controller) (= lb_dpv_public_interest lb_dpv_legitimate_interest))) (and (= lb_dpv_official_authority_of_controller lb_dpv_consent) (or (= lb_dpv_official_authority_of_controller lb_dpv_consent) (= lb_dpv_official_authority_of_controller lb_dpv_contract) (= lb_dpv_official_authority_of_controller lb_dpv_legal_obligation) (= lb_dpv_official_authority_of_controller lb_dpv_vital_interest) (= lb_dpv_official_authority_of_controller lb_dpv_public_interest) (= lb_dpv_official_authority_of_controller lb_dpv_official_authority_of_controller) (= lb_dpv_official_authority_of_controller lb_dpv_legitimate_interest))) (and (= lb_dpv_legitimate_interest lb_dpv_consent) (or (= lb_dpv_legitimate_interest lb_dpv_consent) (= lb_dpv_legitimate_interest lb_dpv_contract) (= lb_dpv_legitimate_interest lb_dpv_legal_obligation) (= lb_dpv_legitimate_interest lb_dpv_vital_interest) (= lb_dpv_legitimate_interest lb_dpv_public_interest) (= lb_dpv_legitimate_interest lb_dpv_official_authority_of_controller) (= lb_dpv_legitimate_interest lb_dpv_legitimate_interest)))))) :named w_kgc350))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
