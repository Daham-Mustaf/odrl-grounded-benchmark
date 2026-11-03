%------------------------------------------------------------------------------
% File     : KGC109+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for public benefit or non-commercial research, or any narrower purpose against use for improving transport mobility only: some use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for public benefit or
%            non-commercial research, or any narrower purpose. A city
%            transport authority commits to improving transport mobility. This
%            problem states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC395-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC395 is Compatible. Its two problems state that some use meets
%            the two policies (KGC109) and that no use does (KGC110). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc395, axiom,
    ( kge_leq(dpv_improve_transport_mobility, dpv_public_benefit)
| kge_leq(dpv_improve_transport_mobility, dpv_non_commercial_research) )).
%------------------------------------------------------------------------------
