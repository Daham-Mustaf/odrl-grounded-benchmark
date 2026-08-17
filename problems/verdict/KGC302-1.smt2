; -------------------------------------------------------------------------
; File     : KGC302-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isPartOf gn:Europe against eq gn:France (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC302-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Resource: France is within Europe.  The order axioms are emitted by the
; writer, in full and quantified, so this file states only the resource.
(assert (! (kge_leq gn_france gn_europe) :named res_kgc302_0))
; witness condition asserted
(assert (! (or (and (kge_leq gn_europe gn_europe) (= gn_europe gn_france))
    (and (kge_leq gn_france gn_europe) (= gn_france gn_france))) :named w_kgc302))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
