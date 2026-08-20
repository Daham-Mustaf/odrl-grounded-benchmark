; -------------------------------------------------------------------------
; File     : KGC330-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isPartOf loc:NL against eq loc:BQ (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC330-2.smt2
; Status   : unsat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_nl () Concept)
(declare-fun loc_bq () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Resource: the containment the extension publishes.
(assert (! (kge_leq loc_bq loc_nl) :named res_kgc330_0))
; witness condition negated
(assert (! (not (or (and (kge_leq loc_nl loc_nl) (= loc_nl loc_bq))
    (and (kge_leq loc_bq loc_nl) (= loc_bq loc_bq)))) :named w_kgc330))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
