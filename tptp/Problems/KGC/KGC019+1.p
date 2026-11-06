%------------------------------------------------------------------------------
% File     : KGC019+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for any DPV purpose against use for delivery of goods only: some use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for any DPV purpose. A
%            logistics company commits to use for delivery of goods. This
%            problem states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC315-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC315 is Compatible. Its two problems state that some use meets
%            the two policies (KGC019) and that no use does (KGC020); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc315, axiom,
    kge_leq(dpv_delivery_of_goods, dpv_purpose)).
%------------------------------------------------------------------------------
