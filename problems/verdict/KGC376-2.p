%--------------------------------------------------------------------------
% File     : KGC376-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, isAllOf nl fr against eq nl, registry uniqueness declared (witness condition negated)
% Version  : 1.0
% English  : A Belgian federal publisher requires distribution in both Dutch and French. The licensee distributes in Dutch only. The parties adopt the registry rule that different primary subtags name different languages.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC376-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').
include('axioms/BCP47001-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc376, axiom,
    ~ ( ( bcp_nl = bcp_nl & bcp_fr = bcp_nl & ( bcp_nl = bcp_nl
| bcp_fr = bcp_nl ) ) )).
%--------------------------------------------------------------------------
