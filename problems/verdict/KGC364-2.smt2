; -------------------------------------------------------------------------
; File     : KGC364-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : measures, isAllOf {Encryption, AccessControl} against eq Encryption, declared distinct (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC364-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun tm_encryption () Concept)
(declare-fun tm_access_control_method () Concept)
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
(assert (! (not (= tm_encryption tm_access_control_method)) :named bg_dist_tm_encryption_tm_access_control_method))
; witness condition negated
(assert (! (not (and (= tm_encryption tm_encryption) (= tm_access_control_method tm_encryption) (or (= tm_encryption tm_encryption) (= tm_access_control_method tm_encryption)))) :named w_kgc364))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
