%------------------------------------------------------------------------------
% File     : KGC003+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use within Europe against use in France only: some use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The versions have the
%            same status.
% English  : A German library permits use within Europe. A French library's
%            policy commits to use in France only. This problem states that
%            some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC302-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC302 is Compatible. Its two problems state that some use meets
%            the two policies (KGC003) and that no use does (KGC004); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+5.ax').

fof(w_kgc302, axiom,
    ( ( kge_leq(gn_europe, gn_europe) & gn_europe = gn_france )
    | kge_leq(gn_france, gn_europe)
    | ( kge_leq(gn_auvergne_rhone_alpes, gn_europe) & gn_auvergne_rhone_alpes = gn_france )
    | ( kge_leq(gn_baden_wuerttemberg, gn_europe) & gn_baden_wuerttemberg = gn_france )
    | ( kge_leq(gn_bayern, gn_europe) & gn_bayern = gn_france )
    | ( kge_leq(gn_berlin, gn_europe) & gn_berlin = gn_france )
    | ( kge_leq(gn_germany, gn_europe) & gn_germany = gn_france )
    | ( kge_leq(gn_grand_est, gn_europe) & gn_grand_est = gn_france )
    | ( kge_leq(gn_ile_de_france, gn_europe) & gn_ile_de_france = gn_france )
    | ( kge_leq(gn_munich, gn_europe) & gn_munich = gn_france )
    | ( kge_leq(gn_nouvelle_aquitaine, gn_europe) & gn_nouvelle_aquitaine = gn_france )
    | ( kge_leq(gn_occitanie, gn_europe) & gn_occitanie = gn_france )
    | ( kge_leq(gn_paris, gn_europe) & gn_paris = gn_france )
    | ( kge_leq(gn_provence_alpes_cote_d_azur, gn_europe) & gn_provence_alpes_cote_d_azur = gn_france )
    | ( kge_leq(gn_strasbourg, gn_europe) & gn_strasbourg = gn_france ) )).
%------------------------------------------------------------------------------
