%--------------------------------------------------------------------------
% File     : KGC412-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isA / Unknown: isA dpv:NonCommercialPurpose x eq dpv:ScientificResearch
% Version  : 1.0
% English  : isA operator, Unknown verdict.  This is the motivating
%           : example's purpose pair: DPV silent on ScientificResearch
%           : <= NonCommercialPurpose; OWA gives Unknown.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC412-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC412-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_isa(X, dpv_non_commercial_purpose))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, dpv_scientific_research))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc412, conjecture,
    verdict_unknown(c_offer, c_request)).
%--------------------------------------------------------------------------
