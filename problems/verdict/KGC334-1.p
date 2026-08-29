%--------------------------------------------------------------------------
% File     : KGC334-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, eq loc:DE against eq loc:FR, under the ISO 3166 uniqueness rule (witness condition asserted)
% Version  : 1.0
% English  : The constraints of KGC333 under a background theory generated from the rule that ISO 3166 assigns one code to an area.  No model then identifies the two, the witness fails everywhere, and the verdict is Incompatible.  The extension asserts no such distinctness: the rule is the parties', and the certificate marks it withdrawable.  The rule separates areas rather than codes, since the extension itself records thirty pairs of codes denoting one area, and a rule applied to the codes would contradict it.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC334-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').
include('axioms/LOC-dpvloc-iso.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: one instance of the ISO 3166 uniqueness rule.
%
% The rule is stated in LOC-dpvloc-iso.ax and ranges over 249 areas.  It is
% instantiated here rather than expanded there: a refutation should cite the
% inequation it used, not one term standing for thirty thousand.
fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

% --- witness condition asserted ------------------------------------------
fof(w_kgc334, axiom,
    ( ( loc_de = loc_de & loc_de = loc_fr )
| ( loc_fr = loc_de & loc_fr = loc_fr ) )).
%--------------------------------------------------------------------------
