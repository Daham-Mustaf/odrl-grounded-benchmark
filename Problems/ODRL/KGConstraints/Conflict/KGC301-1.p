%--------------------------------------------------------------------------
% File     : KGC301-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : purpose: isA dpv:NonCommercialPurpose x eq dpv:ScientificResearch -> Unknown
% Version  : 1.0
% English  : Offer:   (purpose, isA, dpv:NonCommercialPurpose)
%           : Request: (purpose, eq,  dpv:ScientificResearch)
%           : DPV asserts neither ScientificResearch <= NonCommercialPurpose
%           : NOR kge_disjoint between them. Open-world: silence is not
%           : evidence either way. The conjecture asks for verdict_unknown,
%           : which is not entailed (a model exists where SR <= NCP makes
%           : Compatible), so the expected status is CounterSatisfiable.
%           : [def:conflict, motivating example, OWA]
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC301-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC301-policy.ttl
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
    ![X]: (in_denotation(X, c_request) <=> den_eq (X, dpv_scientific_research))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc301, conjecture,
    verdict_unknown(c_offer, c_request)).
%--------------------------------------------------------------------------
