; --------------------------------------------------------------------------
; File     : KGC601-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 3 concrete request: r0 satisfies c1, must NOT satisfy c2 [BCP 47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC601-1.smt2
; Status   : unsat
; Verdict  : RuntimeSoundness
; Comments : Verdict: RuntimeSoundness  Category: Runtime  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000 load-bearing axioms.
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
;
; SMT scope: as in KGC600, the SMT side cross-checks the conclusion-level
; Conflict between c1 and c2. The full runtime chain (operand_of,
; omega_assigns, grounded_as_value, satisfies_def) is tested in FOF only.
;
; Witness query: a single x in both [c1] and [c2]. Contradicts
; (distinct bcp_de bcp_fr).
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))
(check-sat)
(exit)
