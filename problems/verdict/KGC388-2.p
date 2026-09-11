%--------------------------------------------------------------------------
% File     : KGC388-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, or(isPartOf loc:DE-NW, isPartOf loc:DE-BY) against eq loc:DE-NW (witness condition negated)
% Version  : 1.0
% English  : Use within North Rhine-Westphalia or within Bavaria against use in North Rhine-Westphalia. Compatible through the first disjunct, by reflexivity. The first verdict problem in the suite with a Logical Constraint; the refutation must cite the disjunct it used, which tests that attribution follows the branch.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC388-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc388, axiom,
    ~ ( ( ( ( kge_leq(loc_de_nw, loc_de_nw) & loc_de_nw = loc_de_nw )
| ( kge_leq(loc_de_by, loc_de_nw) & loc_de_by = loc_de_nw ) )
| ( ( kge_leq(loc_de_nw, loc_de_by) & loc_de_nw = loc_de_nw )
| ( kge_leq(loc_de_by, loc_de_by) & loc_de_by = loc_de_nw ) ) ) )).
%--------------------------------------------------------------------------
