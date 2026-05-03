%--------------------------------------------------------------------------
% File     : KGC502-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Lemma 1 verdict-asymmetry: Compatible does NOT propagate through refinement [GeoNames]
% Version  : 1.0
% English  : Lemma 1 verdict-asymmetry. Lemma 1 is stated for Conflict only.
%           : The Compatible-analog -- 'c1 refines c2 AND verdict(c2, c3) =
%           : Compatible ==> verdict(c1, c3) = Compatible' -- is FALSE in
%           : general. KGC502 demonstrates this with a concrete counterexample.
%           : 
%           : Setup:
%           : c1 = (spatial, eq,        gn:Germany)
%           : => [c1] = {gn_germany}
%           : c2 = (spatial, isPartOf,  gn:Europe)
%           : => [c2] = downward cone of gn_europe
%           : ⊇ {Europe, Germany, France, Bayern, ...}
%           : c3 = (spatial, eq,        gn:France)
%           : => [c3] = {gn_france}
%           : 
%           : Refinement: [c1] = {Germany} subseteq [c2] (Germany <= Europe
%           : in GeoNames).  Real downward-cone inclusion.
%           : Premise:    verdict_compatible(c2, c3) holds. France is in the
%           : cone of Europe (kge_leq(gn_france, gn_europe) in
%           : GN000-0.ax), so [c2] cap [c3] = {France} -- a
%           : non-empty witness exists.
%           : 
%           : Compatible-analog conclusion verdict_compatible(c1, c3) FAILS:
%           : [c1] cap [c3] = {Germany} cap {France} = empty.
%           : No witness exists in the intersection.
%           : Under OWA without SDA: verdict(c1, c3) = Unknown.
%           : Under SDA:             verdict(c1, c3) = Conflict.
%           : In neither case:       verdict(c1, c3) = Compatible.
%           : 
%           : Refinement narrowed [c1] from [c2] but did not preserve the
%           : common satisfier. This is the structural reason Lemma 1 is
%           : one-directional: Conflict propagates, Compatible does not.
%           : 
%           : Conjecture style A: the Compatible-analog implication is the
%           : conjecture. Vampire returns CounterSatisfiable: a model exists
%           : where the antecedents hold but the conclusion does not.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC502-1.p
%
% Status   : CounterSatisfiable
% Verdict  : CompatibleNonPropagation
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC502-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/REFINE000-0.ax').
include('Axioms/GN000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Three constraint tokens with defined denotations.
fof(c1_defined, axiom, ~denotation_undef(c1)).
fof(c2_defined, axiom, ~denotation_undef(c2)).
fof(c3_defined, axiom, ~denotation_undef(c3)).

% Denotations
fof(c1_den, axiom, ![X]: (in_denotation(X, c1) <=> den_eq(X, gn_germany))).
fof(c2_den, axiom, ![X]: (in_denotation(X, c2) <=> den_ispartof(X, gn_europe))).
fof(c3_den, axiom, ![X]: (in_denotation(X, c3) <=> den_eq(X, gn_france))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc502, conjecture,
    (refines(c1, c2) & verdict_compatible(c2, c3))
       => verdict_compatible(c1, c3)).
%--------------------------------------------------------------------------
