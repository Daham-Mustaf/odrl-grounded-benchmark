; -------------------------------------------------------------------------
; File     : KGC331-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isPartOf loc:EU against eq loc:DE (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC331-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_eu () Concept)
(declare-fun loc_de () Concept)
(declare-fun loc_eu27 () Concept)
(declare-fun loc_eu28 () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq loc_de loc_eu) :named res_loc_de_within_loc_eu))
(assert (! (kge_leq loc_de loc_eu27) :named res_loc_de_within_loc_eu27))
(assert (! (kge_leq loc_de loc_eu28) :named res_loc_de_within_loc_eu28))
(assert (! (kge_leq loc_eu27 loc_eu) :named res_loc_eu27_within_loc_eu))
(assert (! (kge_leq loc_eu28 loc_eu) :named res_loc_eu28_within_loc_eu))
; witness condition negated
(assert (! (not (kge_leq loc_de loc_eu)) :named w_kgc331))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
