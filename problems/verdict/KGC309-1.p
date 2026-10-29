%--------------------------------------------------------------------------
% File     : KGC309-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf Germany against eq France, countries disjoint (witness condition asserted)
% Version  : 1.0
% English  : As KGC308, with the features that share a parent declared disjoint: nothing lies within both.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC309-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: the two countries declared disjoint.
fof(bg_disj_gn_france_disjoint_gn_germany, axiom,
    ! [X] : ~ ( kge_leq(X, gn_france) & kge_leq(X, gn_germany) )).

% --- witness condition asserted ------------------------------------------
fof(w_kgc309, axiom,
    ( ( kge_leq(gn_germany, gn_germany) & gn_germany = gn_france )
| ( kge_leq(gn_france, gn_germany) & gn_france = gn_france ) )).
%--------------------------------------------------------------------------
