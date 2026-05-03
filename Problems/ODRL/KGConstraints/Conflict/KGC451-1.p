%--------------------------------------------------------------------------
% File     : KGC451-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : neq / Compatible: neq bcp:de x eq bcp:fr
% Version  : 1.0
% English  : neq operator, Compatible verdict.  Offer's denotation is
%           : C \ {bcp_de} (every concept except bcp_de).  Request's
%           : denotation is {bcp_fr}.  Witness: bcp_fr is in C \ {bcp_de}
%           : (since bcp_fr != bcp_de by BCP 47 registry uniqueness) AND
%           : in {bcp_fr}, providing a common element.  The kge_concept
%           : guard is satisfied because bcp_fr is asserted as a concept
%           : in BCP47000.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC451-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC451-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_neq(X, bcp_de))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_fr))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc451, conjecture,
    verdict_compatible(c_offer, c_request)).
%--------------------------------------------------------------------------
