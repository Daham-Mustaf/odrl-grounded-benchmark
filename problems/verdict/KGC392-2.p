%--------------------------------------------------------------------------
% File     : KGC392-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isNoneOf {loc:WF} against eq loc:WF-UV, ISO rule (witness condition negated)
% Version  : 1.0
% English  : Use anywhere except Wallis and Futuna, against use in Uvea, a commune the file places within Wallis and Futuna. isNoneOf excludes the named area by identity, Uvea is a different concept under the ISO rule, and the verdict is Compatible.
%           : 
%           : The verdict is faithful to ODRL's set-based operator and defeats what the drafter meant: 'not in Wallis and Futuna' is a claim about parthood, and no ODRL operator tests the complement of a down-set. The spatial twin of neq EU not meaning outside the EU.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC392-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').
include('axioms/LOC-dpvloc-iso.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: instances of the ISO 3166 uniqueness rule,
% stated in LOC-dpvloc-iso.ax and instantiated here.

fof(bg_dist_loc_wf_uv_loc_wf, axiom,
    loc_wf_uv != loc_wf).

% --- witness condition negated -------------------------------------------
fof(w_kgc392, axiom,
    ~ ( ( ( loc_wf != loc_wf & loc_wf = loc_wf_uv )
| ( loc_wf_uv != loc_wf & loc_wf_uv = loc_wf_uv ) ) )).
%--------------------------------------------------------------------------
