%--------------------------------------------------------------------------
% File     : KGC305-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(isPartOf France, isPartOf Germany) against eq France, countries distinct (witness condition asserted)
% Version  : 1.0
% English  : A library permits use within exactly one of France and Germany. A researcher's policy commits to use in France. France and Germany are declared distinct.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC305-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: the two countries declared distinct.
fof(bg_dist_gn_france_gn_germany, axiom,
    gn_france != gn_germany).

% --- witness condition asserted ------------------------------------------
fof(w_kgc305, axiom,
    ( ( ( ( kge_leq(gn_france, gn_france) & gn_france = gn_france )
| ( kge_leq(gn_germany, gn_france) & gn_germany = gn_france ) ) & ( ( ( kge_leq(gn_france, gn_france) & gn_france = gn_france ) & ~ ( kge_leq(gn_france, gn_germany) ) )
| ( ( kge_leq(gn_germany, gn_france) & gn_germany = gn_france ) & ~ ( kge_leq(gn_germany, gn_germany) ) ) ) )
| ( ( ( kge_leq(gn_france, gn_germany) & gn_france = gn_france )
| ( kge_leq(gn_germany, gn_germany) & gn_germany = gn_france ) ) & ( ( ( kge_leq(gn_france, gn_germany) & gn_france = gn_france ) & ~ ( kge_leq(gn_france, gn_france) ) )
| ( ( kge_leq(gn_germany, gn_germany) & gn_germany = gn_france ) & ~ ( kge_leq(gn_germany, gn_france) ) ) ) ) )).
%--------------------------------------------------------------------------
