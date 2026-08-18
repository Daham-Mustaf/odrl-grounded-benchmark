%--------------------------------------------------------------------------
% File     : KGC317-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isNoneOf {dpv:Marketing} against eq dpv:Marketing (witness condition negated)
% Version  : 1.0
% English  : Offer (purpose, isNoneOf, {dpv:Marketing}) against request (purpose, eq, dpv:Marketing).  The offer excludes exactly the purpose the request requires.  No order assertion and no declaration takes part: the witness asks for a concept both distinct from and identical to marketing, which no structure provides.  Incompatible, and the certificate has nothing withdrawable in it, so unlike KGC300 and KGC314 no party can reopen the verdict by retracting an assertion.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC317-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-milestone.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty, and it stays empty.  The incompatibility here
% is between the two constraints, not between a constraint and something a
% party declared.

% --- witness condition negated -------------------------------------------
fof(w_kgc317, axiom,
    ~ ( ( dpv_marketing != dpv_marketing & dpv_marketing = dpv_marketing ) )).
%--------------------------------------------------------------------------
