%--------------------------------------------------------------------------
% File     : KGC390-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, xone(eq loc:DE-NW, eq loc:DE-BY) against eq loc:DE-NW, ISO rule (witness condition asserted)
% Version  : 1.0
% English  : KGC389 under the ISO rule: the two Laender differ, the negated literal holds, and the verdict is Compatible. The only place in the suite where a declaration yields a positive verdict through a negated literal.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC390-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').
include('axioms/LOC-dpvloc-iso.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: instances of the ISO 3166 uniqueness rule,
% stated in LOC-dpvloc-iso.ax and instantiated here.

fof(bg_dist_loc_de_nw_loc_de_by, axiom,
    loc_de_nw != loc_de_by).

% --- witness condition asserted ------------------------------------------
fof(w_kgc390, axiom,
    ( ( ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_nw )
| ( loc_de_by = loc_de_nw & loc_de_by = loc_de_nw ) ) & ( ( ( loc_de_nw = loc_de_nw & loc_de_nw = loc_de_nw ) & ~ ( loc_de_nw = loc_de_by ) )
| ( ( loc_de_by = loc_de_nw & loc_de_by = loc_de_nw ) & ~ ( loc_de_by = loc_de_by ) ) ) )
| ( ( ( loc_de_nw = loc_de_by & loc_de_nw = loc_de_nw )
| ( loc_de_by = loc_de_by & loc_de_by = loc_de_nw ) ) & ( ( ( loc_de_nw = loc_de_by & loc_de_nw = loc_de_nw ) & ~ ( loc_de_nw = loc_de_nw ) )
| ( ( loc_de_by = loc_de_by & loc_de_by = loc_de_nw ) & ~ ( loc_de_by = loc_de_nw ) ) ) ) )).
%--------------------------------------------------------------------------
