%------------------------------------------------------------------------------
% File     : KGC101+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in an area that covers all of North Rhine-Westphalia against use in Germany only: some use meets both
% Version  : Especial.
% English  : A library, bound by a digitisation grant from North Rhine-
%            Westphalia, permits use only in an area that covers all of the
%            state. A researcher's policy commits to use in Germany, which
%            covers the state. This problem states that some use meets the two
%            policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC391-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC391 is Compatible. Its two problems state that some use meets
%            the two policies (KGC101) and that no use does (KGC102). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+6.ax').

fof(w_kgc391, axiom,
    kge_leq(loc_de_nw, loc_de)).
%------------------------------------------------------------------------------
