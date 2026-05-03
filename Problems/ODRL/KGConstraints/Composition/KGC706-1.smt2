; --------------------------------------------------------------------------
; File     : KGC706-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 2 (and): paper Example 1 verbatim [GeoNames+DPV+BCP47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC706-1.smt2
; Status   : unsat
; Verdict  : AndConflict
; Comments : Verdict: AndConflict  Category: Composition  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
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
; GeoNames: France below Europe.
(assert (kge_leq gn_france gn_europe))
; DPV: no edge or disjointness asserted between SR and NonCommercial.
; (SR's only parent in DPV is ResearchAndDevelopment, which we omit
;  here since it is irrelevant to operand 2's empty-but-not-forced
;  intersection.)
; BCP47: de disjoint fr.
(assert (kge_disjoint bcp_de bcp_fr))
; Identity.
(assert (distinct gn_europe gn_france
                  dpv_non_commercial_purpose dpv_scientific_research
                  bcp_de bcp_fr))
;
; SMT cross-check: at the Conflict-bearing operand (language), the
; forced-emptiness check refutes a shared concept x assigned both
; bcp_de and bcp_fr.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))
(check-sat)
(exit)
