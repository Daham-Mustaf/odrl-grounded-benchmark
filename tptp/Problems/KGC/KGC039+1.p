%------------------------------------------------------------------------------
% File     : KGC039+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in Germany only against use in France only: some use meets both
% Version  : Especial.
% English  : A library permits use in Germany. A researcher's policy commits
%            to use in France. This problem states that some use meets the two
%            policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC333-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC333 is Unknown. Its two problems state that some use meets the
%            two policies (KGC039) and that no use does (KGC040); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+6.ax').

fof(w_kgc333, axiom,
    loc_de = loc_fr).
%------------------------------------------------------------------------------
