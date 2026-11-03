%------------------------------------------------------------------------------
% File     : KGC012+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use within Germany against use in France only: no use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The two versions have the
%            same status.
% English  : A library permits use within Germany. A researcher's policy
%            commits to use in France. France and Germany are declared
%            distinct. This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC308-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC308 is Unknown. Its two problems state that some use meets the
%            two policies (KGC011) and that no use does (KGC012). A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+5.ax').

fof(bg_dist_gn_germany_gn_france, axiom,
    gn_germany != gn_france).

fof(bg_dist_gn_germany_gn_auvergne_rhone_alpes, axiom,
    gn_germany != gn_auvergne_rhone_alpes).

fof(bg_dist_gn_germany_gn_baden_wuerttemberg, axiom,
    gn_germany != gn_baden_wuerttemberg).

fof(bg_dist_gn_germany_gn_bayern, axiom,
    gn_germany != gn_bayern).

fof(bg_dist_gn_germany_gn_berlin, axiom,
    gn_germany != gn_berlin).

fof(bg_dist_gn_germany_gn_europe, axiom,
    gn_germany != gn_europe).

fof(bg_dist_gn_germany_gn_grand_est, axiom,
    gn_germany != gn_grand_est).

fof(bg_dist_gn_germany_gn_ile_de_france, axiom,
    gn_germany != gn_ile_de_france).

fof(bg_dist_gn_germany_gn_munich, axiom,
    gn_germany != gn_munich).

fof(bg_dist_gn_germany_gn_nouvelle_aquitaine, axiom,
    gn_germany != gn_nouvelle_aquitaine).

fof(bg_dist_gn_germany_gn_occitanie, axiom,
    gn_germany != gn_occitanie).

fof(bg_dist_gn_germany_gn_paris, axiom,
    gn_germany != gn_paris).

fof(bg_dist_gn_germany_gn_provence_alpes_cote_d_azur, axiom,
    gn_germany != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_germany_gn_strasbourg, axiom,
    gn_germany != gn_strasbourg).

fof(bg_dist_gn_france_gn_auvergne_rhone_alpes, axiom,
    gn_france != gn_auvergne_rhone_alpes).

fof(bg_dist_gn_france_gn_baden_wuerttemberg, axiom,
    gn_france != gn_baden_wuerttemberg).

fof(bg_dist_gn_france_gn_bayern, axiom,
    gn_france != gn_bayern).

fof(bg_dist_gn_france_gn_berlin, axiom,
    gn_france != gn_berlin).

fof(bg_dist_gn_france_gn_europe, axiom,
    gn_france != gn_europe).

fof(bg_dist_gn_france_gn_grand_est, axiom,
    gn_france != gn_grand_est).

fof(bg_dist_gn_france_gn_ile_de_france, axiom,
    gn_france != gn_ile_de_france).

fof(bg_dist_gn_france_gn_munich, axiom,
    gn_france != gn_munich).

fof(bg_dist_gn_france_gn_nouvelle_aquitaine, axiom,
    gn_france != gn_nouvelle_aquitaine).

fof(bg_dist_gn_france_gn_occitanie, axiom,
    gn_france != gn_occitanie).

fof(bg_dist_gn_france_gn_paris, axiom,
    gn_france != gn_paris).

fof(bg_dist_gn_france_gn_provence_alpes_cote_d_azur, axiom,
    gn_france != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_france_gn_strasbourg, axiom,
    gn_france != gn_strasbourg).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_baden_wuerttemberg, axiom,
    gn_auvergne_rhone_alpes != gn_baden_wuerttemberg).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_bayern, axiom,
    gn_auvergne_rhone_alpes != gn_bayern).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_berlin, axiom,
    gn_auvergne_rhone_alpes != gn_berlin).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_europe, axiom,
    gn_auvergne_rhone_alpes != gn_europe).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_grand_est, axiom,
    gn_auvergne_rhone_alpes != gn_grand_est).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_ile_de_france, axiom,
    gn_auvergne_rhone_alpes != gn_ile_de_france).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_munich, axiom,
    gn_auvergne_rhone_alpes != gn_munich).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_nouvelle_aquitaine, axiom,
    gn_auvergne_rhone_alpes != gn_nouvelle_aquitaine).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_occitanie, axiom,
    gn_auvergne_rhone_alpes != gn_occitanie).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_paris, axiom,
    gn_auvergne_rhone_alpes != gn_paris).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_provence_alpes_cote_d_azur, axiom,
    gn_auvergne_rhone_alpes != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_auvergne_rhone_alpes_gn_strasbourg, axiom,
    gn_auvergne_rhone_alpes != gn_strasbourg).

fof(bg_dist_gn_baden_wuerttemberg_gn_bayern, axiom,
    gn_baden_wuerttemberg != gn_bayern).

fof(bg_dist_gn_baden_wuerttemberg_gn_berlin, axiom,
    gn_baden_wuerttemberg != gn_berlin).

