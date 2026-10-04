%--------------------------------------------------------------------------
% File     : KGC303-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(eq France, eq Germany) against eq France (witness condition asserted)
% Version  : 1.0
% English  : A library permits use in exactly one of France and Germany. A researcher's policy commits to use in France.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC303-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc303, axiom,
    ( ( ( ( gn_france = gn_france & gn_france = gn_france )
| ( gn_germany = gn_france & gn_germany = gn_france ) ) & ( ( ( gn_france = gn_france & gn_france = gn_france ) & ~ ( gn_france = gn_germany ) )
| ( ( gn_germany = gn_france & gn_germany = gn_france ) & ~ ( gn_germany = gn_germany ) ) ) )
| ( ( ( gn_france = gn_germany & gn_france = gn_france )
| ( gn_germany = gn_germany & gn_germany = gn_france ) ) & ( ( ( gn_france = gn_germany & gn_france = gn_france ) & ~ ( gn_france = gn_france ) )
| ( ( gn_germany = gn_germany & gn_germany = gn_france ) & ~ ( gn_germany = gn_france ) ) ) ) )).
%--------------------------------------------------------------------------
