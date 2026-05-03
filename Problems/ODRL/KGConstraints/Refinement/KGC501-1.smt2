; --------------------------------------------------------------------------
; File     : KGC501-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Lemma 1 non-creation: refines holds, premise NOT Conflict, conclusion not derivable [DPV]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC501-1.smt2
; Status   : sat
; Verdict  : NoConflictCreation
; Comments : Verdict: NoConflictCreation  Category: Refinement  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_marketing           () Concept)
(declare-fun dpv_purpose             () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; DPV000: ScientificResearch and Marketing are both DPV purposes,
; with no asserted equality and no asserted disjointness.
(assert (kge_leq dpv_scientific_research dpv_purpose))
(assert (kge_leq dpv_marketing           dpv_purpose))
; Identity.
(assert (distinct dpv_scientific_research
                  dpv_marketing
                  dpv_purpose))
;
; Under these axioms there is no derivation of a witness in
; [c1] cap [c3], and there is no derivation of forced-empty for the
; pair. The corresponding FOF conjecture verdict_conflict(c1, c3) is
; CounterSatisfiable. Z3 returns sat: the axioms are consistent and
; admit a model where Conflict is not forced.
(check-sat)
(exit)
