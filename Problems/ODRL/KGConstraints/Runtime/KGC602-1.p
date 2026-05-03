%--------------------------------------------------------------------------
% File     : KGC602-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Default-deny: undef-grounded constraint admits no satisfying request [BCP 47]
% Version  : 1.0
% English  : Default-deny corner case. Tests that the runtime layer
%           : correctly refuses to satisfy any constraint whose denotation
%           : is undefined.
%           : 
%           : Setup:
%           : c_undef is a constraint over the language operand whose
%           : right-operand value did not ground successfully (e.g., a
%           : typo or deprecated tag like bcp:xz). Its denotation is
%           : undef.
%           : 
%           : Per Definition 4 of the paper, an undef denotation must
%           : yield denotation_undef(c_undef) -- asserted directly here
%           : rather than derived from a denotation bridge.
%           : 
%           : Default-deny via satisfies_def:
%           : satisfies(R, c_undef) requires ~denotation_undef(c_undef)
%           : as one of its conjuncts. Since denotation_undef(c_undef)
%           : is asserted, the conjunct fails for any R, L, V, G witness
%           : combination. Hence ~satisfies(R, c_undef) for all R.
%           : 
%           : This is the only problem in the audit grid that exercises
%           : the undef branch of satisfies_def. The operand-level audit
%           : always asserts ~denotation_undef.
%           : 
%           : Conjecture style A: universal closure ![R]: ~sat(R, c_undef).
%           : No functionality axioms or concrete request needed -- the
%           : default-deny fires before any L/V/G witnesses are reached.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC602-1.p
%
% Status   : Theorem
% Verdict  : RuntimeSoundness
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC602-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/RUNTIME000-0.ax').
include('Axioms/BCP47000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% --- Static-side wiring ---------------------------------------------------
% c_undef's right-operand value does not ground; per Definition 4,
% denotation(c_undef) = undef.  Asserted directly (no denotation bridge).
fof(c_undef_undef, axiom, denotation_undef(c_undef)).

% --- Runtime hooks --------------------------------------------------------
% operand_of/2: c_undef's left operand is language.
fof(c_undef_operand, axiom, operand_of(c_undef, language)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc602, conjecture,
    ![R]: ~satisfies(R, c_undef)).
%--------------------------------------------------------------------------
