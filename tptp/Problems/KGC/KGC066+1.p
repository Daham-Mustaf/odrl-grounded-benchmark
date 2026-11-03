%------------------------------------------------------------------------------
% File     : KGC066+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use with at least one of encryption and access control in place against use with encryption as the only measure: no use meets both
% Version  : Especial.
% English  : A controller requires at least one of encryption and access
%            control. A processor's policy commits to encryption as the only
%            measure. This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC362-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC362 is Compatible. Its two problems state that some use meets
%            the two policies (KGC065) and that no use does (KGC066). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+4.ax').

fof(w_kgc362, axiom,
    ~ ( $true )).
%------------------------------------------------------------------------------
