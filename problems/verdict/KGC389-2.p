%--------------------------------------------------------------------------
% File     : KGC389-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(eq loc:DE-NW, eq loc:DE-BY) against eq loc:DE-NW (witness condition negated)
% Version  : 1.0
% English  : A library permits use in exactly one of North Rhine-Westphalia and Bavaria. A researcher's policy commits to use in North Rhine-Westphalia.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC389-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc389, axiom,
    ~ ( ( ( ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_nw )
| ( loc_de_by = loc_de_nw & loc_de_by = loc_de_nw ) ) & ( ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_nw ) & ~ ( loc_de_nw = loc_de_by ) )
| ( ( loc_de_by = loc_de_nw & loc_de_by = loc_de_nw ) & ~ ( loc_de_by = loc_de_by ) ) ) )
| ( ( ( loc_de_nw = loc_de_by & loc_de_nw = loc_de_nw )
| ( loc_de_by = loc_de_by & loc_de_by = loc_de_nw ) ) & ( ( ( loc_de_nw = loc_de_by & loc_de_nw = loc_de_nw ) & ~ ( loc_de_nw = loc_de_nw ) )
| ( ( loc_de_by = loc_de_by & loc_de_by = loc_de_nw ) & ~ ( loc_de_by = loc_de_nw ) ) ) ) ) )).
%--------------------------------------------------------------------------
