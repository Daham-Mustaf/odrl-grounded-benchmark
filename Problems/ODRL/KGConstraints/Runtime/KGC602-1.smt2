; --------------------------------------------------------------------------
; File     : KGC602-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Default-deny: undef-grounded constraint admits no satisfying request [BCP 47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC602-1.smt2
; Status   : unsat
; Verdict  : RuntimeSoundness
; Comments : Verdict: RuntimeSoundness  Category: Runtime  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Constraint 0)
(declare-fun c_undef () Constraint)
(declare-fun denotation_undef (Constraint) Bool)
; SMT side directly tests the default-deny conclusion via the
; denotation_undef predicate.  satisfies(_, c_undef) requires
; ~denotation_undef(c_undef), which contradicts the asserted fact.
(assert (denotation_undef c_undef))
;
; A request satisfies c_undef only if denotation_undef does not hold.
; The negation of the conjecture asserts a witness; combined with the
; above, contradiction follows immediately.
(declare-fun sat_witness () Bool)
(assert (=> sat_witness (not (denotation_undef c_undef))))
(assert sat_witness)
(check-sat)
(exit)
