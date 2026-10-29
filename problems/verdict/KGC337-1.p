%--------------------------------------------------------------------------
% File     : KGC337-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isAllOf {loc:DE, loc:FR} against eq loc:DE, ISO rule (witness condition asserted)
% Version  : 1.0
% English  : A library lends its digitised manuscripts to a Franco-German research programme and requires use at partner sites in both Germany and France. A researcher's policy commits to use in Germany only. The ISO 3166 rule makes the two countries different places.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC337-1.p
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
% Declarations: instances of the ISO 3166 distinctness rule,
% stated in LOC-dpvloc-iso.ax and instantiated here.

fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).

% --- witness condition asserted ------------------------------------------
fof(w_kgc337, axiom,
    ( loc_de = loc_de & loc_fr = loc_de & ( loc_de = loc_de
| loc_fr = loc_de ) )).
%--------------------------------------------------------------------------
