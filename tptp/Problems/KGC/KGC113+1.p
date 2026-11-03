%------------------------------------------------------------------------------
% File     : KGC113+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for any purpose except marketing against use for advertising only: some use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for any purpose except
%            marketing. A company commits to advertising. This problem states
%            that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC397-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC397 is Compatible. Its two problems state that some use meets
%            the two policies (KGC113) and that no use does (KGC114). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(bg_dist_dpv_marketing_dpv_advertising, axiom,
    dpv_marketing != dpv_advertising).

fof(w_kgc397, axiom,
    dpv_advertising != dpv_marketing).
%------------------------------------------------------------------------------
