; -------------------------------------------------------------------------
; File     : KGC308-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isPartOf Germany against eq France, countries distinct (witness condition asserted)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC308-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun gn_germany () Concept)
(declare-fun gn_france () Concept)
(declare-fun gn_auvergne_rhone_alpes () Concept)
(declare-fun gn_baden_wuerttemberg () Concept)
(declare-fun gn_bayern () Concept)
(declare-fun gn_berlin () Concept)
(declare-fun gn_europe () Concept)
(declare-fun gn_grand_est () Concept)
(declare-fun gn_ile_de_france () Concept)
(declare-fun gn_munich () Concept)
(declare-fun gn_nouvelle_aquitaine () Concept)
(declare-fun gn_occitanie () Concept)
(declare-fun gn_paris () Concept)
(declare-fun gn_provence_alpes_cote_d_azur () Concept)
(declare-fun gn_strasbourg () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
(declare-fun kge_concept (Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_concept gn_auvergne_rhone_alpes) :named gn_auvergne_rhone_alpes_concept))
(assert (! (kge_concept gn_baden_wuerttemberg) :named gn_baden_wuerttemberg_concept))
(assert (! (kge_concept gn_bayern) :named gn_bayern_concept))
(assert (! (kge_concept gn_berlin) :named gn_berlin_concept))
(assert (! (kge_concept gn_europe) :named gn_europe_concept))
(assert (! (kge_concept gn_france) :named gn_france_concept))
(assert (! (kge_concept gn_germany) :named gn_germany_concept))
(assert (! (kge_concept gn_grand_est) :named gn_grand_est_concept))
(assert (! (kge_concept gn_ile_de_france) :named gn_ile_de_france_concept))
(assert (! (kge_concept gn_munich) :named gn_munich_concept))
(assert (! (kge_concept gn_nouvelle_aquitaine) :named gn_nouvelle_aquitaine_concept))
(assert (! (kge_concept gn_occitanie) :named gn_occitanie_concept))
(assert (! (kge_concept gn_paris) :named gn_paris_concept))
(assert (! (kge_concept gn_provence_alpes_cote_d_azur) :named gn_provence_alpes_cote_d_azur_concept))
(assert (! (kge_concept gn_strasbourg) :named gn_strasbourg_concept))
(assert (! (kge_leq gn_auvergne_rhone_alpes gn_france) :named gn_auvergne_rhone_alpes_leq_france))
(assert (! (kge_leq gn_baden_wuerttemberg gn_germany) :named gn_baden_wuerttemberg_leq_germany))
(assert (! (kge_leq gn_bayern gn_germany) :named gn_bayern_leq_germany))
(assert (! (kge_leq gn_berlin gn_germany) :named gn_berlin_leq_germany))
(assert (! (kge_leq gn_france gn_europe) :named gn_france_leq_europe))
(assert (! (kge_leq gn_germany gn_europe) :named gn_germany_leq_europe))
(assert (! (kge_leq gn_grand_est gn_france) :named gn_grand_est_leq_france))
(assert (! (kge_leq gn_ile_de_france gn_france) :named gn_ile_de_france_leq_france))
(assert (! (kge_leq gn_munich gn_bayern) :named gn_munich_leq_bayern))
(assert (! (kge_leq gn_nouvelle_aquitaine gn_france) :named gn_nouvelle_aquitaine_leq_france))
(assert (! (kge_leq gn_occitanie gn_france) :named gn_occitanie_leq_france))
(assert (! (kge_leq gn_paris gn_ile_de_france) :named gn_paris_leq_ile_de_france))
(assert (! (kge_leq gn_provence_alpes_cote_d_azur gn_france) :named gn_provence_alpes_cote_d_azur_leq_france))
(assert (! (kge_leq gn_strasbourg gn_grand_est) :named gn_strasbourg_leq_grand_est))
; Declarations: https://w3id.org/odrl-kb/geonames-europe/declared
(assert (! (not (= gn_germany gn_france)) :named bg_dist_gn_germany_gn_france))
; witness condition asserted
(assert (! (kge_leq gn_france gn_germany) :named w_kgc308))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
