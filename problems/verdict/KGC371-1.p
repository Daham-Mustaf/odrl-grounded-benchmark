%--------------------------------------------------------------------------
% File     : KGC371-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq fr, declaration withdrawn (witness condition asserted)
% Version  : 1.0
% English  : As KGC370, without the registry rule.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC371-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc371, axiom,
    ( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) )).
%--------------------------------------------------------------------------
