%--------------------------------------------------------------------------
% File     : KGC392-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isNoneOf {loc:WF} against eq loc:WF-UV, ISO rule (witness condition asserted)
% Version  : 1.0
% English  : A library permits use anywhere except Wallis and Futuna. A researcher's policy commits to use in Uvea, a district of Wallis and Futuna.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC392-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-geo.ax').
include('axioms/LOC-dpvloc-iso.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: instances of the ISO 3166 uniqueness rule,
% stated in LOC-dpvloc-iso.ax and instantiated here.

fof(bg_dist_loc_wf_uv_loc_wf, axiom,
    loc_wf_uv != loc_wf).

% --- witness condition asserted ------------------------------------------
fof(w_kgc392, axiom,
    ( ( loc_wf != loc_wf & loc_wf = loc_wf_uv )
| ( loc_wf_uv != loc_wf & loc_wf_uv = loc_wf_uv ) )).
%--------------------------------------------------------------------------
