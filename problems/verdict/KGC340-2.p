%--------------------------------------------------------------------------
% File     : KGC340-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, isA ValidForProcessing against eq ConsentGiven (witness condition negated)
% Version  : 1.0
% English  : A controller permits use while the consent on record may justify processing; a processor commits to processing only under given consent.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC340-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc340, axiom,
    ~ ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given )
| ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) & dpv_consent_given = dpv_consent_given ) ) )).
%--------------------------------------------------------------------------
