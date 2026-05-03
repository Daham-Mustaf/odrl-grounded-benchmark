%--------------------------------------------------------------------------
% File     : KGC702-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 2 (and): Strong Kleene Unknown propagation [GeoNames, DPV]
% Version  : 1.0
% English  : Theorem 2 (and) Strong Kleene Unknown propagation. One operand
%           : pair Compatible, one Unknown; rule_and(r1) = unknown by Strong
%           : Kleene's Unknown-propagation rule.
%           : 
%           : Setup:
%           : Operand 1 (spatial, GeoNames): verdict_compatible holds
%           : (France in cone of Europe; witness gn_france). Asserted
%           : as a premise.
%           : Operand 2 (purpose, DPV): verdict_unknown holds (DPV silent
%           : on disjointness between SR and Marketing). Asserted as
%           : a premise.
%           : 
%           : Why operand-level verdicts are asserted as premises:
%           : verdict_compatible is positively derivable (witness exists)
%           : but asserted for symmetry. verdict_unknown under OWA is the
%           : meta-claim ~verdict_compatible & ~verdict_conflict, which is
%           : not positively derivable in FOL: it requires showing two
%           : negative existentials over an unbounded concept domain. We
%           : assert it as a premise to isolate Theorem 2's rule-level
%           : claim (Strong Kleene aggregation) from the operand-level
%           : Unknown derivation, which is separately audited in KGC402,
%           : KGC412, etc., and known to require model-finding rather
%           : than saturation (see eprover/cvc5 limitations on those
%           : problems).
%           : 
%           : Bridges:
%           : Premise verdict_unknown(c2_off, c2_req) implies
%           : ~verdict_compatible(c2_off, c2_req) by verdict_unknown_def.
%           : This implies ~all_compat(r1) via the bridge.
%           : Premise verdict_unknown also gives ~verdict_conflict, so
%           : ~has_conflict(r1) via the bridge.
%           : 
%           : Strong Kleene AND:
%           : rule_and(R) = unknown <=> ~all_compat(R) & ~has_conflict(R).
%           : Both negations hold for r1, so rule_and(r1) = unknown.
%           : 
%           : Conjecture (Style A): rule_and(r1) = unknown.
%           : Expected: Theorem.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC702-1.p
%
% Status   : Theorem
% Verdict  : AndUnknown
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC702-policy.ttl
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

% --- Operand-level verdict premises ---
% Operand 1: verdict_compatible is positively derivable
% (gn_france is in both [c1_off] and [c1_req]). Asserted explicitly
% to keep the proof focused on rule-level aggregation.
fof(c1_compat_premise, axiom,
    verdict_compatible(c1_off, c1_req)).

% Operand 2: verdict_unknown is the OWA meta-claim that DPV is silent
% on the SR-vs-Marketing pair. Not positively derivable in FOL (no
% finite witness for two nested negations under unbounded quantification).
% Asserted as a premise so the audit isolates Theorem 2's Strong Kleene
% rule-level aggregation from operand-level Unknown derivation, which
% is separately audited (KGC402, KGC412, etc.).
fof(c2_unknown_premise, axiom,
    verdict_unknown(c2_off, c2_req)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc702, conjecture,
    rule_and(r1) = unknown).
%--------------------------------------------------------------------------
