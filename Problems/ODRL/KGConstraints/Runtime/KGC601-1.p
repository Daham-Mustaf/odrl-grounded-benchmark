%--------------------------------------------------------------------------
% File     : KGC601-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Theorem 3 concrete request: r0 satisfies c1, must NOT satisfy c2 [BCP 47]
% Version  : 1.0
% English  : Theorem 3 specialized to a concrete request. Demonstrates that
%           : a runtime request witnessing one constraint of a Conflict pair
%           : is forbidden from witnessing the other.
%           : 
%           : Setup:
%           : c1 = (language, eq, bcp:de)  =>  [c1] = {bcp_de}
%           : c2 = (language, eq, bcp:fr)  =>  [c2] = {bcp_fr}
%           : verdict_conflict(c1, c2) holds via BCP 47 disjointness.
%           : 
%           : Concrete request:
%           : r0 assigns the language operand the value val_de.
%           : val_de grounds to the concept bcp_de.
%           : 
%           : Theorem 3 specialization:
%           : satisfies(r0, c1) holds: witnesses L = language, V = val_de,
%           : G = bcp_de; in_denotation(bcp_de, c1) holds since
%           : [c1] = {bcp_de}.
%           : ~satisfies(r0, c2) must hold: any L', V', G' witnesses must
%           : equal language, val_de, bcp_de via the three functionality
%           : axioms, then in_denotation(bcp_de, c2) requires
%           : bcp_de = bcp_fr, contradicting BCP47 distinctness.
%           : 
%           : Conjecture style A: conjunctive (positive + negative). Tests
%           : the runtime layer on a single concrete witness rather than
%           : universally.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC601-1.p
%
% Status   : Theorem
% Verdict  : RuntimeSoundness
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC601-policy.ttl
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

fof(operand_of_functional, axiom,
    ![C, L1, L2]:
      ((operand_of(C, L1) & operand_of(C, L2))
        => L1 = L2)).

fof(grounded_as_value_functional, axiom,
    ![V, G1, G2]:
      ((grounded_as_value(V, G1) & grounded_as_value(V, G2))
        => G1 = G2)).

% --- Concrete request r0 --------------------------------------------------
% r0 assigns the language operand the value val_de;
% gamma grounds val_de to bcp_de.
fof(r0_assigns,         axiom, omega_assigns(r0, language, val_de)).
fof(val_de_grounds,     axiom, grounded_as_value(val_de, bcp_de)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc601, conjecture,
    satisfies(r0, c1) & ~satisfies(r0, c2)).
%--------------------------------------------------------------------------
