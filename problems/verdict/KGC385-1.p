%--------------------------------------------------------------------------
% File     : KGC385-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, eq loc:DE-NW against eq loc:DE-BY, ISO rule (witness condition asserted)
% Version  : 1.0
% English  : KGC384 under the ISO 3166-2 rule, one code per subdivision within a country. The two Laender are then distinct areas, no use satisfies both sides, and the verdict is Incompatible on the parties' rule, withdrawable by dropping it.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC385-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').
include('axioms/LOC-dpvloc-iso.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: instances of the ISO 3166 uniqueness rule,
% stated in LOC-dpvloc-iso.ax and instantiated here.

fof(bg_dist_loc_de_nw_loc_de_by, axiom,
    loc_de_nw != loc_de_by).

% --- witness condition asserted ------------------------------------------
fof(w_kgc385, axiom,
    ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_by )
| ( loc_de_by = loc_de_nw & loc_de_by = loc_de_by ) )).
%--------------------------------------------------------------------------
