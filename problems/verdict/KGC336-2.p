%--------------------------------------------------------------------------
% File     : KGC336-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isAnyOf {loc:DE, loc:FR} against eq loc:DE-BY, ISO rule (witness condition negated)
% Version  : 1.0
% English  : A library permits use in at least one of Germany and France. A researcher's policy commits to use in Bavaria. The ISO 3166 rule makes Bavaria a different place from both countries.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC336-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').
include('axioms/LOC-dpvloc-iso.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/dpv-loc/iso, over every pair of the
% witness's candidates it states (3).

fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

fof(bg_dist_loc_de_loc_de_by, axiom,
    loc_de != loc_de_by).

fof(bg_dist_loc_fr_loc_de_by, axiom,
    loc_fr != loc_de_by).

% --- witness condition negated -------------------------------------------
fof(w_kgc336, axiom,
    ~ ( ( loc_de = loc_de_by
| loc_fr = loc_de_by ) )).
%--------------------------------------------------------------------------
