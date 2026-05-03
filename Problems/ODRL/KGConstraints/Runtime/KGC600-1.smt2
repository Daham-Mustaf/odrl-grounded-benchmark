; --------------------------------------------------------------------------
; File     : KGC600-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Theorem 3 universal: static Conflict implies no request satisfies both [BCP 47]
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC600-1.smt2
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
; This SMT encoding tests the conclusion-level Conflict between c1 and c2
; on a witness basis, not the full universal Theorem 3 statement.
; Theorem 3's universal quantifier over requests R, the operand_of /
; grounded_as_value indirection, and the satisfies_def biconditional are
; tested in the FOF encoding via RUNTIME000-0.ax.
;
; Witness query: a single x in both [c1] and [c2] (i.e., x = bcp_de and
; x = bcp_fr). Contradicts (distinct bcp_de bcp_fr). Z3 returns unsat.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))
(check-sat)
(exit)
