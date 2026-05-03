%--------------------------------------------------------------------------
% File     : KGC441-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isAnyOf / Compatible: isAnyOf {bcp:de, bcp:fr} x eq bcp:de
% Version  : 1.0
% English  : isAnyOf operator, Compatible verdict.  Offer's list contains
%           : bcp_de; request equals bcp_de; bcp_de is the witness.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC441-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC441-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_isanyof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc441, conjecture,
    verdict_compatible(c_offer, c_request)).
%--------------------------------------------------------------------------
