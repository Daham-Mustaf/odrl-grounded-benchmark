%--------------------------------------------------------------------------
% File     : KGC373-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq "en-US", primary-subtag grounding (witness condition asserted)
% Version  : 1.0
% English  : A publisher distributes in German, while a reuser requests American English.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC373-1.p
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
fof(w_kgc373, axiom,
    ( ( bcp_de = bcp_de & bcp_de = bcp_en )
| ( bcp_en = bcp_de & bcp_en = bcp_en ) )).
%--------------------------------------------------------------------------
