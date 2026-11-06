%------------------------------------------------------------------------------
% File     : KGC006+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in exactly one of France and Germany against use in France only: no use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The versions have the
%            same status.
% English  : A library permits use in exactly one of France and Germany. A
%            researcher's policy commits to use in France. This problem states
%            that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC303-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC303 is Unknown. Its two problems state that some use meets the
%            two policies (KGC005) and that no use does (KGC006); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+5.ax').

fof(w_kgc303, axiom,
    ~ ( ( gn_france != gn_germany
    | ( gn_auvergne_rhone_alpes = gn_france & gn_auvergne_rhone_alpes != gn_germany )
    | ( gn_baden_wuerttemberg = gn_france & gn_baden_wuerttemberg != gn_germany )
    | ( gn_bayern = gn_france & gn_bayern != gn_germany )
    | ( gn_berlin = gn_france & gn_berlin != gn_germany )
    | ( gn_europe = gn_france & gn_europe != gn_germany )
    | ( gn_grand_est = gn_france & gn_grand_est != gn_germany )
    | ( gn_ile_de_france = gn_france & gn_ile_de_france != gn_germany )
    | ( gn_munich = gn_france & gn_munich != gn_germany )
    | ( gn_nouvelle_aquitaine = gn_france & gn_nouvelle_aquitaine != gn_germany )
    | ( gn_occitanie = gn_france & gn_occitanie != gn_germany )
    | ( gn_paris = gn_france & gn_paris != gn_germany )
    | ( gn_provence_alpes_cote_d_azur = gn_france & gn_provence_alpes_cote_d_azur != gn_germany )
    | ( gn_strasbourg = gn_france & gn_strasbourg != gn_germany ) ) )).
%------------------------------------------------------------------------------
