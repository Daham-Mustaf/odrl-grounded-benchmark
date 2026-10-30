%--------------------------------------------------------------------------
% File     : KGC335-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, neq loc:DE against eq loc:FR, ISO rule (witness condition negated)
% Version  : 1.0
% English  : A library permits use anywhere except Germany. A researcher's policy commits to use in France. The ISO 3166 rule makes the two countries different places.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC335-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').
include('axioms/LOC-dpvloc-iso.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/dpv-loc/iso, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

% --- witness condition negated -------------------------------------------
fof(w_kgc335, axiom,
    ~ ( loc_fr != loc_de )).
%--------------------------------------------------------------------------
