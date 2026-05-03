; --------------------------------------------------------------------------
; File     : KGC502-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Lemma 1 verdict-asymmetry: Compatible does NOT propagate through refinement [GeoNames]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC502-1.smt2
; Status   : sat
; Verdict  : CompatibleNonPropagation
; Comments : Verdict: CompatibleNonPropagation  Category: Refinement  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_germany () Concept)
(declare-fun gn_europe  () Concept)
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
; GN000: parentFeature edges.
(assert (kge_leq gn_germany gn_europe))
(assert (kge_leq gn_france  gn_europe))
; Identity.
(assert (distinct gn_germany gn_europe gn_france))
;
; No SDA loaded: GeoNames asserts no kge_disjoint between Germany and
; France. The Compatible-analog implication has a model where the
; antecedents hold (refinement, Compatible premise) but the conclusion
; (verdict_compatible(c1, c3)) does not. SMT cross-check: Z3 returns
; sat -- no contradiction can be derived.
;
; The full Compatible-analog implication is tested in the FOF encoding
; via REFINE000-0.ax's refines_def and DENOT000-0.ax's
; verdict_compatible_def. The SMT side asserts only the resource axioms
; and confirms consistency.
(check-sat)
(exit)
