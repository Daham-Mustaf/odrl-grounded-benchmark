%--------------------------------------------------------------------------
% File     : KGC387-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isNoneOf {loc:DE-BY, loc:DE-BE} against eq loc:DE-HH, ISO rule (witness condition negated)
% Version  : 1.0
% English  : KGC386 under the ISO rule: Hamburg is distinct from Bavaria and from Berlin, so it lies in the complement in every structure and the verdict is Compatible. The only case in the suite where a declaration settles a complement positively; KGC317's isNoneOf is Incompatible on the constraints alone.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC387-2.p
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

fof(bg_dist_loc_de_hh_loc_de_by, axiom,
    loc_de_hh != loc_de_by).
fof(bg_dist_loc_de_hh_loc_de_be, axiom,
    loc_de_hh != loc_de_be).

% --- witness condition negated -------------------------------------------
fof(w_kgc387, axiom,
    ~ ( ( ( ( loc_de_by != loc_de_by & loc_de_by != loc_de_be ) & loc_de_by = loc_de_hh )
| ( ( loc_de_be != loc_de_by & loc_de_be != loc_de_be ) & loc_de_be = loc_de_hh )
| ( ( loc_de_hh != loc_de_by & loc_de_hh != loc_de_be ) & loc_de_hh = loc_de_hh ) ) )).
%--------------------------------------------------------------------------
