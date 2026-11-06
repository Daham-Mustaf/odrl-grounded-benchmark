%------------------------------------------------------------------------------
% File     : KGC105+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for any purpose except marketing against use for advertising only: no use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for any purpose except
%            marketing. A company commits to advertising. This problem states
%            that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC397-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC397 is Compatible. Its two problems state that some use meets
%            the two policies (KGC104) and that no use does (KGC105); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(bg_dist_dpv_marketing_dpv_advertising, axiom,
    dpv_marketing != dpv_advertising).

fof(w_kgc397, axiom,
    ~ ( dpv_advertising != dpv_marketing )).
%------------------------------------------------------------------------------
