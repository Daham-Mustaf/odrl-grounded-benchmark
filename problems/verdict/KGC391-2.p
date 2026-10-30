%--------------------------------------------------------------------------
% File     : KGC391-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, hasPart loc:DE-NW against eq loc:DE (witness condition negated)
% Version  : 1.0
% English  : A library, bound by a digitisation grant from North Rhine-Westphalia, permits use only in an area that covers all of the state. A researcher's policy commits to use in Germany, which covers the state.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC391-2.p
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
fof(w_kgc391, axiom,
    ~ ( kge_leq(loc_de_nw, loc_de) )).
%--------------------------------------------------------------------------
