%------------------------------------------------------------------------------
% File     : KGC119+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for scientific research or any narrower purpose against use for research and development only: some use meets both
% Version  : Especial.
% English  : As KGC316, with scientific research and research and development
%            declared distinct. This problem states that some use meets the
%            two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC403-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC403 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC119) and that no use does (KGC120). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(bg_dist_dpv_scientific_research_dpv_research_and_development, axiom,
    dpv_scientific_research != dpv_research_and_development).

fof(w_kgc403, axiom,
    kge_leq(dpv_research_and_development, dpv_scientific_research)).
%------------------------------------------------------------------------------
