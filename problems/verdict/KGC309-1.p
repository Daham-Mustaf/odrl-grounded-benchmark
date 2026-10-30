%--------------------------------------------------------------------------
% File     : KGC309-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf Germany against eq France, countries disjoint (witness condition asserted)
% Version  : 1.0
% English  : As KGC308, with the features that share a parent declared disjoint: nothing lies within both.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC309-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/geonames-europe/siblings, over every pair of the
% witness's candidates it states (19).

fof(bg_disj_gn_grand_est_disjoint_gn_nouvelle_aquitaine, axiom,
    ! [X] : ~ ( kge_leq(X, gn_grand_est) & kge_leq(X, gn_nouvelle_aquitaine) )).

fof(bg_disj_gn_grand_est_disjoint_gn_occitanie, axiom,
    ! [X] : ~ ( kge_leq(X, gn_grand_est) & kge_leq(X, gn_occitanie) )).

fof(bg_disj_gn_grand_est_disjoint_gn_auvergne_rhone_alpes, axiom,
    ! [X] : ~ ( kge_leq(X, gn_grand_est) & kge_leq(X, gn_auvergne_rhone_alpes) )).

fof(bg_disj_gn_grand_est_disjoint_gn_provence_alpes_cote_d_azur, axiom,
    ! [X] : ~ ( kge_leq(X, gn_grand_est) & kge_leq(X, gn_provence_alpes_cote_d_azur) )).

fof(bg_disj_gn_occitanie_disjoint_gn_nouvelle_aquitaine, axiom,
    ! [X] : ~ ( kge_leq(X, gn_occitanie) & kge_leq(X, gn_nouvelle_aquitaine) )).

fof(bg_disj_gn_occitanie_disjoint_gn_auvergne_rhone_alpes, axiom,
    ! [X] : ~ ( kge_leq(X, gn_occitanie) & kge_leq(X, gn_auvergne_rhone_alpes) )).

fof(bg_disj_gn_auvergne_rhone_alpes_disjoint_gn_nouvelle_aquitaine, axiom,
    ! [X] : ~ ( kge_leq(X, gn_auvergne_rhone_alpes) & kge_leq(X, gn_nouvelle_aquitaine) )).

fof(bg_disj_gn_berlin_disjoint_gn_baden_wuerttemberg, axiom,
    ! [X] : ~ ( kge_leq(X, gn_berlin) & kge_leq(X, gn_baden_wuerttemberg) )).

fof(bg_disj_gn_bayern_disjoint_gn_berlin, axiom,
    ! [X] : ~ ( kge_leq(X, gn_bayern) & kge_leq(X, gn_berlin) )).

fof(bg_disj_gn_bayern_disjoint_gn_baden_wuerttemberg, axiom,
    ! [X] : ~ ( kge_leq(X, gn_bayern) & kge_leq(X, gn_baden_wuerttemberg) )).

fof(bg_disj_gn_provence_alpes_cote_d_azur_disjoint_gn_nouvelle_aquitaine, axiom,
    ! [X] : ~ ( kge_leq(X, gn_provence_alpes_cote_d_azur) & kge_leq(X, gn_nouvelle_aquitaine) )).

fof(bg_disj_gn_provence_alpes_cote_d_azur_disjoint_gn_occitanie, axiom,
    ! [X] : ~ ( kge_leq(X, gn_provence_alpes_cote_d_azur) & kge_leq(X, gn_occitanie) )).

fof(bg_disj_gn_provence_alpes_cote_d_azur_disjoint_gn_auvergne_rhone_alpes, axiom,
    ! [X] : ~ ( kge_leq(X, gn_provence_alpes_cote_d_azur) & kge_leq(X, gn_auvergne_rhone_alpes) )).

fof(bg_disj_gn_ile_de_france_disjoint_gn_nouvelle_aquitaine, axiom,
    ! [X] : ~ ( kge_leq(X, gn_ile_de_france) & kge_leq(X, gn_nouvelle_aquitaine) )).

fof(bg_disj_gn_ile_de_france_disjoint_gn_grand_est, axiom,
    ! [X] : ~ ( kge_leq(X, gn_ile_de_france) & kge_leq(X, gn_grand_est) )).

fof(bg_disj_gn_ile_de_france_disjoint_gn_occitanie, axiom,
    ! [X] : ~ ( kge_leq(X, gn_ile_de_france) & kge_leq(X, gn_occitanie) )).

fof(bg_disj_gn_ile_de_france_disjoint_gn_auvergne_rhone_alpes, axiom,
    ! [X] : ~ ( kge_leq(X, gn_ile_de_france) & kge_leq(X, gn_auvergne_rhone_alpes) )).

fof(bg_disj_gn_ile_de_france_disjoint_gn_provence_alpes_cote_d_azur, axiom,
    ! [X] : ~ ( kge_leq(X, gn_ile_de_france) & kge_leq(X, gn_provence_alpes_cote_d_azur) )).

fof(bg_disj_gn_france_disjoint_gn_germany, axiom,
    ! [X] : ~ ( kge_leq(X, gn_france) & kge_leq(X, gn_germany) )).

% --- witness condition asserted ------------------------------------------
fof(w_kgc309, axiom,
    kge_leq(gn_france, gn_germany)).
%--------------------------------------------------------------------------
