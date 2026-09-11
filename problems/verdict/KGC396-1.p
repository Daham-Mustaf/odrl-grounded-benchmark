%--------------------------------------------------------------------------
% File     : KGC396-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isAnyOf {RnD, Marketing} against isAllOf {RnD, ServiceProvision} (witness condition asserted)
% Version  : 1.0
% English  : A provider permits use for research and development or marketing; a consumer commits to research and development and to service provision, both.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
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
    ( $true & $true & ( ( $true & ( dpv_research_and_development = dpv_research_and_development
| dpv_research_and_development = dpv_marketing ) )
| ( $true & ( dpv_marketing = dpv_research_and_development
| dpv_marketing = dpv_marketing ) )
| ( $true & ( dpv_service_provision = dpv_research_and_development
| dpv_service_provision = dpv_marketing ) ) ) )).
%--------------------------------------------------------------------------
