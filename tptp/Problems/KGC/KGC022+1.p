%------------------------------------------------------------------------------
% File     : KGC022+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for scientific research or any narrower purpose against use for research and development only: no use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for scientific
%            research or any narrower purpose. A company commits to use for
%            research and development. This problem states that no use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC316-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC316 is Unknown. Its two problems state that some use meets the
%            two policies (KGC021) and that no use does (KGC022); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc316, axiom,
    ~ ( kge_leq(dpv_research_and_development, dpv_scientific_research) )).
%------------------------------------------------------------------------------
