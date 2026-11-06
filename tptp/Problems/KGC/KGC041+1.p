%------------------------------------------------------------------------------
% File     : KGC041+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in Germany only against use in France only: some use meets both
% Version  : Especial.
% English  : As KGC333, with the ISO 3166 rule that different country codes
%            name different countries. This problem states that some use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC334-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC334 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC041) and that no use does (KGC042);
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

fof(w_kgc334, axiom,
    loc_de = loc_fr).
%------------------------------------------------------------------------------
