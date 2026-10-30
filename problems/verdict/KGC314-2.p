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
% Declarations: https://w3id.org/odrl-kb/dpv-purposes/declared, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_dpv_scientific_research_dpv_marketing, axiom,
    dpv_scientific_research != dpv_marketing).

% --- witness condition negated -------------------------------------------
fof(w_kgc314, axiom,
    ~ ( dpv_scientific_research = dpv_marketing )).
%--------------------------------------------------------------------------
