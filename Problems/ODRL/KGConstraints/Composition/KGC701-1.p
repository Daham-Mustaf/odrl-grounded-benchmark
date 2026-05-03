%--------------------------------------------------------------------------
% File     : KGC701-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 2 (and): Compatible does NOT yield Conflict [GeoNames, DPV]
% Version  : 1.0
% English  : Theorem 2 (and) Compatible aggregation, tested via the
%           : negative direction: when both operand pairs are Compatible,
%           : rule_and(r1) is Compatible (NOT conflict). Tests that the
%           : Strong Kleene AND rule does not over-derive Conflict.
%           : 
%           : Setup:
%           : Operand 1 (spatial, GeoNames):
%           : c1_off = (spatial, isPartOf, gn:Europe)
%           : c1_req = (spatial, eq, gn:France)
%           : [c1_off] = downward cone of gn_europe, [c1_req] = {gn_france}
%           : France is below Europe in GeoNames; witness gn_france.
%           : => verdict_compatible(c1_off, c1_req).
%           : 
%           : Operand 2 (purpose, DPV):
%           : c2_off = (purpose, eq, dpv:ScientificResearch)
%           : c2_req = (purpose, isA, dpv:Purpose)
%           : [c2_off] = {dpv_scientific_research},
%           : [c2_req] = downward cone of dpv_purpose
%           : SR is below Purpose in DPV; witness SR.
%           : => verdict_compatible(c2_off, c2_req).
%           : 
%           : Bridges:
%           : all_compat(r1) holds (both Compatible).
%           : has_conflict(r1) does NOT hold (no operand-pair Conflict).
%           : 
%           : Strong Kleene AND: rule_and(R) = compatible <=> all_compat(R).
%           : rule_and(r1) = compatible.
%           : Conjecture (Style B, asserting Conflict): rule_and(r1) = conflict.
%           : Expected: CounterSatisfiable. The rule is Compatible, so
%           : the asserted Conflict fails to derive.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC701-1.p
%
% Status   : CounterSatisfiable
% Verdict  : AndCompatibleNonConflict
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC701-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/GN000-0.ax').
include('Axioms/DPV000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Operand 1 pair ---
fof(c1_off_defined, axiom, ~denotation_undef(c1_off)).
fof(c1_req_defined, axiom, ~denotation_undef(c1_req)).
fof(c1_off_den, axiom,
    ![X]: (in_denotation(X, c1_off) <=> den_ispartof(X, gn_europe))).
fof(c1_req_den, axiom,
    ![X]: (in_denotation(X, c1_req) <=> den_eq(X, gn_france))).

% --- Operand 2 pair ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_eq(X, dpv_scientific_research))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_eq(X, dpv_marketing))).
% --- Concept distinctness ---
% DPV asserts neither equality nor disjointness between
% ScientificResearch and Marketing -- the OWA silence is exactly
% what makes operand 2 Unknown.  But to refute the existence of a
% witness X equating both denotations, we must assert that the two
% grounded concepts are distinct as IRIs.  Without this, the prover
% finds a model where SR = Marketing, vacuously making operand 2
% Compatible.
fof(sr_neq_marketing, axiom,
    dpv_scientific_research != dpv_marketing).
% --- Rule-level bridge axioms ---
% Wire the two operand-pair verdicts into has/all summaries on r1.
fof(has_compat_bridge, axiom,
    (has_compat(r1) <=>
       (verdict_compatible(c1_off, c1_req) |
        verdict_compatible(c2_off, c2_req)))).
fof(has_conflict_bridge, axiom,
    (has_conflict(r1) <=>
       (verdict_conflict(c1_off, c1_req) |
        verdict_conflict(c2_off, c2_req)))).
fof(all_compat_bridge, axiom,
    (all_compat(r1) <=>
       (verdict_compatible(c1_off, c1_req) &
        verdict_compatible(c2_off, c2_req)))).
fof(all_conflict_bridge, axiom,
    (all_conflict(r1) <=>
       (verdict_conflict(c1_off, c1_req) &
        verdict_conflict(c2_off, c2_req)))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc701, conjecture,
    rule_and(r1) = conflict).
%--------------------------------------------------------------------------
