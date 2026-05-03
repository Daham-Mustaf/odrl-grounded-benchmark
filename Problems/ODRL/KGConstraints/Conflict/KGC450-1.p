%--------------------------------------------------------------------------
% File     : KGC450-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : neq / Conflict: neq bcp:de x eq bcp:de
% Version  : 1.0
% English  : neq operator, Conflict verdict.  Offer's denotation is
%           : C \ {bcp_de} (every concept except bcp_de, restricted to
%           : the resource universe via kge_concept guard).  Request's
%           : denotation is {bcp_de}.  Intersection is empty by
%           : construction: the excluded value is exactly the eq target.
%           : Pattern B3 (neq-vs-eq) in DENOT000 fires structurally; no
%           : disjointness assertion is needed because the denotations
%           : are complementary by definition.
%           : 
%           : FOF side: all five provers derive verdict_conflict as Theorem.
%           : SMT side: Z3 and cvc5 return unsat via direct denotation
%           : membership reasoning.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC450-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC450-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_neq(X, bcp_de))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc450, conjecture,
    verdict_conflict(c_offer, c_request)).
%--------------------------------------------------------------------------
