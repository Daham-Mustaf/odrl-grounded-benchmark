%--------------------------------------------------------------------------
% File     : KGC371-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq fr, declaration withdrawn (witness condition negated)
% Version  : 1.0
% English  : The policies of KGC370, over the same resource, with the registry-uniqueness rule withdrawn.
%           : 
%           : The registry still lists both subtags and still asserts nothing that separates them. So some structures admitted by the resource interpret de and fr as one language and others keep them apart, and whether a single use can satisfy both constraints depends on which. The verdict is Unknown, and the reason is epistemic: a declaration by either party settles it.
%           : 
%           : Read against KGC370 this is what a withdrawable premise means. Two identical policies over one vocabulary, one include line apart, and the verdict moves from definite to open because a party stopped asserting something the registry never asserted.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC371-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc371, axiom,
    ~ ( ( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) ) )).
%--------------------------------------------------------------------------
