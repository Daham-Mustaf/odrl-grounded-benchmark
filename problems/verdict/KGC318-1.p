%--------------------------------------------------------------------------
% File     : KGC318-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, neq dpv:Marketing against eq dpv:ScientificResearch, declared distinct (witness condition asserted)
% Version  : 1.0
% English  : A city's traffic data platform permits use for any purpose other than marketing. A university commits to use for scientific research. Scientific research is declared distinct from marketing.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC318-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').
include('axioms/DPV-dpv-purposes-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_dpv_scientific_research_dpv_marketing, axiom,
    dpv_scientific_research != dpv_marketing).

% --- witness condition asserted ------------------------------------------
fof(w_kgc318, axiom,
    ( ( dpv_marketing != dpv_marketing & dpv_marketing = dpv_scientific_research )
| ( dpv_scientific_research != dpv_marketing & dpv_scientific_research = dpv_scientific_research ) )).
%--------------------------------------------------------------------------
