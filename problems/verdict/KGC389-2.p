%--------------------------------------------------------------------------
% File     : KGC389-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(eq loc:DE-NW, eq loc:DE-BY) against eq loc:DE-NW (witness condition negated)
% Version  : 1.0
% English  : Exactly one of North Rhine-Westphalia and Bavaria, against North Rhine-Westphalia. Expanded, the live alternative is NRW and not Bavaria, which needs the two to differ; the file does not say so: Unknown as published.
%           : 
%           : A construction: rights managers rarely write exactly-one-region; the case exists to exercise the negated literal of the xone expansion.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC389-2.p
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
fof(w_kgc389, axiom,
    ~ ( ( ( ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_nw )
| ( loc_de_by = loc_de_nw & loc_de_by = loc_de_nw ) ) & ( ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_nw ) & ~ ( loc_de_nw = loc_de_by ) )
| ( ( loc_de_by = loc_de_nw & loc_de_by = loc_de_nw ) & ~ ( loc_de_by = loc_de_by ) ) ) )
| ( ( ( loc_de_nw = loc_de_by & loc_de_nw = loc_de_nw )
| ( loc_de_by = loc_de_by & loc_de_by = loc_de_nw ) ) & ( ( ( loc_de_nw = loc_de_by & loc_de_nw = loc_de_nw ) & ~ ( loc_de_nw = loc_de_nw ) )
| ( ( loc_de_by = loc_de_by & loc_de_by = loc_de_nw ) & ~ ( loc_de_by = loc_de_nw ) ) ) ) ) )).
%--------------------------------------------------------------------------
