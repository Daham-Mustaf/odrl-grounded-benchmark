%--------------------------------------------------------------------------
% File     : KGC330-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf loc:NL against eq loc:BQ (witness condition negated)
% Version  : 1.0
% English  : A library permits use within the Netherlands; a researcher asks to use the material in Bonaire. DPV places Bonaire within the Netherlands.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC330-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  The extension asserts no disjointness between
% places and no distinctness between the codes it lists.

% --- witness condition negated -------------------------------------------
fof(w_kgc330, axiom,
    ~ ( ( ( kge_leq(loc_nl, loc_nl) & loc_nl = loc_bq )
| ( kge_leq(loc_bq, loc_nl) & loc_bq = loc_bq ) ) )).
%--------------------------------------------------------------------------
