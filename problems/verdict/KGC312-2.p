%--------------------------------------------------------------------------
% File     : KGC312-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:NCP against eq dpv:SR (witness condition negated)
% Version  : 1.0
% English  : Offer (purpose, isA, dpv:NonCommercialPurpose) against request (purpose, eq, dpv:ScientificResearch).  DPV places scientific research under research and development only, and publishes no disjointness, so a model may place it under non-commercial purpose and a model may not.  Unknown.  DPV does publish dpv:NonCommercialResearch under both parents, so the silence here is a decision rather than an omission.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC312-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-milestone.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  Asserting that the two concepts are unrelated
% would be the closed-world reading this paper rejects.

% --- witness condition negated -------------------------------------------
fof(w_kgc312, axiom,
    ~ ( ( ( kge_leq(dpv_non_commercial_purpose, dpv_non_commercial_purpose) & dpv_non_commercial_purpose = dpv_scientific_research )
| ( kge_leq(dpv_scientific_research,  dpv_non_commercial_purpose) & dpv_scientific_research  = dpv_scientific_research  ) ) )).
%--------------------------------------------------------------------------
