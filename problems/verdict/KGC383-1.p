%--------------------------------------------------------------------------
% File     : KGC383-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf loc:EU against eq loc:DE-NW, jurisdictional (witness condition asserted)
% Version  : 1.0
% English  : Use within the European Union against use in North Rhine-Westphalia, jurisdictional reading: DE-NW within DE, DE a member of EU, one transitivity step. Compatible, and here the composed answer is true. Read with KGC380: same reading, same depth, same two relations; the reading is faithful, and composing two relations is what can fail.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC383-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/LOC-dpvloc-juris.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc383, axiom,
    ( ( kge_leq(loc_eu, loc_eu) & loc_eu = loc_de_nw )
| ( kge_leq(loc_de_nw, loc_eu) & loc_de_nw = loc_de_nw ) )).
%--------------------------------------------------------------------------
