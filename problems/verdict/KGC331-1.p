%--------------------------------------------------------------------------
% File     : KGC331-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf loc:EU against eq loc:DE (witness condition asserted)
% Version  : 1.0
% English  : A library permits use within the European Union; a researcher asks to use the material in Germany. DPV places Germany in the EU, and this binding reads membership as containment.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC331-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-juris.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.
% Resource: the jurisdictional reading, containment together with union
% membership.  Under the geographic reading loc:EU is not a concept and this
% problem does not arise.

% --- witness condition asserted ------------------------------------------
fof(w_kgc331, axiom,
    ( ( kge_leq(loc_eu, loc_eu) & loc_eu = loc_de )
| ( kge_leq(loc_de, loc_eu) & loc_de = loc_de ) )).
%--------------------------------------------------------------------------
