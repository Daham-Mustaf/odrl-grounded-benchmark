%------------------------------------------------------------------------------
% File     : KGC066+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use with both encryption and access control in place against use with encryption as the only measure: no use meets both
% Version  : Especial.
% English  : A controller requires both encryption and access control; a
%            processor commits to encryption only. This problem states that no
%            use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC363-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC363 is Unknown. Its two problems state that some use meets the
%            two policies (KGC065) and that no use does (KGC066); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+4.ax').

fof(w_kgc363, axiom,
    ~ ( tm_access_control_method = tm_encryption )).
%------------------------------------------------------------------------------
