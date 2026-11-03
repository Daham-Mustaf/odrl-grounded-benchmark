%------------------------------------------------------------------------------
% File     : KGC020+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for scientific research only against use for marketing only: no use meets both
% Version  : Especial.
% English  : As KGC313, with scientific research and marketing declared
%            distinct. This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC314-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC314 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC019) and that no use does (KGC020). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(bg_dist_dpv_scientific_research_dpv_marketing, axiom,
    dpv_scientific_research != dpv_marketing).

fof(w_kgc314, axiom,
    ~ ( dpv_scientific_research = dpv_marketing )).
%------------------------------------------------------------------------------
