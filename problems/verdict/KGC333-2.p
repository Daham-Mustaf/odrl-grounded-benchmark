%--------------------------------------------------------------------------
% File     : KGC333-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, eq loc:DE against eq loc:FR (witness condition negated)
% Version  : 1.0
% English  : A library permits use in Germany; a researcher requests use in France.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC333-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.  Two codes are not two places until something
% says so, and the extension says nothing.

% --- witness condition negated -------------------------------------------
fof(w_kgc333, axiom,
    ~ ( ( ( loc_de = loc_de & loc_de = loc_fr )
| ( loc_fr = loc_de & loc_fr = loc_fr ) ) )).
%--------------------------------------------------------------------------
