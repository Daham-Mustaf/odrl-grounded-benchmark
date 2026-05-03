%--------------------------------------------------------------------------
% File     : KGC460-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isNoneOf / Conflict: isNoneOf {bcp:de, bcp:fr} x eq bcp:de
% Version  : 1.0
% English  : isNoneOf operator, Conflict verdict.  Offer's denotation is
%           : C \ {bcp_de, bcp_fr} (every concept except those on the
%           : list).  Request's denotation is {bcp_de}.  Since bcp_de
%           : is on the excluded list, it cannot be in offer's denotation,
%           : and the intersection is empty by construction.  Pattern B4
%           : (isNoneOf-vs-eq) in DENOT000 fires structurally.
%           : 
%           : FOF side: all five provers derive verdict_conflict as Theorem.
%           : SMT side: Z3 and cvc5 return unsat via direct list-membership
%           : and complement reasoning.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC460-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC460-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% List membership for isNoneOf {bcp_de, bcp_fr}.
fof(in_list_de, axiom, in_list(bcp_de, list_de_fr)).
fof(in_list_fr, axiom, in_list(bcp_fr, list_de_fr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_de_fr) <=> (X = bcp_de | X = bcp_fr))).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isnoneof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc460, conjecture,
    verdict_conflict(c_offer, c_request)).
%--------------------------------------------------------------------------
