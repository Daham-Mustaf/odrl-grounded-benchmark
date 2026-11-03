%------------------------------------------------------------------------------
% File     : KGC014+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use within Germany against use in France only: no use meets both
% Version  : Especial.
% English  : As KGC308, with the features that share a parent declared
%            disjoint: nothing lies within both. This problem states that no
%            use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC309-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC309 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC013) and that no use does (KGC014). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+5.ax').

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

fof(w_kgc309, axiom,
    ~ ( kge_leq(gn_france, gn_germany) )).
%------------------------------------------------------------------------------
