%--------------------------------------------------------------------------
% File     : KGC318-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, neq dpv:Marketing against eq dpv:ScientificResearch, declared distinct (witness condition negated)
% Version  : 1.0
% English  : A library permits use for any purpose other than marketing. A researcher's policy commits to use for scientific research. Scientific research is declared distinct from marketing.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC318-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').
include('axioms/DPV-dpv-purposes-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_dpv_scientific_research_dpv_marketing, axiom,
    dpv_scientific_research != dpv_marketing).

% --- witness condition negated -------------------------------------------
fof(w_kgc318, axiom,
    ~ ( ( ( dpv_marketing != dpv_marketing & dpv_marketing = dpv_scientific_research )
| ( dpv_scientific_research != dpv_marketing & dpv_scientific_research = dpv_scientific_research ) ) )).
%--------------------------------------------------------------------------
