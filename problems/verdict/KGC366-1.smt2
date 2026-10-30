; -------------------------------------------------------------------------
; File     : KGC366-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : measures, isAnyOf {Encryption, AccessControl} against eq EncryptionAtRest, declared distinct (witness condition asserted)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC366-1.smt2
; Status   : unsat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun tm_encryption () Concept)
(declare-fun tm_access_control_method () Concept)
(declare-fun tm_encryption_at_rest () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq tm_encryption_at_rest tm_encryption) :named res_tm_encryption_at_rest_below_tm_encryption))
; Declarations: https://w3id.org/odrl-kb/dpv-tom/declared
(assert (! (not (= tm_encryption tm_access_control_method)) :named bg_dist_tm_encryption_tm_access_control_method))
(assert (! (not (= tm_encryption tm_encryption_at_rest)) :named bg_dist_tm_encryption_tm_encryption_at_rest))
(assert (! (not (= tm_access_control_method tm_encryption_at_rest)) :named bg_dist_tm_access_control_method_tm_encryption_at_rest))
; witness condition asserted
(assert (! (or (= tm_encryption tm_encryption_at_rest) (= tm_access_control_method tm_encryption_at_rest)) :named w_kgc366))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
