%--------------------------------------------------------------------------
% File     : KGC300-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq bcp:de against eq bcp:fr (witness condition negated)
% Version  : 1.0
% English  : Offer (language, eq, bcp:de) against request (language, eq, bcp:fr).  The registry's uniqueness rule places the two subtags in the background theory as distinct, so no model identifies them and the witness condition fails in every model.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC300-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: the registry's uniqueness rule, as distinctness.
fof(bt_de_distinct_fr, axiom,
    bcp_de != bcp_fr).

% --- witness condition negated -------------------------------------------
fof(w_kgc300, axiom,
    ~ ( ( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) ) )).
%--------------------------------------------------------------------------
