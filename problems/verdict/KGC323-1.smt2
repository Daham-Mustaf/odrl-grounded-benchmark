; -------------------------------------------------------------------------
; File     : KGC323-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : fileFormat, neq ft:PDF against eq ft:PDFA1A, under a declared distinctness (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC323-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun ft_pdf () Concept)
(declare-fun ft_pdfa1a () Concept)
; Resource: no order relation between the file-type concepts.
; Background theory: ft:PDF and ft:PDFA1A are declared distinct.
(assert (! (distinct ft_pdf ft_pdfa1a) :named bt_kgc323_0))
; witness condition asserted
(assert (! (or (and (not (= ft_pdf ft_pdf)) (= ft_pdf ft_pdfa1a))
    (and (not (= ft_pdfa1a ft_pdf)) (= ft_pdfa1a ft_pdfa1a))) :named w_kgc323))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
