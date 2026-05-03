%--------------------------------------------------------------------------
% File     : KGC300-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : language: eq bcp:de x eq bcp:fr -> Conflict
% Version  : 1.0
% English  : Offer:   (language, eq, bcp:de) -> [[c_offer]]   = {bcp:de}
%           : Request: (language, eq, bcp:fr) -> [[c_request]] = {bcp:fr}
%           : BCP 47 asserts kge_disjoint(bcp_de, bcp_fr) (registry
%           : uniqueness, RFC 5646 sec 2.2.1) -> verdict_conflict(c_offer,
%           : c_request)  [def:conflict, motivating example]
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC300-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC300-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations (no grounding failure).
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations: eq operator
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_eq(X, bcp_de))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_fr))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc300, conjecture,
    verdict_conflict(c_offer, c_request)).
%--------------------------------------------------------------------------
