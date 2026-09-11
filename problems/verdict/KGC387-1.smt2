; -------------------------------------------------------------------------
; File     : KGC387-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isNoneOf {loc:DE-BY, loc:DE-BE} against eq loc:DE-HH, ISO rule (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC387-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_de_by () Concept)
(declare-fun loc_de_be () Concept)
(declare-fun loc_de_hh () Concept)
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
(assert (! (not (= loc_de_hh loc_de_by)) :named bg_dist_loc_de_hh_loc_de_by))
(assert (! (not (= loc_de_hh loc_de_be)) :named bg_dist_loc_de_hh_loc_de_be))
; witness condition asserted
(assert (! (or (and (and (not (= loc_de_by loc_de_by)) (not (= loc_de_by loc_de_be))) (= loc_de_by loc_de_hh)) (and (and (not (= loc_de_be loc_de_by)) (not (= loc_de_be loc_de_be))) (= loc_de_be loc_de_hh)) (and (and (not (= loc_de_hh loc_de_by)) (not (= loc_de_hh loc_de_be))) (= loc_de_hh loc_de_hh))) :named w_kgc387))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
