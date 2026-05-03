%--------------------------------------------------------------------------
% File     : KGC704-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 5 (and): partial operand overlap [GeoNames+BCP47+DPV]
% Version  : 1.0
% English  : Corollary~\ref{cor:and-factoring} case (c): partial overlap
%           : of operand sets. CS over {spatial, language}; CS' over
%           : {language, purpose}. Shared operand: language. Atomic
%           : verdict on language is Conflict (registry uniqueness).
%           : Per Corollary 1 case (c), Strong Kleene aggregates over
%           : shared operands only; rule-level Conflict.
%           : 
%           : Setup:
%           : CS  (offer):
%           : c1_off = (spatial, isPartOf, gn:Europe)   [unshared]
%           : c2_off = (language, eq, bcp:de)            [shared]
%           : CS' (request):
%           : c2_req = (language, eq, bcp:fr)            [shared]
%           : c3_req = (purpose, isA, dpv:Purpose)       [unshared]
%           : 
%           : Shared operand: language. Atomic verdict at language:
%           : [c2_off] = {bcp_de}, [c2_req] = {bcp_fr};
%           : kge_disjoint(bcp_de, bcp_fr) by BCP47 registry uniqueness;
%           : forced_empty fires via pattern B1.
%           : => verdict_conflict(c2_off, c2_req).
%           : 
%           : Bridges (over shared operand language only):
%           : has_conflict(r1) <=> verdict_conflict(c2_off, c2_req).
%           : all_compat(r1) <=> verdict_compatible(c2_off, c2_req).
%           : 
%           : Strong Kleene AND: rule_and(R) = conflict <=>
%           : has_conflict(R). The shared-operand Conflict propagates
%           : to rule-level Conflict (Corollary 1 case (c)).
%           : 
%           : Conjecture (Style A): rule_and(r1) = conflict.
%           : Expected: Theorem.
%           : 
%           : Why this audit matters:
%           : Corollary 1 case (c) is the basis of Theorem 5
%           : (Composition Soundness): cross-pair verdicts in DNF
%           : decomposition aggregate over shared operands only.
%           : Without this audit, the shared-operand reasoning that
%           : carries Theorem 5 is unverified.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC704-1.p
%
% Status   : Theorem
% Verdict  : AndConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC704-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/GN000-0.ax').
include('Axioms/BCP47000-0.ax').
include('Axioms/DPV000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Shared operand: language (BCP47), atomic Conflict ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_eq(X, bcp_de))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_eq(X, bcp_fr))).

% --- Rule-level bridge over shared operands only ---
% Per Corollary 1 case (c): aggregate Strong Kleene over shared
% operands only. Unshared operands (spatial in CS, purpose in CS')
% do not participate in rule-level verdict aggregation.
fof(has_conflict_bridge, axiom,
    (has_conflict(r1) <=> verdict_conflict(c2_off, c2_req))).
fof(all_compat_bridge, axiom,
    (all_compat(r1) <=> verdict_compatible(c2_off, c2_req))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc704, conjecture,
    rule_and(r1) = conflict).
%--------------------------------------------------------------------------
