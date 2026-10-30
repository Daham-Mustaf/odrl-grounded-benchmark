%--------------------------------------------------------------------------
% File     : KGC308-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf Germany against eq France, countries distinct (witness condition negated)
% Version  : 1.0
% English  : A library permits use within Germany. A researcher's policy commits to use in France. France and Germany are declared distinct.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC308-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/geonames-europe/declared, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_gn_germany_gn_france, axiom,
    gn_germany != gn_france).

% --- witness condition negated -------------------------------------------
fof(w_kgc308, axiom,
    ~ ( kge_leq(gn_france, gn_germany) )).
%--------------------------------------------------------------------------
