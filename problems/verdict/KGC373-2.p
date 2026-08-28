%--------------------------------------------------------------------------
% File     : KGC373-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq "en-US", primary-subtag grounding (witness condition negated)
% Version  : 1.0
% English  : The policies of KGC372, read under the profile's other grounding rule.
%           : 
%           : That rule takes a well-formed language tag to its primary subtag, so en-US resolves to en. The request becomes interpretable and the pair gets an ordinary verdict: German and English are declared distinct under the same registry-uniqueness rule as KGC370, so no use satisfies both constraints and the verdict is Incompatible.
%           : 
%           : Neither rule is the correct one. A party who cares which variety of English is distributed declines the reduction and would rather have an uninterpretable policy than a wrong answer; a party who does not, adopts it. The two problems return different verdicts on identical policies over an identical vocabulary, and the parties disagree about no concept: what differs is a reading rule, which the profile records and a report cites.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC373-2.p
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
fof(w_kgc373, axiom,
    ~ ( ( ( bcp_de = bcp_de & bcp_de = bcp_en )
| ( bcp_en = bcp_de & bcp_en = bcp_en ) ) )).
%--------------------------------------------------------------------------
