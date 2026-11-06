%------------------------------------------------------------------------------
% File     : KGC084+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Distribute in any language except English and Italian against distribute in Italian only: no use meets both
% Version  : Especial.
% English  : English and Italian rights were sold separately, so a publisher
%            permits any language except English and Italian. The licensee
%            distributes in Italian. This problem states that no use meets the
%            two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC377-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC377 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC083) and that no use does (KGC084);
%            here the first is Unsatisfiable and the second Satisfiable. A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+1.ax').

fof(w_kgc377, axiom,
    ~ ( ~ ( $true ) )).
%------------------------------------------------------------------------------
