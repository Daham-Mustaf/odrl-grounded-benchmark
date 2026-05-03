%--------------------------------------------------------------------------
% File     : KGC713-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : xone conservative reduction: xone-Conflict via or-Conflict [BCP47]
% Version  : 1.0
% English  : xone conservative reduction (paper Section 4.3 footnote):
%           : xone-Conflict is taken as or-Conflict over the same
%           : disjuncts, since xone-satisfaction implies or-satisfaction.
%           : If every cross-pair has atomic-Conflict, no request
%           : satisfies any xone-disjunct alongside c'.
%           : 
%           : Setup:
%           : CS  = xone(c1, c2, c3):
%           : c1 = (language, eq, bcp:de)
%           : c2 = (language, eq, bcp:fr)
%           : c3 = (language, eq, bcp:es)
%           : CS' = (language, eq, bcp:it).
%           : 
%           : Conservative reduction: treat xone-rule's disjuncts as
%           : or-disjuncts for the purpose of Conflict detection.
%           : Disjunct membership for r1 includes d1, d2, d3.
%           : 
%           : Cross-pairs:
%           : (d1, d1p): bcp:de vs bcp:it -- BCP47 disjoint; Conflict.
%           : (d2, d1p): bcp:fr vs bcp:it -- BCP47 disjoint; Conflict.
%           : (d3, d1p): bcp:es vs bcp:it -- BCP47 disjoint; Conflict.
%           : 
%           : All three cross-pairs Conflict; by Proposition 2 applied
%           : to the conservative or-reduction of xone, rule_or = conflict.
%           : 
%           : This problem reuses the or-encoding (rule_or, has_disjunct,
%           : disjunct_conflict) without new axioms, in line with the
%           : paper's claim that xone-Conflict requires no machinery
%           : beyond or.
%           : 
%           : Conjecture (Style A): rule_or(r1, r2) = conflict.
%           : Expected: Theorem.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC713-1.p
%
% Status   : Theorem
% Verdict  : XoneConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC713-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/COMPOSE001-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Disjunct membership (xone treated as or for Conflict reduction) ---
fof(r1_disjunct_d1,  axiom, has_disjunct(r1, d1)).
fof(r1_disjunct_d2,  axiom, has_disjunct(r1, d2)).
fof(r1_disjunct_d3,  axiom, has_disjunct(r1, d3)).
fof(r2_disjunct_d1p, axiom, has_disjunct(r2, d1p)).

fof(r1_closure, axiom,
    ![D]: (has_disjunct(r1, D) <=> (D = d1 | D = d2 | D = d3))).
fof(r2_closure, axiom,
    ![D]: (has_disjunct(r2, D) <=> D = d1p)).

fof(disjuncts_distinct, axiom,
    d1 != d2 & d1 != d3 & d2 != d3 &
    d1 != d1p & d2 != d1p & d3 != d1p).

% --- Atomic-level constraint denotations per disjunct ---
fof(c_d1_defined, axiom, ~denotation_undef(c_d1)).
fof(c_d1_den, axiom,
    ![X]: (in_denotation(X, c_d1) <=> den_eq(X, bcp_de))).

fof(c_d2_defined, axiom, ~denotation_undef(c_d2)).
fof(c_d2_den, axiom,
    ![X]: (in_denotation(X, c_d2) <=> den_eq(X, bcp_fr))).

fof(c_d3_defined, axiom, ~denotation_undef(c_d3)).
fof(c_d3_den, axiom,
    ![X]: (in_denotation(X, c_d3) <=> den_eq(X, bcp_es))).

fof(c_d1p_defined, axiom, ~denotation_undef(c_d1p)).
fof(c_d1p_den, axiom,
    ![X]: (in_denotation(X, c_d1p) <=> den_eq(X, bcp_it))).

% --- Disjunct-pair Conflict bridges ---
fof(d1_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d1, d1p) <=> verdict_conflict(c_d1, c_d1p))).
fof(d2_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d2, d1p) <=> verdict_conflict(c_d2, c_d1p))).
fof(d3_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d3, d1p) <=> verdict_conflict(c_d3, c_d1p))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc713, conjecture,
    rule_or(r1, r2) = conflict).
%--------------------------------------------------------------------------
