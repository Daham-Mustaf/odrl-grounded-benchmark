; -------------------------------------------------------------------------
; File     : KGC397-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isNoneOf {Marketing} against eq Advertising, declared distinct (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC397-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
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
; Declarations: https://w3id.org/odrl-kb/dpv-purposes/declared
(assert (! (not (= dpv_marketing dpv_advertising)) :named bg_dist_dpv_marketing_dpv_advertising))
; witness condition negated
(assert (! (not (not (= dpv_advertising dpv_marketing))) :named w_kgc397))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
