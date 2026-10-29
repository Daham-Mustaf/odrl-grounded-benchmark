%--------------------------------------------------------------------------
% File     : KGC399-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, or(isA PublicBenefit, isA NonCommercialResearch) against eq CommercialResearch (witness condition asserted)
% Version  : 1.0
% English  : A city's traffic data platform permits use for public benefit or non-commercial research, or any narrower purpose. A company commits to use for commercial research.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC399-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc399, axiom,
    ( ( ( kge_leq(dpv_public_benefit, dpv_public_benefit) & dpv_public_benefit = dpv_commercial_research )
| ( kge_leq(dpv_non_commercial_research, dpv_public_benefit) & dpv_non_commercial_research = dpv_commercial_research )
| ( kge_leq(dpv_commercial_research, dpv_public_benefit) & dpv_commercial_research = dpv_commercial_research ) )
| ( ( kge_leq(dpv_public_benefit, dpv_non_commercial_research) & dpv_public_benefit = dpv_commercial_research )
| ( kge_leq(dpv_non_commercial_research, dpv_non_commercial_research) & dpv_non_commercial_research = dpv_commercial_research )
| ( kge_leq(dpv_commercial_research, dpv_non_commercial_research) & dpv_commercial_research = dpv_commercial_research ) ) )).
%--------------------------------------------------------------------------
