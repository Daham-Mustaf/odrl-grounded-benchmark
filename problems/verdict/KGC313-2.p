%--------------------------------------------------------------------------
% File     : KGC313-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, eq dpv:Marketing against eq dpv:SR (witness condition negated)
% Version  : 1.0
% English  : Offer (purpose, eq, dpv:Marketing) against request (purpose, eq, dpv:ScientificResearch).  Both denote singletons, and the two constraints are satisfiable together only if the two concepts are the same.  DPV publishes no distinctness, so a model may identify them: Unknown.  The same pair under a background theory declaring the two purposes distinct is Incompatible, which is what makes the declaration visible in the verdict.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC313-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-milestone.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  Two names are not two concepts until something
% says so, and the purposes module says nothing.

% --- witness condition negated -------------------------------------------
fof(w_kgc313, axiom,
    ~ ( ( ( dpv_marketing = dpv_marketing & dpv_marketing = dpv_scientific_research )
| ( dpv_scientific_research = dpv_marketing & dpv_scientific_research = dpv_scientific_research ) ) )).
%--------------------------------------------------------------------------
