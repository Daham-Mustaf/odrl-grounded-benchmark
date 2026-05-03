%--------------------------------------------------------------------------
% File     : KGC600-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 3 universal: static Conflict implies no request satisfies both [BCP 47]
% Version  : 1.0
% English  : Theorem 3 universal case. Demonstrates that a static Conflict
%           : verdict between c1 and c2 implies no runtime request R can
%           : satisfy both constraints simultaneously.
%           : 
%           : Setup:
%           : c1 = (language, eq, bcp:de)  =>  [c1] = {bcp_de}
%           : c2 = (language, eq, bcp:fr)  =>  [c2] = {bcp_fr}
%           : 
%           : Static side:
%           : Both denotations defined; intersection [c1] cap [c2] is empty
%           : and forced empty via BCP 47's kge_disjoint(bcp_de, bcp_fr).
%           : By verdict_conflict_def, verdict_conflict(c1, c2) holds.
%           : 
%           : Runtime side:
%           : operand_of(c1, language) and operand_of(c2, language) tie
%           : the constraints to the language operand.
%           : grounded_as_value functionality is asserted problem-locally:
%           : the runtime grounding map gamma is deterministic. This is
%           : not in RUNTIME000-0.ax because gamma is conceptually
%           : resource-side; we make the functionality assumption explicit
%           : here.
%           : No specific request is asserted: the conjecture quantifies
%           : universally over R.
%           : 
%           : Theorem 3 conclusion:
%           : ![R]: ~(satisfies(R, c1) & satisfies(R, c2)).
%           : Proof sketch: any R satisfying both would witness L, V, G
%           : for c1 and L', V', G' for c2. Both operand_of's force
%           : L = L' = language. omega_functional forces V = V'.
%           : grounded_as_value functionality forces G = G'. Then
%           : in_denotation(G, c1) and in_denotation(G, c2) requires
%           : G = bcp_de and G = bcp_fr, contradicting BCP47's distinct.
%           : 
%           : Conjecture style A: full implication.
%           : verdict_conflict(c1, c2) => ![R]: ~(sat(R, c1) & sat(R, c2)).
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC600-1.p
%
% Status   : Theorem
% Verdict  : RuntimeSoundness
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC600-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/RUNTIME000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Static-side wiring ---------------------------------------------------
fof(c1_defined, axiom, ~denotation_undef(c1)).
fof(c2_defined, axiom, ~denotation_undef(c2)).
fof(c1_den, axiom, ![X]: (in_denotation(X, c1) <=> den_eq(X, bcp_de))).
fof(c2_den, axiom, ![X]: (in_denotation(X, c2) <=> den_eq(X, bcp_fr))).

% --- Runtime hooks --------------------------------------------------------
fof(c1_operand, axiom, operand_of(c1, language)).
fof(c2_operand, axiom, operand_of(c2, language)).

% Functionality of operand_of: each constraint has at most one left operand.
% Per Definition 2 of the paper, a constraint is a triple (l, op, v_or_S);
% l is single-valued. Not axiomatized in RUNTIME000-0.ax (it's a structural
% property of the encoding, not the runtime layer); we assert it here.
fof(operand_of_functional, axiom,
    ![C, L1, L2]:
      ((operand_of(C, L1) & operand_of(C, L2))
        => L1 = L2)).

% Functionality of the runtime grounding map gamma.
% Definition 1 in the paper says gamma is a partial function: each value
% V maps to at most one concept G. RUNTIME000-0.ax does not axiomatize
% this; we assert it here so the proof can equate G witnesses across
% sat(R, c1) and sat(R, c2) for the same V.
fof(grounded_as_value_functional, axiom,
    ![V, G1, G2]:
      ((grounded_as_value(V, G1) & grounded_as_value(V, G2))
        => G1 = G2)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc600, conjecture,
    verdict_conflict(c1, c2)
       => (![R]: ~(satisfies(R, c1) & satisfies(R, c2)))).
%--------------------------------------------------------------------------
