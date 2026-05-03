%--------------------------------------------------------------------------
% File     : KGC812-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: Assumption 1 violation [boundary — inconsistent extension]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) BOUNDARY audit: extensions
%           : violating Assumption 1 (disjointness propagation coherence)
%           : are correctly detected as inconsistent.
%           : 
%           : Setup:
%           : R: BCP47-like, with two concepts and asserted disjointness.
%           : in_concepts_R(bcp_de), in_concepts_R(bcp_fr).
%           : disjoint_R(bcp_de, bcp_fr).
%           : 
%           : Extension R' (Assumption 1 violation):
%           : Add concept bcp_z (R'-only) with subsumption edges to BOTH
%           : bcp_de AND bcp_fr:
%           : leq_R_prime(bcp_z, bcp_de)
%           : leq_R_prime(bcp_z, bcp_fr)
%           : This violates Assumption 1: bcp_de and bcp_fr are
%           : disjoint, but bcp_z is a common subordinate. The
%           : propagation axiom kge_disjoint_propagation_R_prime forces
%           : contradiction.
%           : 
%           : Conjecture: $false.
%           : Expected: Theorem.
%           : 
%           : Why: closure axiom extension_disjoint lifts disjoint_R(de, fr)
%           : to disjoint_R_prime(de, fr). The R'-axioms include both
%           : leq_R_prime(z, de) and leq_R_prime(z, fr). The propagation
%           : axiom in R' (kge_disjoint_propagation_R_prime) states that
%           : this configuration is impossible, deriving $false.
%           : 
%           : This audit demonstrates that the framework correctly
%           : rejects inconsistent extensions: an evaluator hitting this
%           : configuration knows immediately that Assumption 1 has been
%           : violated by the resource update.
%           : 
%           : SMT cross-check: same configuration. Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC812-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityAssumption1Boundary
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC812-policy.ttl
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
% R-facts: BCP47-like, two disjoint concepts.
% ============================================================
fof(r_de_in_concepts, axiom,
    in_concepts_R(bcp_de)).

fof(r_fr_in_concepts, axiom,
    in_concepts_R(bcp_fr)).

fof(r_de_disjoint_fr, axiom,
    disjoint_R(bcp_de, bcp_fr)).

fof(r_distinct_de_fr, axiom,
    bcp_de != bcp_fr).

% ============================================================
% R' extension: ASSUMPTION 1 VIOLATION
% Add bcp_z as a common subordinate of two disjoint concepts.
% This is internally inconsistent under the kge_disjoint_propagation
% axiom, which the framework expects to detect.
% ============================================================
fof(r_ext_z_in_concepts_prime, axiom,
    in_concepts_R_prime(bcp_z)).

fof(r_ext_z_not_in_concepts_R, axiom,
    ~in_concepts_R(bcp_z)).

fof(r_ext_z_leq_de_prime, axiom,
    leq_R_prime(bcp_z, bcp_de)).

fof(r_ext_z_leq_fr_prime, axiom,
    leq_R_prime(bcp_z, bcp_fr)).

fof(r_ext_distinct_z_de, axiom,
    bcp_z != bcp_de).

fof(r_ext_distinct_z_fr, axiom,
    bcp_z != bcp_fr).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc812, conjecture,
    $false).
%--------------------------------------------------------------------------
