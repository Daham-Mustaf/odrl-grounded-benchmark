%--------------------------------------------------------------------------
% File     : KGC411-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isA / Compatible: isA dpv:Purpose x eq dpv:ScientificResearch
% Version  : 1.0
% English  : isA operator, Compatible verdict.  Offer's downward cone
%           : of dpv:Purpose contains every DPV purpose; request's
%           : ScientificResearch is one such purpose, providing a witness.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC411-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC411-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/DPV000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isa(X, dpv_purpose))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, dpv_scientific_research))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc411, conjecture,
    verdict_compatible(c_offer, c_request)).
%--------------------------------------------------------------------------
