%--------------------------------------------------------------------------
% File     : KGC810-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: complement counterexample [Remark 2 — neq]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) BOUNDARY audit: complement
%           : operators are NOT preserved under resource extension.
%           : Demonstrates Remark 2 empirically — c_neq verdicts can flip
%           : from Conflict to Compatible under concept addition, which is
%           : why Proposition 1 explicitly restricts to monotone operators.
%           : 
%           : Setup:
%           : R: BCP47-shaped flat registry with two concepts.
%           : in_concepts_R(bcp_de), in_concepts_R(bcp_fr).
%           : grounded_as_R(bcp_de, bcp_de),
%           : grounded_as_R(bcp_fr, bcp_fr).
%           : 
%           : Constraints:
%           : c1 = c_neq(bcp_de)  [denotation: concepts != de]
%           : c2 = c_neq(bcp_fr)  [denotation: concepts != fr]
%           : R-verdict: verdict_conflict_R(c1, c2).
%           : [c1]_R = {bcp_fr}, [c2]_R = {bcp_de}, intersection empty.
%           : Forced empty in R because no concept other than de or fr
%           : exists in R.
%           : 
%           : Extension R' (concept addition):
%           : Add concept bcp_es. Now [c1]_R' = {bcp_fr, bcp_es},
%           : [c2]_R' = {bcp_de, bcp_es}. Intersection = {bcp_es}.
%           : 
%           : Conjecture (Style B): verdict_conflict_R_prime(c1, c2).
%           : Expected: CounterSatisfiable.
%           : 
%           : Why: bcp_es satisfies BOTH complement constraints (it is
%           : != de AND != fr), giving a witness in [c1]_R' \cap [c2]_R'.
%           : The Conflict from R does NOT survive in R'. This concrete
%           : counterexample justifies Remark 2's restriction of
%           : Proposition 1 to monotone operators.
%           : 
%           : The denotation rule den_neq_R requires both in_concepts(X)
%           : AND ~grounded_as(X, g). The concept-membership guard is
%           : essential here: without it, the prover could hallucinate
%           : Skolem witnesses outside the concept set, masking the
%           : counterexample.
%           : 
%           : SMT cross-check: assert R-facts and R'-extension. The witness
%           : bcp_es is in both denotations under R'. Resource is
%           : consistent with verdict_compatible holding. Expected: sat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC810-1.p
%
% Status   : CounterSatisfiable
% Verdict  : MonotonicityComplementBoundary
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC810-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/MONO000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% ============================================================
% KGE000 lifted to R
% ============================================================
fof(kge_leq_reflexive_R, axiom,
    ![X]: leq_R(X, X)).

fof(kge_leq_transitive_R, axiom,
    ![X, Y, Z]:
      ((leq_R(X, Y) & leq_R(Y, Z)) => leq_R(X, Z))).

fof(kge_leq_antisymmetric_R, axiom,
    ![X, Y]:
      ((leq_R(X, Y) & leq_R(Y, X)) => X = Y)).

fof(kge_disjoint_symmetric_R, axiom,
    ![X, Y]:
      (disjoint_R(X, Y) => disjoint_R(Y, X))).

fof(kge_disjoint_irreflexive_R, axiom,
    ![X]: ~disjoint_R(X, X)).

fof(kge_disjoint_propagation_R, axiom,
    ![A, B, Z]:
      ((disjoint_R(A, B) & leq_R(Z, A) & leq_R(Z, B))
       => $false)).

% ============================================================
% KGE000 lifted to R' (same axioms, `_R_prime` suffix)
% ============================================================
fof(kge_leq_reflexive_R_prime, axiom,
    ![X]: leq_R_prime(X, X)).

fof(kge_leq_transitive_R_prime, axiom,
    ![X, Y, Z]:
      ((leq_R_prime(X, Y) & leq_R_prime(Y, Z))
       => leq_R_prime(X, Z))).

fof(kge_leq_antisymmetric_R_prime, axiom,
    ![X, Y]:
      ((leq_R_prime(X, Y) & leq_R_prime(Y, X)) => X = Y)).

fof(kge_disjoint_symmetric_R_prime, axiom,
    ![X, Y]:
      (disjoint_R_prime(X, Y) => disjoint_R_prime(Y, X))).

fof(kge_disjoint_irreflexive_R_prime, axiom,
    ![X]: ~disjoint_R_prime(X, X)).

fof(kge_disjoint_propagation_R_prime, axiom,
    ![A, B, Z]:
      ((disjoint_R_prime(A, B) & leq_R_prime(Z, A)
        & leq_R_prime(Z, B))
       => $false)).

% ============================================================
% DENOT000 lifted to R: per-operator denotation rules
% Constraint terms: c_eq/1, c_isa/1, c_ispartof/1, c_haspart/1.
% ============================================================
fof(den_eq_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_eq(G)) <=> grounded_as_R(X, G))).

fof(den_isa_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_isa(G)) <=> leq_R(X, G))).

