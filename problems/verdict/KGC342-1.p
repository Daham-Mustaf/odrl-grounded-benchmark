%--------------------------------------------------------------------------
% File     : KGC342-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, isA ValidForProcessing against eq ConsentWithdrawn (witness condition asserted)
% Version  : 1.0
% English  : A controller permits use only while consent may justify processing; a processor states that its processing continues after consent is withdrawn.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC342-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc342, axiom,
    ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_withdrawn )
| ( kge_leq(dpv_consent_withdrawn, dpv_consent_status_valid_for_processing) & dpv_consent_withdrawn = dpv_consent_withdrawn ) )).
%--------------------------------------------------------------------------
