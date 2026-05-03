%--------------------------------------------------------------------------
% File     : KGC501-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Lemma 1 non-creation: refines holds, premise NOT Conflict, conclusion not derivable [DPV]
% Version  : 1.0
% English  : Lemma 1 non-creation: refinement preserves Conflict but does
%           : NOT manufacture it where the lemma's hypothesis fails.
%           : 
%           : Setup:
%           : c1 = (purpose, eq,  dpv:ScientificResearch)
%           : => [c1] = {dpv_scientific_research}
%           : c2 = (purpose, isA, dpv:Purpose)
%           : => [c2] = downward cone of dpv_purpose
%           : ⊇ {ScientificResearch, Marketing, ...}
%           : c3 = (purpose, eq,  dpv:Marketing)
%           : => [c3] = {dpv_marketing}
%           : 
%           : Refinement holds: ScientificResearch is below Purpose in DPV,
%           : so [c1] = {SR} subseteq downward cone of Purpose = [c2].
%           : Asserted as axiom under Style B.
%           : 
%           : Premise verdict_conflict(c2, c3) does NOT hold: Marketing is
%           : in the cone of Purpose (kge_leq(dpv_marketing, dpv_purpose) is
%           : asserted in DPV000-0.ax), so [c2] cap [c3] = {Marketing} is
%           : non-empty. The pair (c2, c3) is Compatible, not Conflict.
%           : 
%           : Bare conclusion verdict_conflict(c1, c3): DPV asserts no
%           : kge_disjoint between ScientificResearch and Marketing, and the
%           : denotations [c1] = {SR} and [c3] = {Marketing} do not share
%           : a witness. Under OWA, verdict(c1, c3) = Unknown; the
%           : verdict_conflict(c1, c3) conjecture is not derivable.
%           : Vampire returns CounterSatisfiable; Z3 returns sat.
%           : 
%           : Conjecture style B: the bare conclusion is the conjecture; the
%           : antecedent refines(c1, c2) is inserted as an axiom. A Style A
%           : implication conjecture would be vacuously Theorem (false
%           : antecedent: verdict_conflict(c2, c3) does not hold), which
%           : tests classical implication, not the encoding's behavior.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC501-1.p
%
% Status   : CounterSatisfiable
% Verdict  : NoConflictCreation
% SPC      : FOF_CSA_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC501-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/REFINE000-0.ax').
include('Axioms/DPV000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Three constraint tokens with defined denotations.
fof(c1_defined, axiom, ~denotation_undef(c1)).
fof(c2_defined, axiom, ~denotation_undef(c2)).
fof(c3_defined, axiom, ~denotation_undef(c3)).

% Denotations
fof(c1_den, axiom, ![X]: (in_denotation(X, c1) <=> den_eq(X, dpv_scientific_research))).
fof(c2_den, axiom, ![X]: (in_denotation(X, c2) <=> den_isa(X, dpv_purpose))).
fof(c3_den, axiom, ![X]: (in_denotation(X, c3) <=> den_eq(X, dpv_marketing))).

% Lemma 1 antecedent: refines(c1, c2). Asserted as axiom (Style B).
% This is licensed by [c1] = {ScientificResearch} subseteq [c2] = downward
% cone of Purpose, since DPV asserts kge_leq(SR, Purpose).
fof(refines_premise, axiom, refines(c1, c2)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc501, conjecture,
    verdict_conflict(c1, c3)).
%--------------------------------------------------------------------------
