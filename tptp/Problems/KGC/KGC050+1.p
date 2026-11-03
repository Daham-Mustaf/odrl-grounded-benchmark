%------------------------------------------------------------------------------
% File     : KGC050+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in both Germany and France against use in Germany only: no use meets both
% Version  : Especial.
% English  : A library lends its digitised manuscripts to a Franco-German
%            research programme and requires use at partner sites in both
%            Germany and France. A researcher's policy commits to use in
%            Germany only. The ISO 3166 rule makes the two countries different
%            places. This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC337-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC337 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC049) and that no use does (KGC050). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+6.ax').

fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

fof(w_kgc337, axiom,
    ~ ( loc_fr = loc_de )).
%------------------------------------------------------------------------------
