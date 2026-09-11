%--------------------------------------------------------------------------
% File     : KGC391-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, hasPart loc:DE-NW against eq loc:DE (witness condition asserted)
% Version  : 1.0
% English  : Use in an area that has North Rhine-Westphalia as a part, against use in Germany. Germany has NRW as a part, on the same assertion as KGC382 read upward. The only up-set operator in the table, and nothing else exercises it.
%           : 
%           : Coverage-motivated: a spatial hasPart clause is rare in practice.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC391-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc391, axiom,
    ( ( kge_leq(loc_de_nw, loc_de_nw) & loc_de_nw = loc_de )
| ( kge_leq(loc_de_nw, loc_de) & loc_de = loc_de ) )).
%--------------------------------------------------------------------------
