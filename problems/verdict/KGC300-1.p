%--------------------------------------------------------------------------
% File     : KGC300-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq bcp:de against eq bcp:fr (witness condition asserted)
% Version  : 1.0
% English  : A German library permits use of its manuscripts in German only. A French library's policy commits to use in French only.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC300-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').
include('axioms/BCP47001-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: the distinctness rule, BCP47001-0.ax.  The
% pair de, fr is one of its 105 instances.

% Declarations: https://w3id.org/odrl-kb/bcp47/distinct, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_bcp47_de_fr, axiom,
    bcp_de != bcp_fr).

% --- witness condition asserted ------------------------------------------
fof(w_kgc300, axiom,
    bcp_de = bcp_fr).
%--------------------------------------------------------------------------
