; --------------------------------------------------------------------------
; File     : KGC700-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 2 (and): Conflict aggregation [GeoNames+SDA, BCP47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC700-1.smt2
; Status   : unsat
; Verdict  : AndConflict
; Comments : Verdict: AndConflict  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
(declare-fun bcp_de     () Concept)
(declare-fun bcp_fr     () Concept)
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
; GN000 + SDA: Bayern below Germany; Germany disjoint France.
(assert (kge_leq gn_bayern gn_germany))
(assert (kge_disjoint gn_germany gn_france))
; BCP47: de disjoint fr.
(assert (kge_disjoint bcp_de bcp_fr))
; Identity.
(assert (distinct gn_bayern gn_germany gn_france bcp_de bcp_fr))
;
; SMT cross-check at the conclusion level: each operand-pair's
; forced-emptiness holds. The full rule-level aggregation via
; COMPOSE000's Strong Kleene rule is FOF-only (SMT does not encode
; rule_and explicitly).
(declare-fun x () Concept)
(assert (= x gn_bayern))
(assert (= x gn_france))
(check-sat)
(exit)
