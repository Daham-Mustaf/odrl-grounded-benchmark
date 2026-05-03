%--------------------------------------------------------------------------
% File     : KGC711-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 2 (or): one cross-pair Compatible [BCP47]
% Version  : 1.0
% English  : Proposition~\ref{prop:cross-disjunct} or-Compatible.
%           : One cross-pair has disjunct-level Compatible (matching
%           : language tag); rule_or(r1, r2) = compatible.
%           : 
%           : Setup:
%           : CS  = or(d1, d2):
%           : d1  = (language, eq, bcp:de)
%           : d2  = (language, eq, bcp:fr)
%           : CS' = or(d1p):
%           : d1p = (language, eq, bcp:de)
%           : 
%           : Cross-pairs:
%           : (d1, d1p): bcp:de vs bcp:de -- same tag; witness bcp_de;
%           : disjunct_compat.
%           : (d2, d1p): bcp:fr vs bcp:de -- BCP47 disjoint;
%           : disjunct_conflict (irrelevant for the verdict here).
%           : 
%           : By Proposition 2, some cross-pair Compatible suffices:
%           : rule_or(r1, r2) = compatible.
%           : 
%           : Conjecture (Style A): rule_or(r1, r2) = compatible.
%           : Expected: Theorem.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC711-1.p
%
% Status   : Theorem
% Verdict  : OrCompatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC711-policy.ttl
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
    ![X]: (in_denotation(X, c_d1p) <=> den_eq(X, bcp_de))).

% --- Disjunct-pair Compatible bridges ---
fof(d1_d1p_compat_bridge, axiom,
    (disjunct_compat(d1, d1p) <=> verdict_compatible(c_d1, c_d1p))).
fof(d2_d1p_compat_bridge, axiom,
    (disjunct_compat(d2, d1p) <=> verdict_compatible(c_d2, c_d1p))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc711, conjecture,
    rule_or(r1, r2) = compatible).
%--------------------------------------------------------------------------
