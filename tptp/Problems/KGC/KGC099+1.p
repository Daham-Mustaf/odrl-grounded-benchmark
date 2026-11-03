%------------------------------------------------------------------------------
% File     : KGC099+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use within North Rhine-Westphalia or Bavaria against use in North Rhine-Westphalia only: some use meets both
% Version  : Especial.
% English  : A library permits use within North Rhine-Westphalia or within
%            Bavaria. A researcher's policy commits to use in North Rhine-
%            Westphalia. This problem states that some use meets the two
%            policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC388-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC388 is Compatible. Its two problems state that some use meets
%            the two policies (KGC099) and that no use does (KGC100). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+6.ax').

fof(w_kgc388, axiom,
    ( kge_leq(loc_de_nw, loc_de_nw)
| kge_leq(loc_de_nw, loc_de_by) )).
%------------------------------------------------------------------------------
