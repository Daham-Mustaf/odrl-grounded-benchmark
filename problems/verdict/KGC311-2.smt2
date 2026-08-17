; -------------------------------------------------------------------------
; File     : KGC311-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isA dpv:Purpose against eq dpv:NCR (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC311-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_purpose () Concept)
(declare-fun dpv_non_commercial_research () Concept)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Resource: the two steps.  Neither asserts the chain.
(assert (! (kge_leq dpv_non_commercial_research dpv_non_commercial_purpose) :named res_kgc311_0))
(assert (! (kge_leq dpv_non_commercial_purpose dpv_purpose) :named res_kgc311_1))
; witness condition negated
(assert (! (not (or (and (kge_leq dpv_purpose dpv_purpose) (= dpv_purpose dpv_non_commercial_research))
    (and (kge_leq dpv_non_commercial_research dpv_purpose) (= dpv_non_commercial_research dpv_non_commercial_research)))) :named w_kgc311))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
