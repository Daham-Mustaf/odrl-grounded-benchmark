; -------------------------------------------------------------------------
; File     : KGC397-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isNoneOf {Marketing} against eq Advertising, declared distinct (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC397-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_marketing () Concept)
(declare-fun dpv_advertising () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq dpv_advertising dpv_marketing) :named res_dpv_advertising_below_dpv_marketing))
; Declared distinctness this problem adopts, named as the TPTP
; side names it.
(assert (! (not (= dpv_advertising dpv_marketing)) :named bg_dist_dpv_advertising_dpv_marketing))
; witness condition asserted
(assert (! (or (and (not (= dpv_marketing dpv_marketing)) (= dpv_marketing dpv_advertising)) (and (not (= dpv_advertising dpv_marketing)) (= dpv_advertising dpv_advertising))) :named w_kgc397))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
