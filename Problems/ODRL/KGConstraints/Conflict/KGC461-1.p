%--------------------------------------------------------------------------
% File     : KGC461-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isNoneOf / Compatible: isNoneOf {bcp:de, bcp:fr} x eq bcp:it
% Version  : 1.0
% English  : isNoneOf operator, Compatible verdict.  Offer's denotation
%           : is C \ {bcp_de, bcp_fr}.  Request's denotation is {bcp_it}.
%           : Witness: bcp_it is in C \ {bcp_de, bcp_fr} (since bcp_it
%           : is distinct from both list members by BCP 47 registry
%           : uniqueness) AND in {bcp_it}, providing a common element.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC461-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC461-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

fof(in_list_de, axiom, in_list(bcp_de, list_de_fr)).
fof(in_list_fr, axiom, in_list(bcp_fr, list_de_fr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_de_fr) <=> (X = bcp_de | X = bcp_fr))).

fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isnoneof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_it))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc461, conjecture,
    verdict_compatible(c_offer, c_request)).
%--------------------------------------------------------------------------
