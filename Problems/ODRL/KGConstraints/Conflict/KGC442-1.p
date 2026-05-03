%--------------------------------------------------------------------------
% File     : KGC442-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isAnyOf / Unknown: isAnyOf {dpv:SR, dpv:CR} x eq dpv:NCP
% Version  : 1.0
% English  : isAnyOf operator, Unknown verdict.  Offer's list is
%           : {ScientificResearch, CommercialResearch}; request is
%           : {NonCommercialPurpose}.  DPV asserts neither equality
%           : (witness) nor disjointness (forced); OWA gives Unknown.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC442-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC442-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/DPV000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

fof(in_list_sr, axiom, in_list(dpv_scientific_research, list_sr_cr)).
fof(in_list_cr, axiom, in_list(dpv_commercial_research, list_sr_cr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_sr_cr) <=>
            (X = dpv_scientific_research | X = dpv_commercial_research))).

fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isanyof(X, list_sr_cr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, dpv_non_commercial_purpose))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc442, conjecture,
    verdict_unknown(c_offer, c_request)).
%--------------------------------------------------------------------------
