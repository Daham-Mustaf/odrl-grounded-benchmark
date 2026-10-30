%--------------------------------------------------------------------------
% File     : KGC304-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(eq France, eq Germany) against eq France, countries distinct (witness condition negated)
% Version  : 1.0
% English  : As KGC303, with France and Germany declared distinct.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC304-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/geonames-europe/declared, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_gn_france_gn_germany, axiom,
    gn_france != gn_germany).

% --- witness condition negated -------------------------------------------
fof(w_kgc304, axiom,
    ~ ( gn_france != gn_germany )).
%--------------------------------------------------------------------------
