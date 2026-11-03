%------------------------------------------------------------------------------
% File     : KGC030+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use under exactly one of the commercial and non-commercial tiers against use for non-commercial research only: no use meets both
% Version  : Especial.
% English  : A city's traffic data platform prices its data in two tiers,
%            commercial and non-commercial, and each use must fall under
%            exactly one tier. A university research group commits to use for
%            non-commercial research. This problem states that no use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC319-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC319 is Unknown. Its two problems state that some use meets the
%            two policies (KGC029) and that no use does (KGC030). A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc319, axiom,
    ~ ( ( ( kge_leq(dpv_non_commercial_research, dpv_commercial_purpose) & ~ ( kge_leq(dpv_non_commercial_research, dpv_non_commercial_purpose) ) )
| ( kge_leq(dpv_non_commercial_research, dpv_non_commercial_purpose) & ~ ( kge_leq(dpv_non_commercial_research, dpv_commercial_purpose) ) ) ) )).
%------------------------------------------------------------------------------
