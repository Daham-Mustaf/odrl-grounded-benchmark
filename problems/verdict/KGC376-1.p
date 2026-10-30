%--------------------------------------------------------------------------
% File     : KGC376-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, isAllOf nl fr against eq nl, distinctness rule declared (witness condition asserted)
% Version  : 1.0
% English  : A Belgian federal publisher requires distribution in both Dutch and French. The licensee distributes in Dutch only. The registry rule that different primary subtags name different languages is adopted.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC376-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').
include('axioms/BCP47001-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/bcp47/distinct, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_bcp47_nl_fr, axiom,
    bcp_nl != bcp_fr).

% --- witness condition asserted ------------------------------------------
fof(w_kgc376, axiom,
    bcp_fr = bcp_nl).
%--------------------------------------------------------------------------
