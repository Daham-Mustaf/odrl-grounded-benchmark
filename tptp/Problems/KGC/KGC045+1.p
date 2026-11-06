%------------------------------------------------------------------------------
% File     : KGC045+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in at least one of Germany and France against use in Bavaria only: some use meets both
% Version  : Especial.
% English  : A library permits use in at least one of Germany and France. A
%            researcher's policy commits to use in Bavaria. The ISO 3166 rule
%            makes Bavaria a different place from both countries. This problem
%            states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC336-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC336 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC045) and that no use does (KGC046);
%            here the first is Unsatisfiable and the second Satisfiable. A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+6.ax').

fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

fof(bg_dist_loc_de_loc_de_by, axiom,
    loc_de != loc_de_by).

fof(bg_dist_loc_fr_loc_de_by, axiom,
    loc_fr != loc_de_by).

fof(w_kgc336, axiom,
    ( loc_de = loc_de_by
| loc_fr = loc_de_by )).
%------------------------------------------------------------------------------
