%--------------------------------------------------------------------------
% File     : KGC317-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isNoneOf {dpv:Marketing} against eq dpv:Marketing (witness condition negated)
% Version  : 1.0
% English  : A library excludes marketing, while a researcher requests use for marketing.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC317-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty, and it stays empty.  The incompatibility here
% is between the two constraints, not between a constraint and something a
% party declared.

% --- witness condition negated -------------------------------------------
fof(w_kgc317, axiom,
    ~ ( ( dpv_marketing != dpv_marketing & dpv_marketing = dpv_marketing ) )).
%--------------------------------------------------------------------------
