%--------------------------------------------------------------------------
% File     : KGC431-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : hasPart / Compatible: hasPart gn:France x eq gn:Europe
% Version  : 1.0
% English  : hasPart operator, Compatible verdict.  Offer's upward cone
%           : of France contains Europe (France <= Europe in GeoNames);
%           : Europe is the witness.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC431-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC431-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_haspart(X, gn_france))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, gn_europe))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc431, conjecture,
    verdict_compatible(c_offer, c_request)).
%--------------------------------------------------------------------------
