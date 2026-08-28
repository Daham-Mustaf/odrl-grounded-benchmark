%--------------------------------------------------------------------------
% File     : KGC374-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against neq fr, registry uniqueness declared (witness condition asserted)
% Version  : 1.0
% English  : The publisher distributes in German; the reuser accepts anything that is not French. German itself is the witness, but only because the parties' uniqueness rule separates the two subtags: in a structure interpreting de and fr as one language, a use in German is a use in French and the request excludes it.
%           : 
%           : So this Compatible rests on a declared premise exactly as KGC370's Incompatible does. The refutation of the second query cites the witness condition and one background premise, and withdrawing that premise is KGC375. A definite verdict of either polarity can stand on the parties' declaration; polarity buys no exemption from provenance.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
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


% --- witness condition asserted ------------------------------------------
fof(w_kgc374, axiom,
    ( ( bcp_de = bcp_de & bcp_de != bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr != bcp_fr ) )).
%--------------------------------------------------------------------------
