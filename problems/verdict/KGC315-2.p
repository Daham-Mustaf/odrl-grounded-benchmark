%--------------------------------------------------------------------------
% File     : KGC315-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:Purpose against eq dpv:DeliveryOfGoods (witness condition negated)
% Version  : 1.0
% English  : A city's traffic data platform permits use for any DPV purpose. A logistics company commits to use for delivery of goods.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC315-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: empty.

% --- witness condition negated -------------------------------------------
fof(w_kgc315, axiom,
    ~ ( kge_leq(dpv_delivery_of_goods, dpv_purpose) )).
%--------------------------------------------------------------------------
