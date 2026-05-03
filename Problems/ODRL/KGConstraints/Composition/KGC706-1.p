%--------------------------------------------------------------------------
% File     : KGC706-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 2 (and): paper Example 1 verbatim [GeoNames+DPV+BCP47]
% Version  : 1.0
% English  : Theorem 2 (and) audit of the paper's running Example 1
%           : (Section 3, Gaia-X cultural heritage scenario) verbatim. The
%           : three operand-pair verdicts are Compatible, Unknown, Conflict
%           : (Table 4 in the paper); under Strong Kleene AND, rule-level
%           : verdict is Conflict (one Conflict suffices).
%           : 
%           : Setup (paper Example 1, Table 3):
%           : Operand 1 (spatial, GeoNames):
%           : c_sp = (spatial, isPartOf, gn:Europe)        [offer]
%           : c'_sp = (spatial, eq, gn:France)             [request]
%           : France <= Europe in GeoNames; witness gn_france.
%           : => verdict_compatible(c_sp, c'_sp).
%           : 
%           : Operand 2 (purpose, DPV):
%           : c_pu  = (purpose, isA, dpv:NonCommercialPurpose)  [offer]
%           : c'_pu = (purpose, eq, dpv:ScientificResearch)     [request]
%           : DPV asserts only ScientificResearch skos:broader
%           : ResearchAndDevelopment; there is NO edge or disjointness
%           : between ScientificResearch and NonCommercialPurpose.
%           : Intersection is empty in the current state but not forced
%           : empty -- a future DPV release could add a skos:broader edge.
%           : Operand-pair verdict_unknown asserted as a premise (see
%           : KGC702 for rationale: Unknown is not positively derivable
%           : in FOL under OWA).
%           : => verdict_unknown(c_pu, c'_pu).
%           : 
%           : Operand 3 (language, BCP47):
%           : c_la  = (language, eq, bcp:de)               [offer]
%           : c'_la = (language, eq, bcp:fr)               [request]
%           : BCP47 asserts kge_disjoint(bcp_de, bcp_fr) by registry
%           : uniqueness; B1 pattern fires forced_empty.
%           : => verdict_conflict(c_la, c'_la).
%           : 
%           : Bridges:
%           : has_conflict(r1) holds (operand 3 is Conflict).
%           : 
%           : Strong Kleene AND: rule_and(R) = conflict <=> has_conflict(R).
%           : rule_and(r1) = conflict.
%           : 
%           : Conjecture (Style A): rule_and(r1) = conflict.
%           : Expected: Theorem.
%           : 
%           : Why this audit matters:
%           : This is the paper's lead motivating example. Without an
%           : empirical audit, the framework's flagship claim ('the three
%           : yield three different verdicts, composing under and to
%           : rule-level Conflict') is unverified. KGC706 closes that gap.
%           : The audit covers all three Strong Kleene operand-level cases
%           : (Compatible, Unknown, Conflict) in a single problem, against
%           : three different resource kinds (knowledge graph, taxonomy,
%           : flat registry) and three different operators (isPartOf, isA,
%           : eq).
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC706-1.p
%
% Status   : Theorem
% Verdict  : AndConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC706-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/COMPOSE000-0.ax').
include('Axioms/GN000-0.ax').
include('Axioms/DPV000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Operand 1 pair (spatial, GeoNames): Compatible ---
fof(c1_off_defined, axiom, ~denotation_undef(c1_off)).
fof(c1_req_defined, axiom, ~denotation_undef(c1_req)).
fof(c1_off_den, axiom,
    ![X]: (in_denotation(X, c1_off) <=> den_ispartof(X, gn_europe))).
fof(c1_req_den, axiom,
    ![X]: (in_denotation(X, c1_req) <=> den_eq(X, gn_france))).

% Operand 1 verdict: positively derivable (witness gn_france in both
% denotations via kge_leq(gn_france, gn_europe) for the offer side).
% Asserted explicitly for symmetry with the Unknown premise below.
fof(c1_compat_premise, axiom,
    verdict_compatible(c1_off, c1_req)).

% --- Operand 2 pair (purpose, DPV): Unknown ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_isa(X, dpv_non_commercial_purpose))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_eq(X, dpv_scientific_research))).

% Operand 2 verdict: Unknown is the OWA meta-claim that DPV is silent
% on ScientificResearch vs NonCommercialPurpose. Per the DPV TTL
% source, ScientificResearch's only parent is ResearchAndDevelopment;
% no skos:broader edge connects ScientificResearch to
% NonCommercialPurpose. The intersection of denotations is empty in
% the current state but not forced empty. Asserted as a premise
% because verdict_unknown under OWA is not positively derivable in FOL
% (see KGC702 audit notes).
fof(c2_unknown_premise, axiom,
    verdict_unknown(c2_off, c2_req)).

% --- Operand 3 pair (language, BCP47): Conflict ---
fof(c3_off_defined, axiom, ~denotation_undef(c3_off)).
fof(c3_req_defined, axiom, ~denotation_undef(c3_req)).
fof(c3_off_den, axiom,
    ![X]: (in_denotation(X, c3_off) <=> den_eq(X, bcp_de))).
fof(c3_req_den, axiom,
    ![X]: (in_denotation(X, c3_req) <=> den_eq(X, bcp_fr))).

% Operand 3 verdict: Conflict, positively derivable from
% kge_disjoint(bcp_de, bcp_fr) via B1 forced_empty pattern.
% No premise needed; verdict_conflict_def derives it directly from
% the BCP47000-0.ax disjointness fact.

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
fof(kgc706, conjecture,
    rule_and(r1) = conflict).
%--------------------------------------------------------------------------
