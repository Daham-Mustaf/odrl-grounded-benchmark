%--------------------------------------------------------------------------
% File     : KGC422-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isPartOf / Unknown: isPartOf gn:Germany x eq gn:Strasbourg
% Version  : 1.0
% English  : isPartOf operator, Unknown verdict.  GeoNames asserts neither
%           : Strasbourg <= Germany nor disjointness; OWA gives Unknown.
%           : (In closed-world geography, Strasbourg is in France, but
%           : GeoNames doesn't assert sibling-country disjointness.)
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC422-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC422-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_ispartof(X, gn_germany))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, gn_strasbourg))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc422, conjecture,
    verdict_unknown(c_offer, c_request)).
%--------------------------------------------------------------------------
