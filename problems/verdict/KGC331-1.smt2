; -------------------------------------------------------------------------
; File     : KGC331-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isPartOf loc:EU against eq loc:DE (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC331-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_eu () Concept)
(declare-fun loc_de () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Resource: membership, read as the order by the jurisdictional profile and
; not read at all by the geographic one.
(assert (! (kge_leq loc_de loc_eu) :named res_kgc331_0))
; witness condition asserted
(assert (! (or (and (kge_leq loc_eu loc_eu) (= loc_eu loc_de))
    (and (kge_leq loc_de loc_eu) (= loc_de loc_de))) :named w_kgc331))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
