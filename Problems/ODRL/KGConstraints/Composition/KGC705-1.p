%--------------------------------------------------------------------------
% File     : KGC705-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 2 (and): three-operand all-Compatible [GeoNames+DPV+BCP47]
% Version  : 1.0
% English  : Theorem 2 (and) Compatible aggregation in a realistic three-
%           : operand, three-resource scenario. Tests Strong Kleene's
%           : all-Compatible case end-to-end: when every operand-pair is
%           : Compatible (via different reasoning paths in different
%           : resources), the rule-level verdict is Compatible.
%           : 
%           : Setup:
%           : Operand 1 (spatial, GeoNames):
%           : c1_off = (spatial, isPartOf, gn:Europe)
%           : c1_req = (spatial, eq, gn:France)
%           : [c1_off] = downward cone of gn_europe;
%           : [c1_req] = {gn_france}.
%           : France in cone of Europe; witness gn_france.
%           : => verdict_compatible(c1_off, c1_req).
%           : 
%           : Operand 2 (purpose, DPV):
%           : c2_off = (purpose, eq, dpv:ScientificResearch)
%           : c2_req = (purpose, isA, dpv:Purpose)
%           : [c2_off] = {dpv_scientific_research};
%           : [c2_req] = downward cone of dpv_purpose.
%           : SR in cone of Purpose; witness SR.
%           : => verdict_compatible(c2_off, c2_req).
%           : 
%           : Operand 3 (language, BCP47):
%           : c3_off = (language, eq, bcp:de)
%           : c3_req = (language, isAnyOf, {bcp:de, bcp:fr})
%           : [c3_off] = {bcp_de};
%           : [c3_req] = {bcp_de, bcp_fr}.
%           : bcp_de in [c3_req]; witness bcp_de.
%           : => verdict_compatible(c3_off, c3_req).
%           : 
%           : Bridges:
%           : all_compat(r1) holds (all three operand-pairs Compatible).
%           : has_conflict(r1) does NOT hold.
%           : 
%           : Strong Kleene AND: rule_and(R) = compatible <=> all_compat(R).
%           : rule_and(r1) = compatible.
%           : 
%           : Conjecture (Style B, asserting Conflict): rule_and(r1) = conflict.
%           : Expected: CounterSatisfiable. The rule is Compatible across
%           : three operand families and three resources; the asserted
%           : Conflict cannot derive.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC705-1.p
%
% Status   : CounterSatisfiable
% Verdict  : AndCompatibleNonConflict
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC705-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/GN000-0.ax').
include('Axioms/DPV000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Operand 1 pair (spatial, GeoNames) ---
fof(c1_off_defined, axiom, ~denotation_undef(c1_off)).
fof(c1_req_defined, axiom, ~denotation_undef(c1_req)).
fof(c1_off_den, axiom,
    ![X]: (in_denotation(X, c1_off) <=> den_ispartof(X, gn_europe))).
fof(c1_req_den, axiom,
    ![X]: (in_denotation(X, c1_req) <=> den_eq(X, gn_france))).

% --- Operand 2 pair (purpose, DPV) ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_eq(X, dpv_scientific_research))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_isa(X, dpv_purpose))).

% --- Operand 3 pair (language, BCP47) ---
fof(c3_off_defined, axiom, ~denotation_undef(c3_off)).
fof(c3_req_defined, axiom, ~denotation_undef(c3_req)).
fof(c3_off_den, axiom,
    ![X]: (in_denotation(X, c3_off) <=> den_eq(X, bcp_de))).
fof(c3_req_den, axiom,
    ![X]: (in_denotation(X, c3_req) <=>
              (den_eq(X, bcp_de) | den_eq(X, bcp_fr)))).

% --- Rule-level bridge axioms (3-operand version) ---
fof(has_conflict_bridge, axiom,
    (has_conflict(r1) <=>
       (verdict_conflict(c1_off, c1_req) |
        verdict_conflict(c2_off, c2_req) |
        verdict_conflict(c3_off, c3_req)))).
fof(all_compat_bridge, axiom,
    (all_compat(r1) <=>
       (verdict_compatible(c1_off, c1_req) &
        verdict_compatible(c2_off, c2_req) &
        verdict_compatible(c3_off, c3_req)))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc705, conjecture,
    rule_and(r1) = conflict).
%--------------------------------------------------------------------------
