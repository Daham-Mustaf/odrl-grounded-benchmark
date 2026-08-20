%--------------------------------------------------------------------------
% File     : KGC333-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, eq loc:DE against eq loc:FR (witness condition asserted)
% Version  : 1.0
% English  : Offer (spatial, eq, loc:DE) against request (spatial, eq, loc:FR).  Both denote singletons, so the constraints hold together only if the two codes denote one place.  The extension asserts no distinctness anywhere, so a model may identify them: Unknown.  The file looks as though it settles this and does not: every country has an inverse jurisdiction concept, and non-DE is narrower than France, but that says which concepts belong to a complement and not that the two are different.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC333-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  Two codes are not two places until something
% says so, and the extension says nothing.

% --- witness condition asserted ------------------------------------------
fof(w_kgc333, axiom,
    ( ( loc_de = loc_de & loc_de = loc_fr )
| ( loc_fr = loc_de & loc_fr = loc_fr ) )).
%--------------------------------------------------------------------------
