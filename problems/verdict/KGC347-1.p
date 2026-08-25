%--------------------------------------------------------------------------
% File     : KGC347-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, xone(isA ValidForProcessing, isA InvalidForProcessing) against eq ConsentGiven, branches disjoint (witness condition asserted)
% Version  : 1.0
% English  : The constraints of KGC346 with the branches declared disjoint.  Nothing lies below both, so the given state lies below the valid branch and not the invalid one, exactly one alternative holds, and the verdict is Compatible.  The refutation cites an assertion DPV published and a declaration the parties made, and the certificate marks which is which.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC347-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').
include('axioms/DPV-consent-definitional.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc347, axiom,
    ( ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) & dpv_consent_given = dpv_consent_given ) ) & ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_invalid_for_processing) ) )
| ( ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_invalid_for_processing) ) )
| ( ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) & dpv_consent_given = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_given, dpv_consent_status_invalid_for_processing) ) ) ) )
| ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_given, dpv_consent_status_invalid_for_processing) & dpv_consent_given = dpv_consent_given ) ) & ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) ) )
| ( ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_invalid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) ) )
| ( ( kge_leq(dpv_consent_given, dpv_consent_status_invalid_for_processing) & dpv_consent_given = dpv_consent_given ) & ~ ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) ) ) ) ) )).
%--------------------------------------------------------------------------
