%--------------------------------------------------------------------------
% File     : KGC398-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, isAnyOf {de, fr} against isAllOf {nl, fr}, no declaration (witness condition asserted)
% Version  : 1.0
% English  : A translation licence covers at least one of a German and a French edition. The licensee publishes in both Dutch and French.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC398-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc398, axiom,
    $true).
%--------------------------------------------------------------------------
