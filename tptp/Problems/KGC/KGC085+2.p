%------------------------------------------------------------------------------
% File     : KGC085+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Distribute in both Dutch and French against distribute in Dutch only: some use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The two versions have the
%            same status.
% English  : A Belgian federal publisher requires distribution in both Dutch
%            and French. The licensee distributes in Dutch only. The registry
%            rule that different primary subtags name different languages is
%            adopted. This problem states that some use meets the two
%            policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC376-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC376 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC085) and that no use does (KGC086). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+1.ax').

fof(bg_dist_bcp47_nl_fr, axiom,
    bcp_nl != bcp_fr).

fof(bg_dist_bcp47_nl_bg, axiom,
    bcp_nl != bcp_bg).

fof(bg_dist_bcp47_nl_cs, axiom,
    bcp_nl != bcp_cs).

fof(bg_dist_bcp47_nl_da, axiom,
    bcp_nl != bcp_da).

fof(bg_dist_bcp47_nl_de, axiom,
    bcp_nl != bcp_de).

fof(bg_dist_bcp47_nl_el, axiom,
    bcp_nl != bcp_el).

fof(bg_dist_bcp47_nl_en, axiom,
    bcp_nl != bcp_en).

fof(bg_dist_bcp47_nl_es, axiom,
    bcp_nl != bcp_es).

fof(bg_dist_bcp47_nl_fi, axiom,
    bcp_nl != bcp_fi).

fof(bg_dist_bcp47_nl_hu, axiom,
    bcp_nl != bcp_hu).

fof(bg_dist_bcp47_nl_it, axiom,
    bcp_nl != bcp_it).

fof(bg_dist_bcp47_nl_pl, axiom,
    bcp_nl != bcp_pl).

fof(bg_dist_bcp47_nl_pt, axiom,
    bcp_nl != bcp_pt).

fof(bg_dist_bcp47_nl_sv, axiom,
    bcp_nl != bcp_sv).

fof(bg_dist_bcp47_fr_bg, axiom,
    bcp_fr != bcp_bg).

fof(bg_dist_bcp47_fr_cs, axiom,
    bcp_fr != bcp_cs).

fof(bg_dist_bcp47_fr_da, axiom,
    bcp_fr != bcp_da).

fof(bg_dist_bcp47_fr_de, axiom,
    bcp_fr != bcp_de).

fof(bg_dist_bcp47_fr_el, axiom,
    bcp_fr != bcp_el).

fof(bg_dist_bcp47_fr_en, axiom,
    bcp_fr != bcp_en).

fof(bg_dist_bcp47_fr_es, axiom,
    bcp_fr != bcp_es).

fof(bg_dist_bcp47_fr_fi, axiom,
    bcp_fr != bcp_fi).

fof(bg_dist_bcp47_fr_hu, axiom,
    bcp_fr != bcp_hu).

fof(bg_dist_bcp47_fr_it, axiom,
    bcp_fr != bcp_it).

fof(bg_dist_bcp47_fr_pl, axiom,
    bcp_fr != bcp_pl).

fof(bg_dist_bcp47_fr_pt, axiom,
    bcp_fr != bcp_pt).

fof(bg_dist_bcp47_fr_sv, axiom,
    bcp_fr != bcp_sv).

fof(bg_dist_bcp47_bg_cs, axiom,
    bcp_bg != bcp_cs).

fof(bg_dist_bcp47_bg_da, axiom,
    bcp_bg != bcp_da).

fof(bg_dist_bcp47_bg_de, axiom,
    bcp_bg != bcp_de).

fof(bg_dist_bcp47_bg_el, axiom,
    bcp_bg != bcp_el).

fof(bg_dist_bcp47_bg_en, axiom,
    bcp_bg != bcp_en).

fof(bg_dist_bcp47_bg_es, axiom,
    bcp_bg != bcp_es).

fof(bg_dist_bcp47_bg_fi, axiom,
    bcp_bg != bcp_fi).

fof(bg_dist_bcp47_bg_hu, axiom,
    bcp_bg != bcp_hu).

fof(bg_dist_bcp47_bg_it, axiom,
    bcp_bg != bcp_it).

fof(bg_dist_bcp47_bg_pl, axiom,
    bcp_bg != bcp_pl).

fof(bg_dist_bcp47_bg_pt, axiom,
    bcp_bg != bcp_pt).

fof(bg_dist_bcp47_bg_sv, axiom,
    bcp_bg != bcp_sv).

fof(bg_dist_bcp47_cs_da, axiom,
    bcp_cs != bcp_da).

fof(bg_dist_bcp47_cs_de, axiom,
    bcp_cs != bcp_de).

fof(bg_dist_bcp47_cs_el, axiom,
    bcp_cs != bcp_el).

fof(bg_dist_bcp47_cs_en, axiom,
    bcp_cs != bcp_en).

fof(bg_dist_bcp47_cs_es, axiom,
    bcp_cs != bcp_es).

fof(bg_dist_bcp47_cs_fi, axiom,
    bcp_cs != bcp_fi).

fof(bg_dist_bcp47_cs_hu, axiom,
    bcp_cs != bcp_hu).

fof(bg_dist_bcp47_cs_it, axiom,
    bcp_cs != bcp_it).

fof(bg_dist_bcp47_cs_pl, axiom,
    bcp_cs != bcp_pl).

fof(bg_dist_bcp47_cs_pt, axiom,
    bcp_cs != bcp_pt).

fof(bg_dist_bcp47_cs_sv, axiom,
    bcp_cs != bcp_sv).

