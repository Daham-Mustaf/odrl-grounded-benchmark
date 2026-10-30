; -------------------------------------------------------------------------
; File     : KGC376-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : language, isAllOf nl fr against eq nl, distinctness rule declared (witness condition asserted)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC376-1.smt2
; Status   : unsat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun bcp_nl () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
(declare-fun kge_concept (Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_concept bcp_fr) :named res_bcp47_fr))
(assert (! (kge_concept bcp_nl) :named res_bcp47_nl))
; Declarations: https://w3id.org/odrl-kb/bcp47/distinct
(assert (! (not (= bcp_nl bcp_fr)) :named bg_dist_bcp47_nl_fr))
; witness condition asserted
(assert (! (= bcp_fr bcp_nl) :named w_kgc376))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
