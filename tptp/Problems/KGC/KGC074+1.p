%------------------------------------------------------------------------------
% File     : KGC074+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use with at least one of encryption and access control in place against use with encryption at rest as the only measure: no use meets both
% Version  : Especial.
% English  : A controller requires at least one of encryption and access
%            control. A processor's policy commits to encryption at rest as
%            the only measure. This problem states that no use meets the two
%            policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC366-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC366 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC073) and that no use does (KGC074). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+4.ax').

fof(bg_dist_tm_encryption_tm_access_control_method, axiom,
    tm_encryption != tm_access_control_method).

fof(bg_dist_tm_encryption_tm_encryption_at_rest, axiom,
    tm_encryption != tm_encryption_at_rest).

fof(bg_dist_tm_access_control_method_tm_encryption_at_rest, axiom,
    tm_access_control_method != tm_encryption_at_rest).

fof(w_kgc366, axiom,
    ~ ( ( tm_encryption = tm_encryption_at_rest
| tm_access_control_method = tm_encryption_at_rest ) )).
%------------------------------------------------------------------------------
