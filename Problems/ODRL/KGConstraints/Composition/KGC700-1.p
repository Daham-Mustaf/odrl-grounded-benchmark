%--------------------------------------------------------------------------
% File     : KGC700-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 2 (and): Conflict aggregation [GeoNames+SDA, BCP47]
% Version  : 1.0
% English  : Theorem 2 (and) Conflict aggregation. Two operand-pair
%           : verdicts of Conflict combine to rule-level Conflict via
%           : Strong Kleene's `existential Conflict` rule for AND.
%           : 
%           : Setup:
%           : Operand 1 (spatial, GeoNames+SDA):
%           : c1_off = (spatial, eq, gn:Bayern)
%           : c1_req = (spatial, eq, gn:France)
%           : [c1_off] = {gn_bayern}, [c1_req] = {gn_france}
%           : SDA asserts kge_disjoint(gn_germany, gn_france);
%           : Bayern is below Germany, so B1 pattern fires:
%           : forced_empty([c1_off], [c1_req]) holds.
%           : => verdict_conflict(c1_off, c1_req).
%           : 
%           : Operand 2 (language, BCP47):
%           : c2_off = (language, eq, bcp:de)
%           : c2_req = (language, eq, bcp:fr)
%           : [c2_off] = {bcp_de}, [c2_req] = {bcp_fr}
%           : BCP47 asserts kge_disjoint(bcp_de, bcp_fr).
%           : => verdict_conflict(c2_off, c2_req).
%           : 
%           : Bridges:
%           : has_conflict(r1) holds (both operand-pairs Conflict).
%           : 
%           : Strong Kleene AND: rule_and(R) = conflict <=> has_conflict(R).
%           : Conjecture (Style A): rule_and(r1) = conflict.
%           : Expected: Theorem.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC700-1.p
%
% Status   : Theorem
% Verdict  : AndConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC700-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/GN000-0.ax').
include('Axioms/GN001-SDA-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Operand 1 pair ---
fof(c1_off_defined, axiom, ~denotation_undef(c1_off)).
fof(c1_req_defined, axiom, ~denotation_undef(c1_req)).
fof(c1_off_den, axiom,
    ![X]: (in_denotation(X, c1_off) <=> den_eq(X, gn_bayern))).
fof(c1_req_den, axiom,
    ![X]: (in_denotation(X, c1_req) <=> den_eq(X, gn_france))).

% --- Operand 2 pair ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_eq(X, bcp_de))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_eq(X, bcp_fr))).
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
fof(kgc700, conjecture,
    rule_and(r1) = conflict).
%--------------------------------------------------------------------------
