%--------------------------------------------------------------------------
% File     : KGC377-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, isNoneOf en it against eq it, no declaration (witness condition negated)
% Version  : 1.0
% English  : English and Italian rights were sold separately, so a publisher permits any language except English and Italian. The licensee distributes in Italian.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC377-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc377, axiom,
    ~ ( ~ ( $true ) )).
%--------------------------------------------------------------------------
