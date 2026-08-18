; -------------------------------------------------------------------------
; File     : KGC320-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : fileFormat, eq ft:PDF against eq ft:PDFA1A (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC320-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun ft_pdf () Concept)
(declare-fun ft_pdfa1a () Concept)
; Resource: nothing.  228 concepts, no relations between any of them.
; witness condition asserted
(assert (! (or (and (= ft_pdf ft_pdf) (= ft_pdf ft_pdfa1a))
    (and (= ft_pdfa1a ft_pdf) (= ft_pdfa1a ft_pdfa1a))) :named w_kgc320))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
