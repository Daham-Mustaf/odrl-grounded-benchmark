%--------------------------------------------------------------------------
% File     : KGC330-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf loc:NL against eq loc:BQ (witness condition asserted)
% Version  : 1.0
% English  : Offer (spatial, isPartOf, loc:NL) against request (spatial, eq, loc:BQ).  The extension places Bonaire, Sint Eustatius and Saba within the Netherlands, so the witness holds in every model and the verdict is Compatible.  The refutation cites one resource premise and no transitivity: under the geographic reading the order is two levels deep and this is one step of it.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC330-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  The extension asserts no disjointness between
% places and no distinctness between the codes it lists.

% --- witness condition asserted ------------------------------------------
fof(w_kgc330, axiom,
    ( ( kge_leq(loc_nl, loc_nl) & loc_nl = loc_bq )
| ( kge_leq(loc_bq, loc_nl) & loc_bq = loc_bq ) )).
%--------------------------------------------------------------------------
