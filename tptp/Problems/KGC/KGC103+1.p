%------------------------------------------------------------------------------
% File     : KGC103+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for public benefit or any narrower purpose against use for both data altruism and improving transport mobility: no use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for public benefit or
%            any narrower purpose. A city transport authority commits to data
%            altruism and improving transport mobility together. This problem
%            states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC396-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC396 is Compatible. Its two problems state that some use meets
%            the two policies (KGC102) and that no use does (KGC103); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc396, axiom,
    ~ ( ( kge_leq(dpv_data_altruism, dpv_public_benefit) & kge_leq(dpv_improve_transport_mobility, dpv_public_benefit) ) )).
%------------------------------------------------------------------------------
