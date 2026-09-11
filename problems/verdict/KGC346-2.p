%--------------------------------------------------------------------------
% File     : KGC346-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, xone(isA ValidForProcessing, isA InvalidForProcessing) against eq ConsentGiven (witness condition negated)
% Version  : 1.0
% English  : An offer requires the record to fall under exactly one of the two consent branches; a processor commits to processing only under given consent.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC346-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc346, axiom,
    ~ ( ( ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) & dpv_consent_given = dpv_consent_given ) ) & ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_invalid_for_processing) ) )
| ( ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_invalid_for_processing) ) )
| ( ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) & dpv_consent_given = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_given, dpv_consent_status_invalid_for_processing) ) ) ) )
| ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_given, dpv_consent_status_invalid_for_processing) & dpv_consent_given = dpv_consent_given ) ) & ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) ) )
| ( ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) ) )
| ( ( kge_leq(dpv_consent_given, dpv_consent_status_invalid_for_processing) & dpv_consent_given = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) ) ) ) ) ) )).
%--------------------------------------------------------------------------