fof(bg_dist_bcp47_da_de, axiom,
    bcp_da != bcp_de).

fof(bg_dist_bcp47_da_el, axiom,
    bcp_da != bcp_el).

fof(bg_dist_bcp47_da_en, axiom,
    bcp_da != bcp_en).

fof(bg_dist_bcp47_da_es, axiom,
    bcp_da != bcp_es).

fof(bg_dist_bcp47_da_fi, axiom,
    bcp_da != bcp_fi).

fof(bg_dist_bcp47_da_hu, axiom,
    bcp_da != bcp_hu).

fof(bg_dist_bcp47_da_it, axiom,
    bcp_da != bcp_it).

fof(bg_dist_bcp47_da_pl, axiom,
    bcp_da != bcp_pl).

fof(bg_dist_bcp47_da_pt, axiom,
    bcp_da != bcp_pt).

fof(bg_dist_bcp47_da_sv, axiom,
    bcp_da != bcp_sv).

fof(bg_dist_bcp47_de_el, axiom,
    bcp_de != bcp_el).

fof(bg_dist_bcp47_de_en, axiom,
    bcp_de != bcp_en).

fof(bg_dist_bcp47_de_es, axiom,
    bcp_de != bcp_es).

fof(bg_dist_bcp47_de_fi, axiom,
    bcp_de != bcp_fi).

fof(bg_dist_bcp47_de_hu, axiom,
    bcp_de != bcp_hu).

fof(bg_dist_bcp47_de_it, axiom,
    bcp_de != bcp_it).

fof(bg_dist_bcp47_de_pl, axiom,
    bcp_de != bcp_pl).

fof(bg_dist_bcp47_de_pt, axiom,
    bcp_de != bcp_pt).

fof(bg_dist_bcp47_de_sv, axiom,
    bcp_de != bcp_sv).

fof(bg_dist_bcp47_el_en, axiom,
    bcp_el != bcp_en).

fof(bg_dist_bcp47_el_es, axiom,
    bcp_el != bcp_es).

fof(bg_dist_bcp47_el_fi, axiom,
    bcp_el != bcp_fi).

fof(bg_dist_bcp47_el_hu, axiom,
    bcp_el != bcp_hu).

fof(bg_dist_bcp47_el_it, axiom,
    bcp_el != bcp_it).

fof(bg_dist_bcp47_el_pl, axiom,
    bcp_el != bcp_pl).

fof(bg_dist_bcp47_el_pt, axiom,
    bcp_el != bcp_pt).

fof(bg_dist_bcp47_el_sv, axiom,
    bcp_el != bcp_sv).

fof(bg_dist_bcp47_en_es, axiom,
    bcp_en != bcp_es).

fof(bg_dist_bcp47_en_fi, axiom,
    bcp_en != bcp_fi).

fof(bg_dist_bcp47_en_hu, axiom,
    bcp_en != bcp_hu).

fof(bg_dist_bcp47_en_it, axiom,
    bcp_en != bcp_it).

fof(bg_dist_bcp47_en_pl, axiom,
    bcp_en != bcp_pl).

fof(bg_dist_bcp47_en_pt, axiom,
    bcp_en != bcp_pt).

fof(bg_dist_bcp47_en_sv, axiom,
    bcp_en != bcp_sv).

fof(bg_dist_bcp47_es_fi, axiom,
    bcp_es != bcp_fi).

fof(bg_dist_bcp47_es_hu, axiom,
    bcp_es != bcp_hu).

fof(bg_dist_bcp47_es_it, axiom,
    bcp_es != bcp_it).

fof(bg_dist_bcp47_es_pl, axiom,
    bcp_es != bcp_pl).

fof(bg_dist_bcp47_es_pt, axiom,
    bcp_es != bcp_pt).

fof(bg_dist_bcp47_es_sv, axiom,
    bcp_es != bcp_sv).

fof(bg_dist_bcp47_fi_hu, axiom,
    bcp_fi != bcp_hu).

fof(bg_dist_bcp47_fi_it, axiom,
    bcp_fi != bcp_it).

fof(bg_dist_bcp47_fi_pl, axiom,
    bcp_fi != bcp_pl).

fof(bg_dist_bcp47_fi_pt, axiom,
    bcp_fi != bcp_pt).

fof(bg_dist_bcp47_fi_sv, axiom,
    bcp_fi != bcp_sv).

fof(bg_dist_bcp47_hu_it, axiom,
    bcp_hu != bcp_it).

fof(bg_dist_bcp47_hu_pl, axiom,
    bcp_hu != bcp_pl).

fof(bg_dist_bcp47_hu_pt, axiom,
    bcp_hu != bcp_pt).

fof(bg_dist_bcp47_hu_sv, axiom,
    bcp_hu != bcp_sv).

fof(bg_dist_bcp47_it_pl, axiom,
    bcp_it != bcp_pl).

fof(bg_dist_bcp47_it_pt, axiom,
    bcp_it != bcp_pt).

fof(bg_dist_bcp47_it_sv, axiom,
    bcp_it != bcp_sv).

fof(bg_dist_bcp47_pl_pt, axiom,
    bcp_pl != bcp_pt).

fof(bg_dist_bcp47_pl_sv, axiom,
    bcp_pl != bcp_sv).

fof(bg_dist_bcp47_pt_sv, axiom,
    bcp_pt != bcp_sv).

fof(w_kgc376, axiom,
    bcp_fr = bcp_nl).
%------------------------------------------------------------------------------
