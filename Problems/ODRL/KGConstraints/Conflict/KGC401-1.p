%--------------------------------------------------------------------------
% File     : KGC401-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : eq / Compatible: bcp:de x bcp:de
% Version  : 1.0
% English  : eq operator, Compatible verdict.  Both sides ground to
%           : bcp_de; reflexivity gives a witness.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC401-1.p
%
% Status   : Theorem
% Verdict  : Compatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC401-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_eq(X, bcp_de))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc401, conjecture,
    verdict_compatible(c_offer, c_request)).
%--------------------------------------------------------------------------
