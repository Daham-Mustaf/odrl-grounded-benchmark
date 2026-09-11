%--------------------------------------------------------------------------
% File     : KGC384-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, eq loc:DE-NW against eq loc:DE-BY (witness condition negated)
% Version  : 1.0
% English  : Use in North Rhine-Westphalia against use in Bavaria. Both sides name one Land, and both can be satisfied only if the two are one place. The file relates the Laender to DE and to nothing sideways, and separates nothing: Unknown.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC384-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc384, axiom,
    ~ ( ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_by )
| ( loc_de_by = loc_de_nw & loc_de_by = loc_de_by ) ) )).
%--------------------------------------------------------------------------
