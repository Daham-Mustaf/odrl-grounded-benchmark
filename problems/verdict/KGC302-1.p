%--------------------------------------------------------------------------
% File     : KGC302-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : spatial, isPartOf gn:Europe against eq gn:France (witness condition asserted)
% Version  : 1.0
% English  : A German library permits use within Europe. A French library's policy commits to use in France only.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC302-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/GN000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc302, axiom,
    kge_leq(gn_france, gn_europe)).
%--------------------------------------------------------------------------
