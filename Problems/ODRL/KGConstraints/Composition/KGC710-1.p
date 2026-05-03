%--------------------------------------------------------------------------
% File     : KGC710-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 2 (or): all cross-pairs Conflict [BCP47]
% Version  : 1.0
% English  : Proposition~\ref{prop:cross-disjunct} or-Conflict.
%           : Two or-composed rules whose every cross-pair has
%           : disjunct-level Conflict; rule_or(r1, r2) = conflict.
%           : 
%           : Setup:
%           : CS  = or(d1, d2):
%           : d1  = (language, eq, bcp:de)
%           : d2  = (language, eq, bcp:fr)
%           : CS' = or(d1p):
%           : d1p = (language, eq, bcp:it)
%           : 
%           : Cross-pairs:
%           : (d1, d1p): bcp:de vs bcp:it -- disjoint by BCP47 registry
%           : uniqueness; atomic-level B1 fires; disjunct_conflict.
%           : (d2, d1p): bcp:fr vs bcp:it -- disjoint; disjunct_conflict.
%           : 
%           : Both cross-pairs Conflict, so by Proposition 2,
%           : rule_or(r1, r2) = conflict.
%           : 
%           : Conjecture (Style A): rule_or(r1, r2) = conflict.
%           : Expected: Theorem.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC710-1.p
%
% Status   : Theorem
% Verdict  : OrConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC710-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/COMPOSE001-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Disjunct membership ---
fof(r1_disjunct_d1,  axiom, has_disjunct(r1, d1)).
fof(r1_disjunct_d2,  axiom, has_disjunct(r1, d2)).
fof(r2_disjunct_d1p, axiom, has_disjunct(r2, d1p)).

fof(r1_closure, axiom,
    ![D]: (has_disjunct(r1, D) <=> (D = d1 | D = d2))).
fof(r2_closure, axiom,
    ![D]: (has_disjunct(r2, D) <=> D = d1p)).

fof(disjuncts_distinct, axiom,
    d1 != d2 & d1 != d1p & d2 != d1p).

% --- Atomic-level constraint denotations per disjunct ---
fof(c_d1_defined, axiom, ~denotation_undef(c_d1)).
fof(c_d1_den, axiom,
    ![X]: (in_denotation(X, c_d1) <=> den_eq(X, bcp_de))).

fof(c_d2_defined, axiom, ~denotation_undef(c_d2)).
fof(c_d2_den, axiom,
    ![X]: (in_denotation(X, c_d2) <=> den_eq(X, bcp_fr))).

fof(c_d1p_defined, axiom, ~denotation_undef(c_d1p)).
fof(c_d1p_den, axiom,
    ![X]: (in_denotation(X, c_d1p) <=> den_eq(X, bcp_it))).

% --- Disjunct-pair Conflict bridges ---
% Each disjunct is a single atomic constraint, so disjunct-level
% Conflict reduces to atomic verdict_conflict on the constraint pair.
fof(d1_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d1, d1p) <=> verdict_conflict(c_d1, c_d1p))).
fof(d2_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d2, d1p) <=> verdict_conflict(c_d2, c_d1p))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc710, conjecture,
    rule_or(r1, r2) = conflict).
%--------------------------------------------------------------------------
