; --------------------------------------------------------------------------
; File     : KGC430-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : hasPart / Conflict: hasPart bcp:de x eq bcp:fr
; Version  : 1.0
; Authors  : .
; Refs     : ()
; Source   : 
; Names    : KGC430-1.smt2
; Status   : unsat
; Verdict  : Conflict
; Comments : Verdict: Conflict  Category: Conflict  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
; hasPart bcp_de denotes upward cone of bcp_de.
; eq bcp_fr denotes {bcp_fr}.
; Witness x: x is above bcp_de AND x = bcp_fr.
; After substitution: kge_leq(bcp_de, bcp_fr). Combined with reflexivity
; kge_leq(bcp_de, bcp_de) and kge_disjoint(bcp_de, bcp_fr), propagation
; instantiated at (a=bcp_de, b=bcp_fr, z=bcp_de) derives false. Unsat.
(declare-fun x () Concept)
(assert (kge_leq bcp_de x))
(assert (= x bcp_fr))
(check-sat)
(exit)
