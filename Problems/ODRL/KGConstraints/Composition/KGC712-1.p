%--------------------------------------------------------------------------
% File     : KGC712-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 2 (or): Unknown propagation [DPV]
% Version  : 1.0
% English  : Proposition~\ref{prop:cross-disjunct} or-Unknown propagation.
%           : Single-disjunct each side; the cross-pair is atomic-Unknown
%           : (DPV silent on the relevant pair). Asserted as a premise
%           : since OWA-Unknown is not positively derivable in FOL
%           : (see KGC702/706 audit notes; atomic Unknown audited at
%           : KGC412).
%           : 
%           : Setup:
%           : CS  = or(d1):
%           : d1  = (purpose, isA, dpv:NonCommercialPurpose)
%           : CS' = or(d1p):
%           : d1p = (purpose, eq, dpv:ScientificResearch)
%           : 
%           : Cross-pair (d1, d1p): DPV asserts neither a skos:broader
%           : edge nor disjointness between ScientificResearch and
%           : NonCommercialPurpose; atomic verdict is Unknown.
%           : 
%           : No cross-pair is disjunct_compat; not every cross-pair is
%           : disjunct_conflict; so by Proposition 2 and the rule-level
%           : verdict definition, rule_or(r1, r2) = unknown.
%           : 
%           : Conjecture (Style A): rule_or(r1, r2) = unknown.
%           : Expected: Theorem.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC712-1.p
%
% Status   : Theorem
% Verdict  : OrUnknown
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC712-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/COMPOSE001-0.ax').
include('Axioms/DPV000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Disjunct membership (single disjunct each side) ---
fof(r1_disjunct_d1,  axiom, has_disjunct(r1, d1)).
fof(r2_disjunct_d1p, axiom, has_disjunct(r2, d1p)).

fof(r1_closure, axiom,
    ![D]: (has_disjunct(r1, D) <=> D = d1)).
fof(r2_closure, axiom,
    ![D]: (has_disjunct(r2, D) <=> D = d1p)).

fof(disjuncts_distinct, axiom,
    d1 != d1p).

% --- Atomic-level constraint denotations per disjunct ---
fof(c_d1_defined, axiom, ~denotation_undef(c_d1)).
fof(c_d1_den, axiom,
    ![X]: (in_denotation(X, c_d1) <=>
              den_isa(X, dpv_non_commercial_purpose))).

fof(c_d1p_defined, axiom, ~denotation_undef(c_d1p)).
fof(c_d1p_den, axiom,
    ![X]: (in_denotation(X, c_d1p) <=>
              den_eq(X, dpv_scientific_research))).

% --- Atomic-level Unknown asserted as premise ---
% OWA non-derivability for verdict_unknown; see KGC702/706 audit notes
% and atomic audit KGC412.
fof(d1_d1p_atomic_unknown, axiom,
    verdict_unknown(c_d1, c_d1p)).

% --- Disjunct-pair verdict bridges ---
% Single-atomic disjuncts: disjunct verdicts mirror atomic verdicts.
fof(d1_d1p_compat_bridge, axiom,
    (disjunct_compat(d1, d1p) <=> verdict_compatible(c_d1, c_d1p))).
fof(d1_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d1, d1p) <=> verdict_conflict(c_d1, c_d1p))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc712, conjecture,
    rule_or(r1, r2) = unknown).
%--------------------------------------------------------------------------
