; -------------------------------------------------------------------------
; File     : KGC301-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : purpose, isA dpv:NCP against eq dpv:SR (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL. Under submission.
; Source   : TODO repository URL
; Authors  : TODO Author Names
; Names    : KGC301-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research  () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, restricted to the named concepts.
(assert (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose))
(assert (kge_leq dpv_scientific_research  dpv_scientific_research))
; The vocabulary says nothing further.  No negative assertion is made.
; witness condition negated
(assert (not (or (and (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose) (= dpv_non_commercial_purpose dpv_scientific_research))
    (and (kge_leq dpv_scientific_research  dpv_non_commercial_purpose) (= dpv_scientific_research  dpv_scientific_research)))))
(check-sat)
(exit)
