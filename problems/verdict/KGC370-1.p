%--------------------------------------------------------------------------
% File     : KGC370-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq fr, registry uniqueness declared (witness condition asserted)
% Version  : 1.0
% English  : The publisher distributes in German; the reuser asks for French. With the parties' registry-uniqueness rule in force no structure interprets the two subtags as one language, so no use satisfies both constraints and the verdict is Incompatible.
%           : 
%           : The refutation cites one background premise. The registry lists both subtags and asserts nothing that separates them, so what makes this verdict definite is a rule the parties adopted rather than something IANA published.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC370-1.p
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


% --- witness condition asserted ------------------------------------------
fof(w_kgc370, axiom,
    ( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) )).
%--------------------------------------------------------------------------
