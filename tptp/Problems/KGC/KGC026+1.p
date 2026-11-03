%------------------------------------------------------------------------------
% File     : KGC026+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for any purpose except marketing against use for marketing only: no use meets both
% Version  : Especial.
% English  : A city's traffic data platform permits use for any purpose other
%            than marketing. A company commits to use for marketing. This
%            problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC317-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC317 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC025) and that no use does (KGC026). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc317, axiom,
    ~ ( ~ ( $true ) )).
%------------------------------------------------------------------------------
