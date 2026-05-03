%--------------------------------------------------------------------------
% File     : KGC430-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : hasPart / Conflict: hasPart bcp:de x eq bcp:fr
% Version  : 1.0
% English  : hasPart operator, Conflict verdict. FOF-encoding incomplete,
%           : SMT-encoding complete.
%           : 
%           : FOF side: hasPart denotes an upward cone of bcp_de.  Neither
%           : the B1 (downward-pair) nor the B2 (list-vs-eq) pattern in
%           : DENOT000-0.ax covers upward cones, so forced_empty does not
%           : fire.  Vampire and E return CounterSatisfiable.  This
%           : documents the remaining FOF-encoding gap relative to
%           : Definition 7.
%           : 
%           : SMT side: the hand-rolled encoding bypasses forced_empty and
%           : uses kge_disjoint_propagation directly. With reflexivity
%           : kge_leq(bcp_de, bcp_de) and the witness assertion
%           : kge_leq(bcp_de, bcp_fr), propagation instantiated at
%           : (a=bcp_de, b=bcp_fr, z=bcp_de) derives false. Z3 and cvc5
%           : return unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC430-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Conflict
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC430-policy.ttl
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
    ![X]: (in_denotation(X, c_offer)   <=> den_haspart(X, bcp_de))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_fr))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc430, conjecture,
    verdict_conflict(c_offer, c_request)).
%--------------------------------------------------------------------------
