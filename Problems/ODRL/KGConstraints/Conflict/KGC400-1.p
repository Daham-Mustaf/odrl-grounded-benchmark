%--------------------------------------------------------------------------
% File     : KGC400-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : eq / Conflict: bcp:de x bcp:fr
% Version  : 1.0
% English  : eq operator, Conflict verdict.  BCP 47 asserts
%           : kge_disjoint(bcp_de, bcp_fr); the eq/eq pair has empty
%           : intersection forced by registry uniqueness.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC400-1.p
%
% Status   : Theorem
% Verdict  : Conflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC400-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_eq(X, bcp_de))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_fr))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc400, conjecture,
    verdict_conflict(c_offer, c_request)).
%--------------------------------------------------------------------------
