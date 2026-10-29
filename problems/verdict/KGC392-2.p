%--------------------------------------------------------------------------
% File     : KGC392-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isNoneOf {loc:DE} against eq loc:DE-BY, ISO rule (witness condition negated)
% Version  : 1.0
% English  : A library permits use anywhere except Germany. A researcher's policy commits to use in Bavaria, a state of Germany.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC392-2.p
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
% Declarations: instances of the ISO 3166 distinctness rule,
% stated in LOC-dpvloc-iso.ax and instantiated here.

fof(bg_dist_loc_de_by_loc_de, axiom,
    loc_de_by != loc_de).

% --- witness condition negated -------------------------------------------
fof(w_kgc392, axiom,
    ~ ( ( ( loc_de != loc_de & loc_de = loc_de_by )
| ( loc_de_by != loc_de & loc_de_by = loc_de_by ) ) )).
%--------------------------------------------------------------------------
