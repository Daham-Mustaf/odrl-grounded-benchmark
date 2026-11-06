%------------------------------------------------------------------------------
% File     : KGC063+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use with at least one of encryption and access control in place against use with encryption as the only measure: some use meets both
% Version  : Especial.
% English  : A controller requires at least one of encryption and access
%            control. A processor's policy commits to encryption as the only
%            measure. This problem states that some use meets the two
%            policies. It is also a check of KGC365: A controller requires
%            both encryption and access control. A processor commits to
%            encryption, access control and pseudonymisation together. There
%            it states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC362-1 [Mus26]
%          : KGC365-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : This problem is 2 checks whose formulas and include lines are the
%            same after renaming the case. KGC362 is Compatible. Its two
%            problems state that some use meets the two policies (KGC063) and
%            that no use does (KGC064); here the first is Satisfiable and the
%            second Unsatisfiable. KGC365 is Compatible. Its two problems
%            state that some use meets the two policies (KGC063) and that no
%            use does (KGC064); here the first is Satisfiable and the second
%            Unsatisfiable. A pair of policies is Incompatible when the first
%            is Unsatisfiable, Compatible when the second is Unsatisfiable,
%            and Unknown when both are Satisfiable; a Satisfiable problem also
%            shows the statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+4.ax').

fof(w_kgc362, axiom,
    $true).
%------------------------------------------------------------------------------