fof(bg_dist_gn_baden_wuerttemberg_gn_europe, axiom,
    gn_baden_wuerttemberg != gn_europe).

fof(bg_dist_gn_baden_wuerttemberg_gn_grand_est, axiom,
    gn_baden_wuerttemberg != gn_grand_est).

fof(bg_dist_gn_baden_wuerttemberg_gn_ile_de_france, axiom,
    gn_baden_wuerttemberg != gn_ile_de_france).

fof(bg_dist_gn_baden_wuerttemberg_gn_munich, axiom,
    gn_baden_wuerttemberg != gn_munich).

fof(bg_dist_gn_baden_wuerttemberg_gn_nouvelle_aquitaine, axiom,
    gn_baden_wuerttemberg != gn_nouvelle_aquitaine).

fof(bg_dist_gn_baden_wuerttemberg_gn_occitanie, axiom,
    gn_baden_wuerttemberg != gn_occitanie).

fof(bg_dist_gn_baden_wuerttemberg_gn_paris, axiom,
    gn_baden_wuerttemberg != gn_paris).

fof(bg_dist_gn_baden_wuerttemberg_gn_provence_alpes_cote_d_azur, axiom,
    gn_baden_wuerttemberg != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_baden_wuerttemberg_gn_strasbourg, axiom,
    gn_baden_wuerttemberg != gn_strasbourg).

fof(bg_dist_gn_bayern_gn_berlin, axiom,
    gn_bayern != gn_berlin).

fof(bg_dist_gn_bayern_gn_europe, axiom,
    gn_bayern != gn_europe).

fof(bg_dist_gn_bayern_gn_grand_est, axiom,
    gn_bayern != gn_grand_est).

fof(bg_dist_gn_bayern_gn_ile_de_france, axiom,
    gn_bayern != gn_ile_de_france).

fof(bg_dist_gn_bayern_gn_munich, axiom,
    gn_bayern != gn_munich).

fof(bg_dist_gn_bayern_gn_nouvelle_aquitaine, axiom,
    gn_bayern != gn_nouvelle_aquitaine).

fof(bg_dist_gn_bayern_gn_occitanie, axiom,
    gn_bayern != gn_occitanie).

fof(bg_dist_gn_bayern_gn_paris, axiom,
    gn_bayern != gn_paris).

fof(bg_dist_gn_bayern_gn_provence_alpes_cote_d_azur, axiom,
    gn_bayern != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_bayern_gn_strasbourg, axiom,
    gn_bayern != gn_strasbourg).

fof(bg_dist_gn_berlin_gn_europe, axiom,
    gn_berlin != gn_europe).

fof(bg_dist_gn_berlin_gn_grand_est, axiom,
    gn_berlin != gn_grand_est).

fof(bg_dist_gn_berlin_gn_ile_de_france, axiom,
    gn_berlin != gn_ile_de_france).

fof(bg_dist_gn_berlin_gn_munich, axiom,
    gn_berlin != gn_munich).

fof(bg_dist_gn_berlin_gn_nouvelle_aquitaine, axiom,
    gn_berlin != gn_nouvelle_aquitaine).

fof(bg_dist_gn_berlin_gn_occitanie, axiom,
    gn_berlin != gn_occitanie).

fof(bg_dist_gn_berlin_gn_paris, axiom,
    gn_berlin != gn_paris).

fof(bg_dist_gn_berlin_gn_provence_alpes_cote_d_azur, axiom,
    gn_berlin != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_berlin_gn_strasbourg, axiom,
    gn_berlin != gn_strasbourg).

fof(bg_dist_gn_europe_gn_grand_est, axiom,
    gn_europe != gn_grand_est).

fof(bg_dist_gn_europe_gn_ile_de_france, axiom,
    gn_europe != gn_ile_de_france).

fof(bg_dist_gn_europe_gn_munich, axiom,
    gn_europe != gn_munich).

fof(bg_dist_gn_europe_gn_nouvelle_aquitaine, axiom,
    gn_europe != gn_nouvelle_aquitaine).

fof(bg_dist_gn_europe_gn_occitanie, axiom,
    gn_europe != gn_occitanie).

fof(bg_dist_gn_europe_gn_paris, axiom,
    gn_europe != gn_paris).

fof(bg_dist_gn_europe_gn_provence_alpes_cote_d_azur, axiom,
    gn_europe != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_europe_gn_strasbourg, axiom,
    gn_europe != gn_strasbourg).

fof(bg_dist_gn_grand_est_gn_ile_de_france, axiom,
    gn_grand_est != gn_ile_de_france).

fof(bg_dist_gn_grand_est_gn_munich, axiom,
    gn_grand_est != gn_munich).

fof(bg_dist_gn_grand_est_gn_nouvelle_aquitaine, axiom,
    gn_grand_est != gn_nouvelle_aquitaine).

