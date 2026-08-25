%--------------------------------------------------------------------------
% File     : KGC340-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, isA ValidForProcessing against eq ConsentGiven (witness condition negated)
% Version  : 1.0
% English  : The controller permits use while the consent may justify processing; the record is in the given state.  DPV places consent given below the branch of states valid for processing, so the verdict is Compatible on one assertion.  The offer names the branch rather than the states, so a state DPV adds to that branch later is covered without the offer being rewritten.
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
    ~ ( ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given ) )
| ( ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) & dpv_consent_given = dpv_consent_given ) ) ) )).
%--------------------------------------------------------------------------
