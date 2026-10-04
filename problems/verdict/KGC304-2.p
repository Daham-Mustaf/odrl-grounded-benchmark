%--------------------------------------------------------------------------
% File     : KGC304-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(eq France, eq Germany) against eq France, countries distinct (witness condition negated)
% Version  : 1.0
% English  : As KGC303, with France and Germany declared distinct.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC304-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: the two countries declared distinct.
fof(bg_dist_gn_france_gn_germany, axiom,
    gn_france != gn_germany).

% --- witness condition negated -------------------------------------------
fof(w_kgc304, axiom,
    ~ ( ( ( ( ( gn_france = gn_france & gn_france = gn_france )
| ( gn_germany = gn_france & gn_germany = gn_france ) ) & ( ( ( gn_france = gn_france & gn_france = gn_france ) & ~ ( gn_france = gn_germany ) )
| ( ( gn_germany = gn_france & gn_germany = gn_france ) & ~ ( gn_germany = gn_germany ) ) ) )
| ( ( ( gn_france = gn_germany & gn_france = gn_france )
| ( gn_germany = gn_germany & gn_germany = gn_france ) ) & ( ( ( gn_france = gn_germany & gn_france = gn_france ) & ~ ( gn_france = gn_france ) )
| ( ( gn_germany = gn_germany & gn_germany = gn_france ) & ~ ( gn_germany = gn_france ) ) ) ) ) )).
%--------------------------------------------------------------------------
