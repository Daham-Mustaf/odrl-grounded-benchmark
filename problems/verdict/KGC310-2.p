%--------------------------------------------------------------------------
% File     : KGC310-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:R&D against eq dpv:SR (witness condition negated)
% Version  : 1.0
% English  : Offer (purpose, isA, dpv:ResearchAndDevelopment) against request (purpose, eq, dpv:ScientificResearch).  The vocabulary places the requested purpose under the offered one directly, so the witness holds in every model and the verdict is Compatible.  The refutation should cite one resource premise.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC310-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-milestone.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  The purposes module publishes no disjointness
% and no distinctness, and the parties declare none.

% --- witness condition negated -------------------------------------------
fof(w_kgc310, axiom,
    ~ ( ( ( kge_leq(dpv_research_and_development, dpv_research_and_development) & dpv_research_and_development = dpv_scientific_research )
| ( kge_leq(dpv_scientific_research,  dpv_research_and_development) & dpv_scientific_research  = dpv_scientific_research  ) ) )).
%--------------------------------------------------------------------------
