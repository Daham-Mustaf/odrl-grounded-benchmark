; -------------------------------------------------------------------------
; File     : KGC385-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, eq loc:DE-NW against eq loc:DE-BY, ISO rule (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC385-1.smt2
; Status   : unsat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_de_nw () Concept)
(declare-fun loc_de_by () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Instances of the registry rule this problem adopts, named as
; the TPTP side names them.
(assert (! (not (= loc_de_nw loc_de_by)) :named bg_dist_loc_de_nw_loc_de_by))
; witness condition asserted
(assert (! (or (and (= loc_de_nw loc_de_nw) (= loc_de_nw loc_de_by)) (and (= loc_de_by loc_de_nw) (= loc_de_by loc_de_by))) :named w_kgc385))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
