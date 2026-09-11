%--------------------------------------------------------------------------
% File     : KGC313-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, eq dpv:Marketing against eq dpv:SR (witness condition asserted)
% Version  : 1.0
% English  : A library permits use for marketing, while a researcher requests use for scientific research.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC313-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  Two names are not two concepts until something
% says so, and the purposes module says nothing.

% --- witness condition asserted ------------------------------------------
fof(w_kgc313, axiom,
    ( ( dpv_marketing = dpv_marketing & dpv_marketing = dpv_scientific_research )
| ( dpv_scientific_research = dpv_marketing & dpv_scientific_research = dpv_scientific_research ) )).
%--------------------------------------------------------------------------
