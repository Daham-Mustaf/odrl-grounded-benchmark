%--------------------------------------------------------------------------
% File     : KGC396-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA PublicBenefit against isAllOf {DataAltruism, ImproveTransportMobility} (witness condition asserted)
% Version  : 1.0
% English  : A city's traffic data platform permits use for public benefit or any narrower purpose. A city transport authority commits to data altruism and improving transport mobility together.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC396-1.p
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
fof(w_kgc396, axiom,
    ( kge_leq(dpv_data_altruism, dpv_public_benefit) & kge_leq(dpv_improve_transport_mobility, dpv_public_benefit) )).
%--------------------------------------------------------------------------
