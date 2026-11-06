%------------------------------------------------------------------------------
% File     : KGC090+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use within the European Union against use in North Rhine-Westphalia only: some use meets both
% Version  : Especial.
% English  : A library permits use within the European Union. A researcher's
%            policy commits to use in North Rhine-Westphalia. This problem
%            states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC383-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC383 is Compatible. Its two problems state that some use meets
%            the two policies (KGC090) and that no use does (KGC091); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+7.ax').

fof(w_kgc383, axiom,
    kge_leq(loc_de_nw, loc_eu)).
%------------------------------------------------------------------------------
