; -------------------------------------------------------------------------
; File     : KGC300-2.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : language, eq bcp:de against eq bcp:fr (witness condition negated)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC300-2.smt2
; Status   : sat
; Comments : Query 2 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
; Background theory: registry uniqueness, as distinctness.
(assert (! (distinct bcp_de bcp_fr) :named bt_kgc300_0))
; witness condition negated
(assert (! (not (or (and (= bcp_de bcp_de) (= bcp_de bcp_fr))
    (and (= bcp_fr bcp_de) (= bcp_fr bcp_fr)))) :named w_kgc300))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
