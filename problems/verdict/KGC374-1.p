%--------------------------------------------------------------------------
% File     : KGC374-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against neq fr, distinctness rule declared (witness condition asserted)
% Version  : 1.0
% English  : A publisher distributes in German. A licensee's policy accepts any language except French.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC374-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').
include('axioms/BCP47001-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: https://w3id.org/odrl-kb/bcp47/distinct, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_bcp47_de_fr, axiom,
    bcp_de != bcp_fr).

% --- witness condition asserted ------------------------------------------
fof(w_kgc374, axiom,
    bcp_de != bcp_fr).
%--------------------------------------------------------------------------
