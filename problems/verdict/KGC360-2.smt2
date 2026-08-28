; -------------------------------------------------------------------------
; File     : KGC360-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : measures, isAllOf(Encryption, AccessControlMethod) against isA TechnicalMeasure (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC360-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun tm_encryption () Concept)
(declare-fun tm_access_control_method () Concept)
(declare-fun tm_technical_measure () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq tm_access_control_method tm_technical_measure) :named res_tm_access_control_method_below_tm_technical_measure))
(assert (! (kge_leq tm_encryption tm_technical_measure) :named res_tm_encryption_below_tm_technical_measure))
; witness condition negated
(assert (! (not (and (kge_leq tm_encryption tm_technical_measure) (kge_leq tm_access_control_method tm_technical_measure) (or (kge_leq tm_encryption tm_technical_measure) (kge_leq tm_access_control_method tm_technical_measure) (kge_leq tm_technical_measure tm_technical_measure)))) :named w_kgc360))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
