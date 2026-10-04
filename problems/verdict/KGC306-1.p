%--------------------------------------------------------------------------
% File     : KGC306-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(isPartOf France, isPartOf Germany) against eq France, countries disjoint (witness condition asserted)
% Version  : 1.0
% English  : As KGC305, with France and Germany declared disjoint: nothing lies within both.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC306-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: the two countries declared disjoint.
fof(bg_disj_gn_france_disjoint_gn_germany, axiom,
    ! [X] : ~ ( kge_leq(X, gn_france) & kge_leq(X, gn_germany) )).

% --- witness condition asserted ------------------------------------------
fof(w_kgc306, axiom,
    ( ( ( ( kge_leq(gn_france, gn_france) & gn_france = gn_france )
| ( kge_leq(gn_germany, gn_france) & gn_germany = gn_france ) ) & ( ( ( kge_leq(gn_france, gn_france) & gn_france = gn_france ) & ~ ( kge_leq(gn_france, gn_germany) ) )
| ( ( kge_leq(gn_germany, gn_france) & gn_germany = gn_france ) & ~ ( kge_leq(gn_germany, gn_germany) ) ) ) )
| ( ( ( kge_leq(gn_france, gn_germany) & gn_france = gn_france )
| ( kge_leq(gn_germany, gn_germany) & gn_germany = gn_france ) ) & ( ( ( kge_leq(gn_france, gn_germany) & gn_france = gn_france ) & ~ ( kge_leq(gn_france, gn_france) ) )
| ( ( kge_leq(gn_germany, gn_germany) & gn_germany = gn_france ) & ~ ( kge_leq(gn_germany, gn_france) ) ) ) ) )).
%--------------------------------------------------------------------------
