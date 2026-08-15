%--------------------------------------------------------------------------
% File     : KGC301-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:NCP against eq dpv:SR (witness condition asserted)
% Version  : 1.0
% English  : Offer (purpose, isA, dpv:NonCommercialPurpose) against request (purpose, eq, dpv:ScientificResearch).  The vocabulary neither places one under the other nor separates them, so both queries are satisfiable and the verdict is Unknown.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL. Under submission.
% Source   : TODO repository URL
% Authors  : TODO Author Names
% Names    : KGC301-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% The vocabulary is silent on the two concepts.  Nothing is asserted here:
% asserting a negative would be the closed-world reading this paper rejects.

% --- witness condition asserted ------------------------------------------
fof(kgc301_w, axiom,
    ( ( kge_leq(dpv_non_commercial_purpose, dpv_non_commercial_purpose) & dpv_non_commercial_purpose = dpv_scientific_research )
| ( kge_leq(dpv_scientific_research,  dpv_non_commercial_purpose) & dpv_scientific_research  = dpv_scientific_research  ) )).
%--------------------------------------------------------------------------
