%--------------------------------------------------------------------------
% File     : KGC334-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, eq loc:DE against eq loc:FR, under the ISO 3166 uniqueness rule (witness condition negated)
% Version  : 1.0
% English  : A library permits use in Germany; a researcher requests use in France.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC334-2.p
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
% Background theory: one instance of the ISO 3166 uniqueness rule.
%
% The rule is stated in LOC-dpvloc-iso.ax and ranges over 249 areas.  It is
% instantiated here rather than expanded there: a refutation should cite the
% inequation it used, not one term standing for thirty thousand.
fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

% --- witness condition negated -------------------------------------------
fof(w_kgc334, axiom,
    ~ ( ( ( loc_de = loc_de & loc_de = loc_fr )
| ( loc_fr = loc_de & loc_fr = loc_fr ) ) )).
%--------------------------------------------------------------------------
