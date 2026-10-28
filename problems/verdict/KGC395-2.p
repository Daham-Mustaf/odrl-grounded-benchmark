%--------------------------------------------------------------------------
% File     : KGC395-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, or(isA RnD, isA Marketing) against eq ScientificResearch (witness condition negated)
% Version  : 1.0
% English  : A library permits use for any purpose under research and development or under marketing; a researcher commits to scientific research.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC395-2.p
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
fof(w_kgc395, axiom,
    ~ ( ( ( ( kge_leq(dpv_research_and_development, dpv_research_and_development) & dpv_research_and_development = dpv_scientific_research )
| ( kge_leq(dpv_marketing, dpv_research_and_development) & dpv_marketing = dpv_scientific_research )
| ( kge_leq(dpv_scientific_research, dpv_research_and_development) & dpv_scientific_research = dpv_scientific_research ) )
| ( ( kge_leq(dpv_research_and_development, dpv_marketing) & dpv_research_and_development = dpv_scientific_research )
| ( kge_leq(dpv_marketing, dpv_marketing) & dpv_marketing = dpv_scientific_research )
| ( kge_leq(dpv_scientific_research, dpv_marketing) & dpv_scientific_research = dpv_scientific_research ) ) ) )).
%--------------------------------------------------------------------------
