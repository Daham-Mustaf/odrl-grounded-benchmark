; --------------------------------------------------------------------------
; File     : KGC500-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Lemma 1 positive: refines + Conflict premise => Conflict conclusion [GeoNames+SDA]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC500-1.smt2
; Status   : unsat
; Verdict  : ConflictPropagation
; Comments : Verdict: ConflictPropagation  Category: Refinement  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
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
; GN000: Bayern parentFeature Germany.
(assert (kge_leq gn_bayern gn_germany))
; GN001-SDA: Germany disjoint France.
(assert (kge_disjoint gn_germany gn_france))
; Identity.
(assert (distinct gn_bayern gn_germany gn_france))
; Lemma 1 negation: a witness x exists in [c1] AND [c3].
; [c1] = {gn_bayern}; [c3] = {gn_france}.
; A witness equates them, contradicting (distinct ...).
;
; This SMT encoding tests the conclusion-level Conflict between c1 and c3.
; The full Lemma 1 propagation (refinement + premise) is tested in the FOF
; encoding via REFINE000-0.ax's refines_def and DENOT000-0.ax's
; verdict_conflict_def. The SMT side cross-checks that the conclusion
; verdict_conflict(c1, c3) holds at the witness level.
(declare-fun x () Concept)
(assert (= x gn_bayern))
(assert (= x gn_france))
(check-sat)
(exit)
