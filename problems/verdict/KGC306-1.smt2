; -------------------------------------------------------------------------
; File     : KGC306-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, xone(isPartOf France, isPartOf Germany) against eq France, countries disjoint (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC306-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun gn_france () Concept)
(declare-fun gn_germany () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; The same disjointness, named as the TPTP side names it.
(assert (! (forall ((x Concept))
    (not (and (kge_leq x gn_france) (kge_leq x gn_germany))))
  :named bg_disj_gn_france_disjoint_gn_germany))
; witness condition asserted
(assert (! (or (and (or (and (kge_leq gn_france gn_france) (= gn_france gn_france)) (and (kge_leq gn_germany gn_france) (= gn_germany gn_france))) (or (and (and (kge_leq gn_france gn_france) (= gn_france gn_france)) (not (kge_leq gn_france gn_germany))) (and (and (kge_leq gn_germany gn_france) (= gn_germany gn_france)) (not (kge_leq gn_germany gn_germany))))) (and (or (and (kge_leq gn_france gn_germany) (= gn_france gn_france)) (and (kge_leq gn_germany gn_germany) (= gn_germany gn_france))) (or (and (and (kge_leq gn_france gn_germany) (= gn_france gn_france)) (not (kge_leq gn_france gn_france))) (and (and (kge_leq gn_germany gn_germany) (= gn_germany gn_france)) (not (kge_leq gn_germany gn_france)))))) :named w_kgc306))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
