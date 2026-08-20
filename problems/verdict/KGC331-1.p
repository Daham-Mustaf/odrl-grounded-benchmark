%--------------------------------------------------------------------------
% File     : KGC331-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf loc:EU against eq loc:DE (witness condition asserted)
% Version  : 1.0
% English  : Offer (spatial, isPartOf, loc:EU) against request (spatial, eq, loc:DE), under the jurisdictional reading.  Germany is a member of the European Union, the reading takes membership as the order, and the verdict is Compatible on one assertion.  Under the geographic reading the same constraints are well sorted and have no verdict: that reading takes only containment, loc:EU is not among its concepts, and the offer's right operand grounds to nothing.  The difference is the profile and nothing else.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC331-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-juris.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.
% Resource: the jurisdictional reading, containment together with union
% membership.  Under the geographic reading loc:EU is not a concept and this
% problem does not arise.

% --- witness condition asserted ------------------------------------------
fof(w_kgc331, axiom,
    ( ( kge_leq(loc_eu, loc_eu) & loc_eu = loc_de )
| ( kge_leq(loc_de, loc_eu) & loc_de = loc_de ) )).
%--------------------------------------------------------------------------
