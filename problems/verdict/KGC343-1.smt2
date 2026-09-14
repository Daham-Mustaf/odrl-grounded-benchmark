; -------------------------------------------------------------------------
; File     : KGC343-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : consent status, isA ValidForProcessing against eq ConsentWithdrawn, branches disjoint (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC343-1.smt2
; Status   : unsat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_consent_status_valid_for_processing () Concept)
(declare-fun dpv_consent_withdrawn () Concept)
(declare-fun dpv_consent_status_invalid_for_processing () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq dpv_consent_withdrawn dpv_consent_status_invalid_for_processing) :named res_dpv_consent_withdrawn_below_dpv_consent_status_invalid_for_processing))
; The same disjointness, named as the TPTP side names it.
(assert (! (forall ((x Concept))
    (not (and (kge_leq x dpv_consent_status_valid_for_processing) (kge_leq x dpv_consent_status_invalid_for_processing))))
  :named bg_disj_dpv_consent_status_valid_for_processing_disjoint_dpv_consent_status_invalid_for_processing))
; witness condition asserted
(assert (! (or (and (kge_leq dpv_consent_status_valid_for_processing dpv_consent_status_valid_for_processing) (= dpv_consent_status_valid_for_processing dpv_consent_withdrawn)) (and (kge_leq dpv_consent_withdrawn dpv_consent_status_valid_for_processing) (= dpv_consent_withdrawn dpv_consent_withdrawn))) :named w_kgc343))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
