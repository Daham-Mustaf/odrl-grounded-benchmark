%--------------------------------------------------------------------------
% File     : KGC370-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq fr, registry uniqueness declared (witness condition negated)
% Version  : 1.0
% English  : A publisher distributes a dataset in German. A reuser asks to distribute it in French. Both constraints are on odrl:language, which this profile binds to a fifteen-subtag slice of the IANA Language Subtag Registry at the nominal sort.
%           : 
%           : The parties have adopted the registry-uniqueness rule: distinct primary subtag records, neither deprecated and with no Preferred-Value link between them, name distinct languages. With that rule in force no structure interprets de and fr as one language, so no single use satisfies both constraints, and the verdict is Incompatible.
%           : 
%           : The refutation cites one premise, and it is the parties' rather than the registry's. IANA lists both subtags and asserts nothing that separates them; what makes this verdict definite is a declaration, and a party who withdraws it reopens the case. KGC371 is that withdrawal.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC370-2.p
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


% --- witness condition negated -------------------------------------------
fof(w_kgc370, axiom,
    ~ ( ( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) ) )).
%--------------------------------------------------------------------------
