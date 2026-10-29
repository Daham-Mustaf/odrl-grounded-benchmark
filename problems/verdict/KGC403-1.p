%--------------------------------------------------------------------------
% File     : KGC403-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:SR against eq dpv:R&D, declared distinct (witness condition asserted)
% Version  : 1.0
% English  : As KGC316, with scientific research and research and development declared distinct.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC403-1.p
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
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_dpv_scientific_research_dpv_research_and_development, axiom,
    dpv_scientific_research != dpv_research_and_development).

% --- witness condition asserted ------------------------------------------
fof(w_kgc403, axiom,
    ( ( kge_leq(dpv_scientific_research, dpv_scientific_research) & dpv_scientific_research = dpv_research_and_development )
| ( kge_leq(dpv_research_and_development, dpv_scientific_research) & dpv_research_and_development = dpv_research_and_development ) )).
%--------------------------------------------------------------------------
