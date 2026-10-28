%--------------------------------------------------------------------------
% File     : KGC336-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isAnyOf {loc:DE, loc:FR} against eq loc:DE-BY, ISO rule (witness condition negated)
% Version  : 1.0
% English  : A library permits use in at least one of Germany and France. A researcher's policy commits to use in Bavaria. The ISO 3166 rule makes Bavaria a different place from both countries.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
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
% Declarations: instances of the ISO 3166 uniqueness rule,
% stated in LOC-dpvloc-iso.ax and instantiated here.

fof(bg_dist_loc_de_by_loc_de, axiom,
    loc_de_by != loc_de).
fof(bg_dist_loc_de_by_loc_fr, axiom,
    loc_de_by != loc_fr).

% --- witness condition negated -------------------------------------------
fof(w_kgc336, axiom,
    ~ ( ( ( loc_de = loc_de_by
| loc_fr = loc_de_by
| loc_de_by = loc_de_by ) & ( ( loc_de = loc_de_by & ( loc_de = loc_de
| loc_de = loc_fr ) )
| ( loc_fr = loc_de_by & ( loc_fr = loc_de
| loc_fr = loc_fr ) )
| ( loc_de_by = loc_de_by & ( loc_de_by = loc_de
| loc_de_by = loc_fr ) ) ) ) )).
%--------------------------------------------------------------------------
