%--------------------------------------------------------------------------
% File     : KGC396-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isAnyOf {RnD, Marketing} against isAllOf {RnD, ServiceProvision} (witness condition negated)
% Version  : 1.0
% English  : A library permits use for research and development or marketing. A researcher's policy commits to both research and development and service provision.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC396-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc396, axiom,
    ~ ( ( $true & $true & ( ( $true & ( dpv_research_and_development = dpv_research_and_development
| dpv_research_and_development = dpv_marketing ) )
| ( $true & ( dpv_marketing = dpv_research_and_development
| dpv_marketing = dpv_marketing ) )
| ( $true & ( dpv_service_provision = dpv_research_and_development
| dpv_service_provision = dpv_marketing ) ) ) ) )).
%--------------------------------------------------------------------------
