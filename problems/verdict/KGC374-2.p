%--------------------------------------------------------------------------
% File     : KGC374-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against neq fr, registry uniqueness declared (witness condition negated)
% Version  : 1.0
% English  : A publisher distributes in German, while a reuser accepts any language except French.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC374-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').
include('axioms/BCP47001-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc374, axiom,
    ~ ( ( ( bcp_de = bcp_de & bcp_de != bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr != bcp_fr ) ) )).
%--------------------------------------------------------------------------
