%------------------------------------------------------------------------------
% File     : KGC080+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Distribute in German only against distribute in any language except French: no use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The versions have the
%            same status.
% English  : As KGC374, without the registry rule. This problem states that no
%            use meets the two policies. It is also a check of KGC379: A
%            licence for a single-language edition allows exactly one of
%            German and French. The licensee publishes in German. There it
%            states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC375-2 [Mus26]
%          : KGC379-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : This problem is 2 checks whose formulas and include lines are the
%            same after renaming the case. KGC375 is Unknown. Its two problems
%            state that some use meets the two policies (KGC079) and that no
%            use does (KGC080); here the first is Satisfiable and the second
%            Satisfiable. KGC379 is Unknown. Its two problems state that some
%            use meets the two policies (KGC079) and that no use does
%            (KGC080); here the first is Satisfiable and the second
%            Satisfiable. A pair of policies is Incompatible when the first is
%            Unsatisfiable, Compatible when the second is Unsatisfiable, and
%            Unknown when both are Satisfiable; a Satisfiable problem also
%            shows the statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+1.ax').

fof(w_kgc375, axiom,
    ~ ( ( bcp_de != bcp_fr
    | ( bcp_bg = bcp_de & bcp_bg != bcp_fr )
    | ( bcp_cs = bcp_de & bcp_cs != bcp_fr )
    | ( bcp_da = bcp_de & bcp_da != bcp_fr )
    | ( bcp_el = bcp_de & bcp_el != bcp_fr )
    | ( bcp_en = bcp_de & bcp_en != bcp_fr )
    | ( bcp_es = bcp_de & bcp_es != bcp_fr )
    | ( bcp_fi = bcp_de & bcp_fi != bcp_fr )
    | ( bcp_hu = bcp_de & bcp_hu != bcp_fr )
    | ( bcp_it = bcp_de & bcp_it != bcp_fr )
    | ( bcp_nl = bcp_de & bcp_nl != bcp_fr )
    | ( bcp_pl = bcp_de & bcp_pl != bcp_fr )
    | ( bcp_pt = bcp_de & bcp_pt != bcp_fr )
    | ( bcp_sv = bcp_de & bcp_sv != bcp_fr ) ) )).
%------------------------------------------------------------------------------
