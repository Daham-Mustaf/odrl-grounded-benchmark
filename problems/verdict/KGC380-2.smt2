; -------------------------------------------------------------------------
; File     : KGC380-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isPartOf loc:EU against eq loc:BQ, jurisdictional (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC380-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_eu () Concept)
(declare-fun loc_bq () Concept)
(declare-fun loc_eu27 () Concept)
(declare-fun loc_eu28 () Concept)
(declare-fun loc_nl () Concept)
(declare-fun loc_nl_bq1 () Concept)
(declare-fun loc_nl_bq2 () Concept)
(declare-fun loc_nl_bq3 () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq loc_bq loc_nl) :named res_loc_bq_within_loc_nl))
(assert (! (kge_leq loc_eu27 loc_eu) :named res_loc_eu27_within_loc_eu))
(assert (! (kge_leq loc_eu28 loc_eu) :named res_loc_eu28_within_loc_eu))
(assert (! (kge_leq loc_nl loc_eu) :named res_loc_nl_within_loc_eu))
(assert (! (kge_leq loc_nl loc_eu27) :named res_loc_nl_within_loc_eu27))
(assert (! (kge_leq loc_nl loc_eu28) :named res_loc_nl_within_loc_eu28))
(assert (! (kge_leq loc_nl_bq1 loc_nl) :named res_loc_nl_bq1_within_loc_nl))
(assert (! (kge_leq loc_nl_bq2 loc_nl) :named res_loc_nl_bq2_within_loc_nl))
(assert (! (kge_leq loc_nl_bq3 loc_nl) :named res_loc_nl_bq3_within_loc_nl))
(assert (! (kge_leq loc_bq loc_nl_bq1) :named res_loc_bq_same_loc_nl_bq1))
(assert (! (kge_leq loc_nl_bq1 loc_bq) :named res_loc_nl_bq1_same_loc_bq))
(assert (! (kge_leq loc_bq loc_nl_bq2) :named res_loc_bq_same_loc_nl_bq2))
(assert (! (kge_leq loc_nl_bq2 loc_bq) :named res_loc_nl_bq2_same_loc_bq))
(assert (! (kge_leq loc_bq loc_nl_bq3) :named res_loc_bq_same_loc_nl_bq3))
(assert (! (kge_leq loc_nl_bq3 loc_bq) :named res_loc_nl_bq3_same_loc_bq))
; witness condition negated
(assert (! (not (or (and (kge_leq loc_eu loc_eu) (= loc_eu loc_bq)) (and (kge_leq loc_bq loc_eu) (= loc_bq loc_bq)))) :named w_kgc380))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
