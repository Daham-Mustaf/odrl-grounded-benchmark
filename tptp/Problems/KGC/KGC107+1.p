%------------------------------------------------------------------------------
% File     : KGC107+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for at least one of public benefit and non-commercial research against use for improving transport mobility only: some use meets both
% Version  : Especial.
% English  : As KGC393, with improving transport mobility declared distinct
%            from both purposes the first policy names. This problem states
%            that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC394-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC394 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC107) and that no use does (KGC108). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(bg_dist_dpv_public_benefit_dpv_non_commercial_research, axiom,
    dpv_public_benefit != dpv_non_commercial_research).

fof(bg_dist_dpv_public_benefit_dpv_improve_transport_mobility, axiom,
    dpv_public_benefit != dpv_improve_transport_mobility).

fof(bg_dist_dpv_non_commercial_research_dpv_improve_transport_mobility, axiom,
    dpv_non_commercial_research != dpv_improve_transport_mobility).

fof(w_kgc394, axiom,
    ( dpv_public_benefit = dpv_improve_transport_mobility
| dpv_non_commercial_research = dpv_improve_transport_mobility )).
%------------------------------------------------------------------------------
