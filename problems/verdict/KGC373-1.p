%--------------------------------------------------------------------------
% File     : KGC373-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against eq "en-US", primary-subtag grounding (witness condition asserted)
% Version  : 1.0
% English  : A publisher distributes in German. A licensee's policy commits to American English (en-US), under the rule that reduces a tag to its primary subtag.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
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
% Declarations: https://w3id.org/odrl-kb/bcp47/distinct, over every pair of the
% witness's candidates it states (1).

fof(bg_dist_bcp47_de_en, axiom,
    bcp_de != bcp_en).

% --- witness condition asserted ------------------------------------------
fof(w_kgc373, axiom,
    bcp_de = bcp_en).
%--------------------------------------------------------------------------
