; -------------------------------------------------------------------------
; File     : KGC322-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : fileFormat, isAnyOf {ft:PDF, ft:PDFA1A} against eq ft:PDFA1A (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC322-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun ft_pdf () Concept)
(declare-fun ft_pdfa1a () Concept)
; Resource: nothing.  The verdict does not need it.
; witness condition asserted
(assert (! (or (and (or (= ft_pdf ft_pdf) (= ft_pdf ft_pdfa1a)) (= ft_pdf ft_pdfa1a))
    (and (or (= ft_pdfa1a ft_pdf) (= ft_pdfa1a ft_pdfa1a)) (= ft_pdfa1a ft_pdfa1a))) :named w_kgc322))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
