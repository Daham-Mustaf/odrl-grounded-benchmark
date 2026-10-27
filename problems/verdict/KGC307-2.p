%--------------------------------------------------------------------------
% File     : KGC307-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(eq France, isAllOf (France Germany)) against eq France, countries distinct (witness condition negated)
% Version  : 1.0
% English  : A library permits use in exactly one of two ways: in France alone, or in both France and Germany. A researcher's policy commits to use in France. France and Germany are declared distinct.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC307-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: the two countries declared distinct.
fof(bg_dist_gn_france_gn_germany, axiom,
    gn_france != gn_germany).

% --- witness condition negated -------------------------------------------
fof(w_kgc307, axiom,
    ~ ( ( ( ( gn_france = gn_france & gn_france != gn_france & gn_france = gn_france )
| ( gn_germany = gn_france & gn_germany != gn_france & gn_germany = gn_france ) )
| ( ( gn_france = gn_france & gn_france != gn_germany & gn_france = gn_france )
| ( gn_germany = gn_france & gn_germany != gn_germany & gn_germany = gn_france ) )
| ( gn_france = gn_france & gn_germany = gn_france & ( gn_france = gn_france
| gn_germany = gn_france ) & ( ( gn_france = gn_france & ~ ( gn_france = gn_france ) )
| ( gn_germany = gn_france & ~ ( gn_germany = gn_france ) ) ) ) ) )).
%--------------------------------------------------------------------------
