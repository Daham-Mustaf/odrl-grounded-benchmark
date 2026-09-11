; -------------------------------------------------------------------------
; File     : KGC392-1.smt2
; Domain   : ODRL Policy / Knowledge-Grounded Fragment
; Problem  : spatial, isNoneOf {loc:WF} against eq loc:WF-UV, ISO rule (witness condition asserted)
; Version  : 1.0
; Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
; Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
; Authors  : Daham Mustafa
; Names    : KGC392-1.smt2
; Status   : sat
; Comments : Query 1 of 2.  Verdict is derived from both queries.
; -------------------------------------------------------------------------

(set-logic UF)
(set-option :produce-unsat-cores true)
(set-option :produce-models true)
(declare-sort Concept 0)
(declare-fun loc_wf () Concept)
(declare-fun loc_wf_uv () Concept)
(declare-fun loc_fr_wf () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (! (forall ((x Concept)) (kge_leq x x)) :named ax_leq_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))) :named ax_leq_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))) :named ax_leq_transitive))
(assert (! (kge_leq loc_wf_uv loc_wf) :named res_loc_wf_uv_within_loc_wf))
(assert (! (kge_leq loc_fr_wf loc_wf) :named res_loc_fr_wf_same_loc_wf))
(assert (! (kge_leq loc_wf loc_fr_wf) :named res_loc_wf_same_loc_fr_wf))
; Instances of the registry rule this problem adopts, named as
; the TPTP side names them.
(assert (! (not (= loc_wf_uv loc_wf)) :named bg_dist_loc_wf_uv_loc_wf))
; witness condition asserted
(assert (! (or (and (not (= loc_wf loc_wf)) (= loc_wf loc_wf_uv)) (and (not (= loc_wf_uv loc_wf)) (= loc_wf_uv loc_wf_uv))) :named w_kgc392))
(check-sat)
(get-unsat-core)
(get-model)
(exit)
