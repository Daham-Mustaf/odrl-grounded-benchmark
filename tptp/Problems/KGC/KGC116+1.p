%------------------------------------------------------------------------------
% File     : KGC116+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Distribute in at least one of German and French against distribute in both Dutch and French: no use meets both
% Version  : Especial.
% English  : A translation licence covers at least one of a German and a
%            French edition. The licensee publishes in both Dutch and French.
%            This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC398-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC398 is Compatible. Its two problems state that some use meets
%            the two policies (KGC115) and that no use does (KGC116). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+1.ax').

fof(w_kgc398, axiom,
    ~ ( $true )).
%------------------------------------------------------------------------------
