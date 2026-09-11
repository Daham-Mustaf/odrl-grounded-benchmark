%--------------------------------------------------------------------------
% File     : KGC397-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isNoneOf {Marketing} against eq Advertising, declared distinct (witness condition asserted)
% Version  : 1.0
% English  : A provider permits use for any purpose except marketing; a consumer commits to advertising.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC397-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').
include('axioms/DPV-dpv-purposes-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: declared distinctness instances, stated in
% the declared theory file and instantiated here.

fof(bg_dist_dpv_advertising_dpv_marketing, axiom,
    dpv_advertising != dpv_marketing).

% --- witness condition asserted ------------------------------------------
fof(w_kgc397, axiom,
    ( ( dpv_marketing != dpv_marketing & dpv_marketing = dpv_advertising )
| ( dpv_advertising != dpv_marketing & dpv_advertising = dpv_advertising ) )).
%--------------------------------------------------------------------------
