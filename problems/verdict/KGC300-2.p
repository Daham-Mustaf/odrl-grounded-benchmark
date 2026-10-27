%--------------------------------------------------------------------------
% File     : KGC300-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq bcp:de against eq bcp:fr (witness condition negated)
% Version  : 1.0
% English  : A German library permits use of its manuscripts in German only. A French library's policy commits to use in French only.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC300-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').
include('axioms/BCP47001-0.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: the registry's uniqueness rule, BCP47001-0.ax.  The
% pair de, fr is one of its 105 instances.

% --- witness condition negated -------------------------------------------
fof(w_kgc300, axiom,
    ~ ( ( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) ) )).
%--------------------------------------------------------------------------
