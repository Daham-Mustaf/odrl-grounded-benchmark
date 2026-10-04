%--------------------------------------------------------------------------
% File     : KGC382-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf loc:DE against eq loc:DE-NW (witness condition negated)
% Version  : 1.0
% English  : A library permits use within Germany. A researcher's policy commits to use in North Rhine-Westphalia.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC382-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc382, axiom,
    ~ ( ( ( kge_leq(loc_de, loc_de) & loc_de = loc_de_nw )
| ( kge_leq(loc_de_nw, loc_de) & loc_de_nw = loc_de_nw ) ) )).
%--------------------------------------------------------------------------
