%--------------------------------------------------------------------------
% File     : KGC316-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:SR against eq dpv:R&D (witness condition negated)
% Version  : 1.0
% English  : A library permits use for scientific research. A researcher's policy commits to use for research and development.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC316-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: empty.  The purposes module publishes no disjointness
% and no distinctness, and the parties declare none.

% --- witness condition negated -------------------------------------------
fof(w_kgc316, axiom,
    ~ ( ( ( kge_leq(dpv_scientific_research, dpv_scientific_research) & dpv_scientific_research = dpv_research_and_development )
| ( kge_leq(dpv_research_and_development, dpv_scientific_research) & dpv_research_and_development = dpv_research_and_development ) ) )).
%--------------------------------------------------------------------------
