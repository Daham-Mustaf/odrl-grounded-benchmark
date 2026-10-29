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
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_dpv_advertising_dpv_marketing, axiom,
    dpv_advertising != dpv_marketing).

% --- witness condition negated -------------------------------------------
fof(w_kgc397, axiom,
    ~ ( ( ( dpv_marketing != dpv_marketing & dpv_marketing = dpv_advertising )
| ( dpv_advertising != dpv_marketing & dpv_advertising = dpv_advertising ) ) )).
%--------------------------------------------------------------------------
