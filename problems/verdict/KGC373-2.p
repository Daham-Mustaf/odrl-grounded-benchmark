%--------------------------------------------------------------------------
% File     : KGC373-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq "en-US", primary-subtag grounding (witness condition negated)
% Version  : 1.0
% English  : The policies of KGC372 read under the binding whose grounding reduces a well-formed tag to its primary subtag. en-US resolves to en, the request is interpretable, and the pair gets an ordinary verdict: German and English are declared distinct, so no use satisfies both and the verdict is Incompatible.
%           : 
%           : Neither reading is wrong. A party who cares which variety of English is distributed declines the reduction and gets an uninterpretable policy rather than a wrong answer; a party who does not, adopts it. The two verdicts differ without any disagreement about a concept, and the profile is where the difference is recorded.
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
