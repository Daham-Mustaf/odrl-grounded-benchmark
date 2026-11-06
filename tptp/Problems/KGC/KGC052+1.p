%------------------------------------------------------------------------------
% File     : KGC052+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use only under given or renewed consent against use only under renewed consent: no use meets both
% Version  : Especial.
% English  : A controller permits use under given or renewed consent. A
%            processor's policy commits to processing only under renewed
%            consent. This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC341-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC341 is Compatible. Its two problems state that some use meets
%            the two policies (KGC051) and that no use does (KGC052); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+2.ax').

fof(w_kgc341, axiom,
    ~ ( $true )).
%------------------------------------------------------------------------------
