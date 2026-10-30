%--------------------------------------------------------------------------
% File     : KGC394-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isAnyOf {PublicBenefit, NonCommercialResearch} against eq ImproveTransportMobility, declared distinct (witness condition asserted)
% Version  : 1.0
% English  : As KGC393, with improving transport mobility declared distinct from both purposes the first policy names.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC394-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').
include('axioms/DPV-dpv-purposes-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/dpv-purposes/declared, over every pair of the
% witness's candidates it states (3).

fof(bg_dist_dpv_public_benefit_dpv_non_commercial_research, axiom,
    dpv_public_benefit != dpv_non_commercial_research).

fof(bg_dist_dpv_public_benefit_dpv_improve_transport_mobility, axiom,
    dpv_public_benefit != dpv_improve_transport_mobility).

fof(bg_dist_dpv_non_commercial_research_dpv_improve_transport_mobility, axiom,
    dpv_non_commercial_research != dpv_improve_transport_mobility).

% --- witness condition asserted ------------------------------------------
fof(w_kgc394, axiom,
    ( dpv_public_benefit = dpv_improve_transport_mobility
| dpv_non_commercial_research = dpv_improve_transport_mobility )).
%--------------------------------------------------------------------------
