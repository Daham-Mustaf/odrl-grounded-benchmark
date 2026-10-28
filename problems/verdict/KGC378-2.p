%--------------------------------------------------------------------------
% File     : KGC378-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, or(eq de, eq fr) against eq fr, no declaration (witness condition negated)
% Version  : 1.0
% English  : A translation licence covers a German or a French edition. The licensee publishes in French.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC378-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc378, axiom,
    ~ ( ( ( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) )
| ( ( bcp_de = bcp_fr & bcp_de = bcp_fr )
| ( bcp_fr = bcp_fr & bcp_fr = bcp_fr ) ) ) )).
%--------------------------------------------------------------------------
