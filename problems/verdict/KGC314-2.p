%--------------------------------------------------------------------------
% File     : KGC314-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, eq dpv:ScientificResearch against eq dpv:Marketing, under a declared distinctness (witness condition negated)
% Version  : 1.0
% English  : As KGC313, with scientific research and marketing declared distinct.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC314-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').
include('axioms/DPV-dpv-purposes-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_dpv_marketing_dpv_scientific_research, axiom,
    dpv_marketing != dpv_scientific_research).

% --- witness condition negated -------------------------------------------
fof(w_kgc314, axiom,
    ~ ( ( ( dpv_scientific_research = dpv_scientific_research & dpv_scientific_research = dpv_marketing )
| ( dpv_marketing = dpv_scientific_research & dpv_marketing = dpv_marketing ) ) )).
%--------------------------------------------------------------------------