fof(den_ispartof_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_ispartof(G)) <=> leq_R(X, G))).

fof(den_haspart_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_haspart(G)) <=> leq_R(G, X))).

% ============================================================
% DENOT000 lifted to R'
% ============================================================
fof(den_eq_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_eq(G)) <=>
       grounded_as_R_prime(X, G))).

fof(den_isa_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_isa(G)) <=>
       leq_R_prime(X, G))).

fof(den_ispartof_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_ispartof(G)) <=>
       leq_R_prime(X, G))).

fof(den_haspart_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_haspart(G)) <=>
       leq_R_prime(G, X))).

% ============================================================
% Forced-emptiness lifted to R and R'
% ============================================================
fof(forced_empty_R_def, axiom,
    ![C1, C2]:
      (forced_empty_R(C1, C2) <=>
       (![X]: ~(in_denotation_R(X, C1) & in_denotation_R(X, C2))))).

fof(forced_empty_R_prime_def, axiom,
    ![C1, C2]:
      (forced_empty_R_prime(C1, C2) <=>
       (![X]: ~(in_denotation_R_prime(X, C1)
                & in_denotation_R_prime(X, C2))))).

% ============================================================
% Verdict definitions lifted to R and R'
% ============================================================
fof(verdict_compatible_intro_R, axiom,
    ![C1, C2, X]:
      ((in_denotation_R(X, C1) & in_denotation_R(X, C2))
       => verdict_compatible_R(C1, C2))).
fof(verdict_conflict_intro_R, axiom,
    ![C1, C2]:
      (forced_empty_R(C1, C2) => verdict_conflict_R(C1, C2))).
      
fof(verdict_compatible_intro_R_prime, axiom,
    ![C1, C2, X]:
      ((in_denotation_R_prime(X, C1) & in_denotation_R_prime(X, C2))
       => verdict_compatible_R_prime(C1, C2))).
       
fof(verdict_conflict_intro_R_prime, axiom,
    ![C1, C2]:
      (forced_empty_R_prime(C1, C2) => verdict_conflict_R_prime(C1, C2))).

% ============================================================
% Monotone-operator guard (Remark 2 fragment)
% Excludes neq and isNoneOf; their denotations C \ {g} are not
% monotone in leq or disjoint. Asserted on each constraint term used
% in the conjectures of monotone-fragment problems.
% ============================================================
fof(monotone_op_eq, axiom,
    ![G]: monotone_op(c_eq(G))).

fof(monotone_op_isa, axiom,
    ![G]: monotone_op(c_isa(G))).

fof(monotone_op_ispartof, axiom,
    ![G]: monotone_op(c_ispartof(G))).

fof(monotone_op_haspart, axiom,
    ![G]: monotone_op(c_haspart(G))).

% ============================================================
% den_neq lifted to R and R' with concept-membership guard.
% This is essential for the boundary audit: complement operators
% reference the complement of the concept set, so denotation
% membership must require in_concepts/1 to prevent the prover from
% hallucinating Skolem witnesses outside the concept set.
% ============================================================
fof(den_neq_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_neq(G)) <=>
       (in_concepts_R(X) & ~grounded_as_R(X, G)))).

fof(den_neq_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_neq(G)) <=>
       (in_concepts_R_prime(X) & ~grounded_as_R_prime(X, G)))).

% ============================================================
% R-facts: BCP47-shaped registry with exactly two concepts.
% Closed-world for R: the only concepts are de and fr.
% ============================================================
fof(r_de_in_concepts, axiom,
    in_concepts_R(bcp_de)).

fof(r_fr_in_concepts, axiom,
    in_concepts_R(bcp_fr)).

fof(r_de_grounded, axiom,
    grounded_as_R(bcp_de, bcp_de)).

fof(r_fr_grounded, axiom,
    grounded_as_R(bcp_fr, bcp_fr)).

% Closed-world enumeration for R: only de and fr are in_concepts_R.
fof(r_concepts_closed, axiom,
    ![X]: (in_concepts_R(X) <=> (X = bcp_de | X = bcp_fr))).

fof(r_distinct_de_fr, axiom,
    bcp_de != bcp_fr).

% ============================================================
% R' extension: add concept bcp_es. R-facts auto-lift via MONO000.
% ============================================================
fof(r_ext_es_in_concepts_prime, axiom,
    in_concepts_R_prime(bcp_es)).

fof(r_ext_es_not_in_concepts_R, axiom,
    ~in_concepts_R(bcp_es)).

fof(r_ext_es_grounded, axiom,
    grounded_as_R_prime(bcp_es, bcp_es)).

fof(r_ext_distinct_es_de, axiom,
    bcp_es != bcp_de).

fof(r_ext_distinct_es_fr, axiom,
    bcp_es != bcp_fr).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc810, conjecture,
    verdict_conflict_R_prime(c_neq(bcp_de), c_neq(bcp_fr))).
%--------------------------------------------------------------------------
