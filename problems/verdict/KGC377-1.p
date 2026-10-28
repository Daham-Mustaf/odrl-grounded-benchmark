%--------------------------------------------------------------------------
% File     : KGC377-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, isNoneOf en it against eq it, no declaration (witness condition asserted)
% Version  : 1.0
% English  : English and Italian rights were sold separately, so a publisher permits any language except English and Italian. The licensee distributes in Italian.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC377-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc377, axiom,
    ( ( ( bcp_en != bcp_en & bcp_en != bcp_it ) & bcp_en = bcp_it )
| ( ( bcp_it != bcp_en & bcp_it != bcp_it ) & bcp_it = bcp_it ) )).
%--------------------------------------------------------------------------
