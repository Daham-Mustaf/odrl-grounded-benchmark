%------------------------------------------------------------------------------
% File     : KGC093+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use within the European Union against use in Bonaire only: some use meets both
% Version  : Especial.
% English  : A library permits use within the European Union. A researcher's
%            policy commits to use in Bonaire. This problem states that some
%            use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC380-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC380 is Compatible. Its two problems state that some use meets
%            the two policies (KGC093) and that no use does (KGC094). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+7.ax').

fof(w_kgc380, axiom,
    kge_leq(loc_nl_bq1, loc_eu)).
%------------------------------------------------------------------------------
