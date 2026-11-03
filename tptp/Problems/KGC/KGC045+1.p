%------------------------------------------------------------------------------
% File     : KGC045+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use anywhere except Germany against use in France only: some use meets both
% Version  : Especial.
% English  : A library permits use anywhere except Germany. A researcher's
%            policy commits to use in France. The ISO 3166 rule makes the two
%            countries different places. This problem states that some use
%            meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC335-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC335 is Compatible. Its two problems state that some use meets
%            the two policies (KGC045) and that no use does (KGC046). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+6.ax').

fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

fof(w_kgc335, axiom,
    loc_fr != loc_de).
%------------------------------------------------------------------------------
