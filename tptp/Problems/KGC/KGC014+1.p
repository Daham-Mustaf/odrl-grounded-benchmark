%------------------------------------------------------------------------------
% File     : KGC014+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for research and development or any narrower purpose against use for scientific research only: no use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for research and
%            development or any narrower purpose. A university commits to use
%            for scientific research. This problem states that no use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC310-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC310 is Compatible. Its two problems state that some use meets
%            the two policies (KGC013) and that no use does (KGC014); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc310, axiom,
    ~ ( kge_leq(dpv_scientific_research, dpv_research_and_development) )).
%------------------------------------------------------------------------------
