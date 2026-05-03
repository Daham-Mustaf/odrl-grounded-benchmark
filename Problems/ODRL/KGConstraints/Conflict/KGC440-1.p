%--------------------------------------------------------------------------
% File     : KGC440-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isAnyOf / Conflict: isAnyOf {bcp:de, bcp:fr} x eq bcp:it
% Version  : 1.0
% English  : isAnyOf operator, Conflict verdict.  Offer's denotation is
%           : {bcp_de, bcp_fr}; request's is {bcp_it}.  BCP 47 asserts
%           : kge_disjoint pairwise across all language tags, so each list
%           : member is disjoint from bcp_it.  Pattern B2 (list-vs-eq) in
%           : DENOT000-0.ax fires: forced_empty(c_offer, c_request) follows
%           : from Assumption 1 applied pointwise to each list member.
%           : 
%           : FOF side: all five provers derive verdict_conflict as Theorem.
%           : SMT side: Z3 and cvc5 return unsat via direct list-membership
%           : and pairwise-distinctness reasoning.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC440-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC440-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% List membership for isAnyOf {bcp_de, bcp_fr}.
fof(in_list_de, axiom, in_list(bcp_de, list_de_fr)).
fof(in_list_fr, axiom, in_list(bcp_fr, list_de_fr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_de_fr) <=> (X = bcp_de | X = bcp_fr))).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isanyof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_it))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc440, conjecture,
    verdict_conflict(c_offer, c_request)).
%--------------------------------------------------------------------------
