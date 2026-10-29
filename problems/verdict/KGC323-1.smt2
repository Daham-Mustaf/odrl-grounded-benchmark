; -------------------------------------------------------------------------
; File     : KGC323-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : fileFormat, neq ft:PDF against eq ft:PDFA1A, under a declared distinctness (witness condition asserted)
; Version  : 1.0
; Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
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
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
; Declared distinctness this problem adopts, named as the TPTP
; side names it.
(assert (! (not (= ft_pdf ft_pdfa1a)) :named bg_dist_ft_pdf_distinct_ft_pdfa1a))
; witness condition asserted
(assert (! (or (and (not (= ft_pdf ft_pdf)) (= ft_pdf ft_pdfa1a)) (and (not (= ft_pdfa1a ft_pdf)) (= ft_pdfa1a ft_pdfa1a))) :named w_kgc323))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
