; -------------------------------------------------------------------------
; File     : KGC334-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, eq loc:DE against eq loc:FR, under the ISO 3166 uniqueness rule (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC334-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_de () Concept)
(declare-fun loc_fr () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Resource: unchanged from KGC333.
; The instance of the registry rule this problem adopts, named as the TPTP
; side names it so that a proof and an unsat core cite one assertion.
(assert (! (distinct loc_de loc_fr) :named bt_loc_de_distinct_loc_fr))
; witness condition negated
(assert (! (not (or (and (= loc_de loc_de) (= loc_de loc_fr))
    (and (= loc_fr loc_de) (= loc_fr loc_fr)))) :named w_kgc334))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
