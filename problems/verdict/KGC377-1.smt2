; -------------------------------------------------------------------------
; File     : KGC377-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : language, isNoneOf en it against eq it, no declaration (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC377-1.smt2
; Status   : unsat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun bcp_en () Concept)
(declare-fun bcp_it () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
(declare-fun kge_concept (Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_concept bcp_en) :named res_bcp47_en))
(assert (! (kge_concept bcp_it) :named res_bcp47_it))
; witness condition asserted
(assert (! (or (and (and (not (= bcp_en bcp_en)) (not (= bcp_en bcp_it))) (= bcp_en bcp_it)) (and (and (not (= bcp_it bcp_en)) (not (= bcp_it bcp_it))) (= bcp_it bcp_it))) :named w_kgc377))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
