%--------------------------------------------------------------------------
% File     : KGC319-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, xone(isA CommercialPurpose, isA NonCommercialPurpose) against eq NonCommercialResearch (witness condition negated)
% Version  : 1.0
% English  : A city's traffic data platform permits use for exactly one of commercial and non-commercial purposes. A university research group commits to use for non-commercial research.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC319-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc319, axiom,
    ~ ( ( ( ( ( kge_leq(dpv_commercial_purpose, dpv_commercial_purpose) & dpv_commercial_purpose = dpv_non_commercial_research )
| ( kge_leq(dpv_non_commercial_purpose, dpv_commercial_purpose) & dpv_non_commercial_purpose = dpv_non_commercial_research )
| ( kge_leq(dpv_non_commercial_research, dpv_commercial_purpose) & dpv_non_commercial_research = dpv_non_commercial_research ) ) & ( ( ( kge_leq(dpv_commercial_purpose, dpv_commercial_purpose) & dpv_commercial_purpose = dpv_non_commercial_research ) & ~ ( kge_leq(dpv_commercial_purpose, dpv_non_commercial_purpose) ) )
| ( ( kge_leq(dpv_non_commercial_purpose, dpv_commercial_purpose) & dpv_non_commercial_purpose = dpv_non_commercial_research ) & ~ ( kge_leq(dpv_non_commercial_purpose, dpv_non_commercial_purpose) ) )
| ( ( kge_leq(dpv_non_commercial_research, dpv_commercial_purpose) & dpv_non_commercial_research = dpv_non_commercial_research ) & ~ ( kge_leq(dpv_non_commercial_research, dpv_non_commercial_purpose) ) ) ) )
| ( ( ( kge_leq(dpv_commercial_purpose, dpv_non_commercial_purpose) & dpv_commercial_purpose = dpv_non_commercial_research )
| ( kge_leq(dpv_non_commercial_purpose, dpv_non_commercial_purpose) & dpv_non_commercial_purpose = dpv_non_commercial_research )
| ( kge_leq(dpv_non_commercial_research, dpv_non_commercial_purpose) & dpv_non_commercial_research = dpv_non_commercial_research ) ) & ( ( ( kge_leq(dpv_commercial_purpose, dpv_non_commercial_purpose) & dpv_commercial_purpose = dpv_non_commercial_research ) & ~ ( kge_leq(dpv_commercial_purpose, dpv_commercial_purpose) ) )
| ( ( kge_leq(dpv_non_commercial_purpose, dpv_non_commercial_purpose) & dpv_non_commercial_purpose = dpv_non_commercial_research ) & ~ ( kge_leq(dpv_non_commercial_purpose, dpv_commercial_purpose) ) )
| ( ( kge_leq(dpv_non_commercial_research, dpv_non_commercial_purpose) & dpv_non_commercial_research = dpv_non_commercial_research ) & ~ ( kge_leq(dpv_non_commercial_research, dpv_commercial_purpose) ) ) ) ) ) )).
%--------------------------------------------------------------------------
