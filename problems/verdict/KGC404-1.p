%--------------------------------------------------------------------------
% File     : KGC404-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:R&D against isA dpv:SR (witness condition asserted)
% Version  : 1.0
% English  : A city's traffic data platform permits use for research and development purposes. A university commits to use for scientific research purposes.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC404-1.p
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
fof(w_kgc404, axiom,
    ( ( kge_leq(dpv_research_and_development, dpv_research_and_development) & kge_leq(dpv_research_and_development, dpv_scientific_research) )
| ( kge_leq(dpv_scientific_research, dpv_research_and_development) & kge_leq(dpv_scientific_research, dpv_scientific_research) ) )).
%--------------------------------------------------------------------------
