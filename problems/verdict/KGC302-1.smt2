; -------------------------------------------------------------------------
; File     : KGC302-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isPartOf gn:Europe against eq gn:France (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC302-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, restricted to the named concepts.
(assert (kge_leq gn_europe gn_europe))
(assert (kge_leq gn_france gn_france))
; Resource: France is within Europe.
(assert (kge_leq gn_france gn_europe))
; witness condition asserted
(assert (or (and (kge_leq gn_europe gn_europe) (= gn_europe gn_france))
    (and (kge_leq gn_france gn_europe) (= gn_france gn_france))))
(check-sat)
(exit)
