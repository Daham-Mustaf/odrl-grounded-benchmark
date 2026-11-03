%------------------------------------------------------------------------------
% File     : KGC010+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in exactly one of France and Germany against use in France only: no use meets both
% Version  : Especial.
% English  : As KGC303, with France and Germany declared distinct. This
%            problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC304-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC304 is Compatible. Its two problems state that some use meets
%            the two policies (KGC009) and that no use does (KGC010). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+5.ax').

fof(bg_dist_gn_france_gn_germany, axiom,
    gn_france != gn_germany).

fof(w_kgc304, axiom,
    ~ ( gn_france != gn_germany )).
%------------------------------------------------------------------------------
