%--------------------------------------------------------------------------
% File     : KGC500-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Lemma 1 positive: refines + Conflict premise => Conflict conclusion [GeoNames+SDA]
% Version  : 1.0
% English  : Lemma 1 positive case. Demonstrates that Conflict propagates
%           : downward through refinement, using a structural (non-trivial)
%           : refinement over GeoNames + SDA profile.
%           : 
%           : Setup:
%           : c1 = (spatial, eq,        gn:Bayern)
%           : => [c1] = {gn_bayern}
%           : c2 = (spatial, isPartOf,  gn:Germany)
%           : => [c2] = downward cone of gn_germany
%           : = {Germany, Bayern, Berlin, Baden-Wuerttemberg}
%           : c3 = (spatial, eq,        gn:France)
%           : => [c3] = {gn_france}
%           : 
%           : Refinement:  [c1] = {Bayern} subseteq [c2] (Bayern <= Germany).
%           : Real downward-cone inclusion, not identity.
%           : Premise:     verdict_conflict(c2, c3) holds. SDA asserts
%           : kge_disjoint(gn_germany, gn_france); B1 pattern
%           : fires for ([c2], [c3]) via ancestor pair
%           : (gn_germany, gn_france) -- forced empty.
%           : Conclusion:  same ancestor pair certifies forced_empty for
%           : ([c1], [c3]) since [c1] is below gn_germany.
%           : verdict_conflict(c1, c3) follows.
%           : 
%           : Conjecture style A: the implication itself is the Theorem to derive.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC500-1.p
%
% Status   : Theorem
% Verdict  : ConflictPropagation
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC500-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/REFINE000-0.ax').
include('Axioms/GN000-0.ax').
include('Axioms/GN001-SDA-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Three constraint tokens with defined denotations.
fof(c1_defined, axiom, ~denotation_undef(c1)).
fof(c2_defined, axiom, ~denotation_undef(c2)).
fof(c3_defined, axiom, ~denotation_undef(c3)).

% Denotations
fof(c1_den, axiom, ![X]: (in_denotation(X, c1) <=> den_eq(X, gn_bayern))).
fof(c2_den, axiom, ![X]: (in_denotation(X, c2) <=> den_ispartof(X, gn_germany))).
fof(c3_den, axiom, ![X]: (in_denotation(X, c3) <=> den_eq(X, gn_france))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc500, conjecture,
    (refines(c1, c2) & verdict_conflict(c2, c3))
       => verdict_conflict(c1, c3)).
%--------------------------------------------------------------------------
