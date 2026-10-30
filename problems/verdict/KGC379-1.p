%--------------------------------------------------------------------------
% File     : KGC379-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, xone(eq de, eq fr) against eq de, no declaration (witness condition asserted)
% Version  : 1.0
% English  : A licence for a single-language edition allows exactly one of German and French. The licensee publishes in German.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC379-1.p
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
fof(w_kgc379, axiom,
    bcp_de != bcp_fr).
%--------------------------------------------------------------------------
