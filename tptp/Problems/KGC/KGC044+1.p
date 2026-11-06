%------------------------------------------------------------------------------
% File     : KGC044+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use anywhere except Germany against use in France only: no use meets both
% Version  : Especial.
% English  : A library permits use anywhere except Germany. A researcher's
%            policy commits to use in France. The ISO 3166 rule makes the two
%            countries different places. This problem states that no use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC335-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC335 is Compatible. Its two problems state that some use meets
%            the two policies (KGC043) and that no use does (KGC044); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+6.ax').

fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

fof(w_kgc335, axiom,
    ~ ( loc_fr != loc_de )).
%------------------------------------------------------------------------------
