; -------------------------------------------------------------------------
; File     : KGC315-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isA dpv:Purpose against eq dpv:RIS (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC315-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun dpv_recruitment_interview_scheduling () Concept)
(declare-fun dpv_recruitment_interview_management () Concept)
(declare-fun dpv_recruitment_management () Concept)
(declare-fun dpv_personnel_hiring () Concept)
(declare-fun dpv_personnel_management () Concept)
(declare-fun dpv_human_resource_management () Concept)
(declare-fun dpv_purpose () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Resource: the six steps.  None of them asserts the chain.
(assert (! (kge_leq dpv_recruitment_interview_scheduling dpv_recruitment_interview_management) :named res_kgc315_0))
(assert (! (kge_leq dpv_recruitment_interview_management dpv_recruitment_management) :named res_kgc315_1))
(assert (! (kge_leq dpv_recruitment_management dpv_personnel_hiring) :named res_kgc315_2))
(assert (! (kge_leq dpv_personnel_hiring dpv_personnel_management) :named res_kgc315_3))
(assert (! (kge_leq dpv_personnel_management dpv_human_resource_management) :named res_kgc315_4))
(assert (! (kge_leq dpv_human_resource_management dpv_purpose) :named res_kgc315_5))
; witness condition asserted
(assert (! (or (and (kge_leq dpv_purpose dpv_purpose) (= dpv_purpose dpv_recruitment_interview_scheduling))
    (and (kge_leq dpv_recruitment_interview_scheduling dpv_purpose) (= dpv_recruitment_interview_scheduling dpv_recruitment_interview_scheduling))) :named w_kgc315))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
