%--------------------------------------------------------------------------
% File     : KGC388-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, or(isPartOf loc:DE-NW, isPartOf loc:DE-BY) against eq loc:DE-NW (witness condition asserted)
% Version  : 1.0
% English  : A library permits use within North Rhine-Westphalia or within Bavaria. A researcher's policy commits to use in North Rhine-Westphalia.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC388-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc388, axiom,
    ( ( ( kge_leq(loc_de_nw, loc_de_nw) & loc_de_nw = loc_de_nw )
| ( kge_leq(loc_de_by, loc_de_nw) & loc_de_by = loc_de_nw ) )
| ( ( kge_leq(loc_de_nw, loc_de_by) & loc_de_nw = loc_de_nw )
| ( kge_leq(loc_de_by, loc_de_by) & loc_de_by = loc_de_nw ) ) )).
%--------------------------------------------------------------------------
