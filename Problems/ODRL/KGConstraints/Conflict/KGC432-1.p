%--------------------------------------------------------------------------
% File     : KGC432-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : hasPart / Unknown: hasPart gn:Strasbourg x eq gn:Germany
% Version  : 1.0
% English  : hasPart operator, Unknown verdict.  Offer's upward cone of
%           : Strasbourg in GeoNames goes through Bas-Rhin -> Grand Est ->
%           : France -> Europe.  Germany is not on this chain, but
%           : GeoNames asserts no disjointness; OWA gives Unknown.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC432-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC432-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_haspart(X, gn_strasbourg))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, gn_germany))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc432, conjecture,
    verdict_unknown(c_offer, c_request)).
%--------------------------------------------------------------------------
