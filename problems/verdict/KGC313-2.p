%--------------------------------------------------------------------------
% File     : KGC313-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, eq dpv:Marketing against eq dpv:SR (witness condition negated)
% Version  : 1.0
% English  : A city's traffic data platform permits use for marketing. A university commits to use for scientific research.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC313-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: empty.  Two names are not two concepts until something
% says so, and the purposes module says nothing.

% --- witness condition negated -------------------------------------------
fof(w_kgc313, axiom,
    ~ ( ( ( dpv_marketing = dpv_marketing & dpv_marketing = dpv_scientific_research )
| ( dpv_scientific_research = dpv_marketing & dpv_scientific_research = dpv_scientific_research ) ) )).
%--------------------------------------------------------------------------
