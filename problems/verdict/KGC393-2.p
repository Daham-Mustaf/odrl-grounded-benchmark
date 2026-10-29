%--------------------------------------------------------------------------
% File     : KGC393-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isAnyOf {PublicBenefit, NonCommercialResearch} against eq ImproveTransportMobility (witness condition negated)
% Version  : 1.0
% English  : A city's traffic data platform permits use for at least one of public benefit and non-commercial research. A city transport authority commits to improving transport mobility.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC393-2.p
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
fof(w_kgc393, axiom,
    ~ ( ( ( dpv_public_benefit = dpv_improve_transport_mobility
| dpv_non_commercial_research = dpv_improve_transport_mobility
| dpv_improve_transport_mobility = dpv_improve_transport_mobility ) & ( ( dpv_public_benefit = dpv_improve_transport_mobility & ( dpv_public_benefit = dpv_public_benefit
| dpv_public_benefit = dpv_non_commercial_research ) )
| ( dpv_non_commercial_research = dpv_improve_transport_mobility & ( dpv_non_commercial_research = dpv_public_benefit
| dpv_non_commercial_research = dpv_non_commercial_research ) )
| ( dpv_improve_transport_mobility = dpv_improve_transport_mobility & ( dpv_improve_transport_mobility = dpv_public_benefit
| dpv_improve_transport_mobility = dpv_non_commercial_research ) ) ) ) )).
%--------------------------------------------------------------------------
