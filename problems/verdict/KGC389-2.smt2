; -------------------------------------------------------------------------
; File     : KGC389-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, xone(eq loc:DE-NW, eq loc:DE-BY) against eq loc:DE-NW (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC389-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
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
; witness condition negated
(assert (! (not (or (and (or (and (= loc_de_nw loc_de_nw) (= loc_de_nw loc_de_nw)) (and (= loc_de_by loc_de_nw) (= loc_de_by loc_de_nw))) (or (and (and (= loc_de_nw loc_de_nw) (= loc_de_nw loc_de_nw)) (not (= loc_de_nw loc_de_by))) (and (and (= loc_de_by loc_de_nw) (= loc_de_by loc_de_nw)) (not (= loc_de_by loc_de_by))))) (and (or (and (= loc_de_nw loc_de_by) (= loc_de_nw loc_de_nw)) (and (= loc_de_by loc_de_by) (= loc_de_by loc_de_nw))) (or (and (and (= loc_de_nw loc_de_by) (= loc_de_nw loc_de_nw)) (not (= loc_de_nw loc_de_nw))) (and (and (= loc_de_by loc_de_by) (= loc_de_by loc_de_nw)) (not (= loc_de_by loc_de_nw))))))) :named w_kgc389))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
