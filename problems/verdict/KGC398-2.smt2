; -------------------------------------------------------------------------
; File     : KGC398-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : language, isAnyOf {de, fr} against isAllOf {nl, fr}, no declaration (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC398-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_nl () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
(declare-fun kge_concept (Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_concept bcp_de) :named res_bcp47_de))
(assert (! (kge_concept bcp_fr) :named res_bcp47_fr))
(assert (! (kge_concept bcp_nl) :named res_bcp47_nl))
; witness condition negated
(assert (! (not (and true true (or (and true (or (= bcp_de bcp_de) (= bcp_de bcp_fr))) (and true (or (= bcp_fr bcp_de) (= bcp_fr bcp_fr))) (and true (or (= bcp_nl bcp_de) (= bcp_nl bcp_fr)))))) :named w_kgc398))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
