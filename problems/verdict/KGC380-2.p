%--------------------------------------------------------------------------
% File     : KGC380-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf loc:EU against eq loc:BQ, jurisdictional (witness condition negated)
% Version  : 1.0
% English  : A library permits use within the European Union; a researcher requests use in Bonaire, Sint Eustatius and Saba.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC380-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-juris.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc380, axiom,
    ~ ( ( ( kge_leq(loc_eu, loc_eu) & loc_eu = loc_bq )
| ( kge_leq(loc_bq, loc_eu) & loc_bq = loc_bq ) ) )).
%--------------------------------------------------------------------------
