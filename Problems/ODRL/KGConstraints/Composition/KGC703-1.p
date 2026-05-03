%--------------------------------------------------------------------------
% File     : KGC703-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 5 (and): disjoint operand sets [GeoNames | BCP47]
% Version  : 1.0
% English  : Corollary~\ref{cor:and-factoring} case (a): disjoint
%           : operand sets yield rule-level Compatible vacuously. CS
%           : constrains spatial only; CS' constrains language only.
%           : No shared operand, so the rule-level intersection is
%           : unrestricted across both rules.
%           : 
%           : Setup:
%           : CS  (offer): one constraint on spatial, no others.
%           : c1_off = (spatial, isPartOf, gn:Europe)
%           : CS' (request): one constraint on language, no others.
%           : c2_req = (language, eq, bcp:de)
%           : 
%           : Operand sets: L = {spatial}, L' = {language}, L cap L' =
%           : empty. Per Corollary 1 case (a), rule_and(r1) = compatible.
%           : 
%           : Bridges:
%           : has_conflict(r1) is vacuously false (no operand-pair
%           : has both a CS and CS' constraint to compare).
%           : all_compat(r1) is vacuously true (no shared operand to
%           : aggregate over).
%           : 
%           : Strong Kleene AND with empty shared-operand set: the
%           : vacuous quantification yields all_compat -> rule
%           : Compatible.
%           : 
%           : Conjecture (Style B, asserting Conflict): rule_and(r1) = conflict.
%           : Expected: CounterSatisfiable. Disjoint operand sets cannot
%           : produce Conflict; the asserted conflict fails to derive.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC703-1.p
%
% Status   : CounterSatisfiable
% Verdict  : AndCompatibleNonConflict
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC703-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/GN000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Single operand on each side (disjoint operand sets) ---
fof(c_offer_defined, axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).
fof(c_offer_den, axiom,
    ![X]: (in_denotation(X, c_offer) <=> den_ispartof(X, gn_europe))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).

% --- Rule-level bridge axioms (vacuous for disjoint operand sets) ---
% Disjoint operand sets: no shared-operand verdict to aggregate.
% has_conflict(r1) is vacuously false; all_compat(r1) is vacuously true.
% This is Corollary 1 case (a).
fof(has_conflict_bridge, axiom,
    ~has_conflict(r1)).
fof(all_compat_bridge, axiom,
    all_compat(r1)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc703, conjecture,
    rule_and(r1) = conflict).
%--------------------------------------------------------------------------
