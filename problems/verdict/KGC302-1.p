%--------------------------------------------------------------------------
% File     : KGC302-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf gn:Europe against eq gn:France (witness condition asserted)
% Version  : 1.0
% English  : Offer (spatial, isPartOf, gn:Europe) against request (spatial, eq, gn:France).  The gazetteer places France within Europe, so the witness condition holds in every model and the negated query is unsatisfiable.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC302-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Resource: the gazetteer places France within Europe.
fof(res_france_within_europe, axiom,
    kge_leq(gn_france, gn_europe)).

% --- witness condition asserted ------------------------------------------
fof(w_kgc302, axiom,
    ( ( kge_leq(gn_europe, gn_europe) & gn_europe = gn_france )
| ( kge_leq(gn_france, gn_europe) & gn_france = gn_france ) )).
%--------------------------------------------------------------------------
