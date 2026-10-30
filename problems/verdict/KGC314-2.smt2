; -------------------------------------------------------------------------
; File     : KGC314-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, eq dpv:ScientificResearch against eq dpv:Marketing, under a declared distinctness (witness condition negated)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC314-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_marketing () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Declarations: https://w3id.org/odrl-kb/dpv-purposes/declared
(assert (! (not (= dpv_scientific_research dpv_marketing)) :named bg_dist_dpv_scientific_research_dpv_marketing))
; witness condition negated
(assert (! (not (= dpv_scientific_research dpv_marketing)) :named w_kgc314))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
