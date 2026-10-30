%--------------------------------------------------------------------------
% File     : KGC397-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isNoneOf {Marketing} against eq Advertising, declared distinct (witness condition negated)
% Version  : 1.0
% English  : A city's traffic data platform permits use for any purpose except marketing. A company commits to advertising.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC397-2.p
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
% Declarations: https://w3id.org/odrl-kb/dpv-purposes/declared, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_dpv_marketing_dpv_advertising, axiom,
    dpv_marketing != dpv_advertising).

% --- witness condition negated -------------------------------------------
fof(w_kgc397, axiom,
    ~ ( dpv_advertising != dpv_marketing )).
%--------------------------------------------------------------------------
