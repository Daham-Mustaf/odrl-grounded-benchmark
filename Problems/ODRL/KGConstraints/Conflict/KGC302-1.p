%--------------------------------------------------------------------------
% File     : KGC302-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : spatial: isPartOf gn:Europe x eq gn:France -> Compatible
% Version  : 1.0
% English  : Offer:   (spatial, isPartOf, gn:Europe) -> [[c_offer]]   contains downward cone of gn:Europe
%           : Request: (spatial, eq,       gn:France) -> [[c_request]] = {gn:France}
%           : GeoNames asserts kge_leq(gn_france, gn_europe), so gn:France
%           : is in the offer's denotation: witness exists ->
%           : verdict_compatible(c_offer, c_request)
%           : [def:conflict, motivating example]
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC302-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC302-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/GN000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_ispartof(X, gn_europe))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq      (X, gn_france))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc302, conjecture,
    verdict_compatible(c_offer, c_request)).
%--------------------------------------------------------------------------