fof(bg_dist_gn_grand_est_gn_occitanie, axiom,
    gn_grand_est != gn_occitanie).

fof(bg_dist_gn_grand_est_gn_paris, axiom,
    gn_grand_est != gn_paris).

fof(bg_dist_gn_grand_est_gn_provence_alpes_cote_d_azur, axiom,
    gn_grand_est != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_grand_est_gn_strasbourg, axiom,
    gn_grand_est != gn_strasbourg).

fof(bg_dist_gn_ile_de_france_gn_munich, axiom,
    gn_ile_de_france != gn_munich).

fof(bg_dist_gn_ile_de_france_gn_nouvelle_aquitaine, axiom,
    gn_ile_de_france != gn_nouvelle_aquitaine).

fof(bg_dist_gn_ile_de_france_gn_occitanie, axiom,
    gn_ile_de_france != gn_occitanie).

fof(bg_dist_gn_ile_de_france_gn_paris, axiom,
    gn_ile_de_france != gn_paris).

fof(bg_dist_gn_ile_de_france_gn_provence_alpes_cote_d_azur, axiom,
    gn_ile_de_france != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_ile_de_france_gn_strasbourg, axiom,
    gn_ile_de_france != gn_strasbourg).

fof(bg_dist_gn_munich_gn_nouvelle_aquitaine, axiom,
    gn_munich != gn_nouvelle_aquitaine).

fof(bg_dist_gn_munich_gn_occitanie, axiom,
    gn_munich != gn_occitanie).

fof(bg_dist_gn_munich_gn_paris, axiom,
    gn_munich != gn_paris).

fof(bg_dist_gn_munich_gn_provence_alpes_cote_d_azur, axiom,
    gn_munich != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_munich_gn_strasbourg, axiom,
    gn_munich != gn_strasbourg).

fof(bg_dist_gn_nouvelle_aquitaine_gn_occitanie, axiom,
    gn_nouvelle_aquitaine != gn_occitanie).

fof(bg_dist_gn_nouvelle_aquitaine_gn_paris, axiom,
    gn_nouvelle_aquitaine != gn_paris).

fof(bg_dist_gn_nouvelle_aquitaine_gn_provence_alpes_cote_d_azur, axiom,
    gn_nouvelle_aquitaine != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_nouvelle_aquitaine_gn_strasbourg, axiom,
    gn_nouvelle_aquitaine != gn_strasbourg).

fof(bg_dist_gn_occitanie_gn_paris, axiom,
    gn_occitanie != gn_paris).

fof(bg_dist_gn_occitanie_gn_provence_alpes_cote_d_azur, axiom,
    gn_occitanie != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_occitanie_gn_strasbourg, axiom,
    gn_occitanie != gn_strasbourg).

fof(bg_dist_gn_paris_gn_provence_alpes_cote_d_azur, axiom,
    gn_paris != gn_provence_alpes_cote_d_azur).

fof(bg_dist_gn_paris_gn_strasbourg, axiom,
    gn_paris != gn_strasbourg).

fof(bg_dist_gn_provence_alpes_cote_d_azur_gn_strasbourg, axiom,
    gn_provence_alpes_cote_d_azur != gn_strasbourg).

fof(w_kgc308, axiom,
    ~ ( ( ( kge_leq(gn_germany, gn_germany) & gn_germany = gn_france )
    | kge_leq(gn_france, gn_germany)
    | ( kge_leq(gn_auvergne_rhone_alpes, gn_germany) & gn_auvergne_rhone_alpes = gn_france )
    | ( kge_leq(gn_baden_wuerttemberg, gn_germany) & gn_baden_wuerttemberg = gn_france )
    | ( kge_leq(gn_bayern, gn_germany) & gn_bayern = gn_france )
    | ( kge_leq(gn_berlin, gn_germany) & gn_berlin = gn_france )
    | ( kge_leq(gn_europe, gn_germany) & gn_europe = gn_france )
    | ( kge_leq(gn_grand_est, gn_germany) & gn_grand_est = gn_france )
    | ( kge_leq(gn_ile_de_france, gn_germany) & gn_ile_de_france = gn_france )
    | ( kge_leq(gn_munich, gn_germany) & gn_munich = gn_france )
    | ( kge_leq(gn_nouvelle_aquitaine, gn_germany) & gn_nouvelle_aquitaine = gn_france )
    | ( kge_leq(gn_occitanie, gn_germany) & gn_occitanie = gn_france )
    | ( kge_leq(gn_paris, gn_germany) & gn_paris = gn_france )
    | ( kge_leq(gn_provence_alpes_cote_d_azur, gn_germany) & gn_provence_alpes_cote_d_azur = gn_france )
    | ( kge_leq(gn_strasbourg, gn_germany) & gn_strasbourg = gn_france ) ) )).
%------------------------------------------------------------------------------
