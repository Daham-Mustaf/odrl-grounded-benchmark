%--------------------------------------------------------------------------
% File     : KGC314-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, eq dpv:Marketing against eq dpv:SR, under a declared distinctness (witness condition asserted)
% Version  : 1.0
% English  : The constraints of KGC313, over the same resource, under a background theory in which the parties declare the two purposes distinct.  No model then identifies them, the witness fails everywhere, and the verdict is Incompatible.  DPV publishes no such distinctness: the verdict rests on the declaration, and the certificate marks it withdrawable.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC314-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-milestone.ax').
include('axioms/DPV-milestone-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: one declared distinctness, from
% DPV-milestone-declared.ax.  Nothing in DPV separates these purposes.

% --- witness condition asserted ------------------------------------------
fof(w_kgc314, axiom,
    ( ( dpv_marketing = dpv_marketing & dpv_marketing = dpv_scientific_research )
| ( dpv_scientific_research = dpv_marketing & dpv_scientific_research = dpv_scientific_research ) )).
%--------------------------------------------------------------------------
