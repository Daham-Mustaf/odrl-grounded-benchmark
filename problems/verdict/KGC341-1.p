%--------------------------------------------------------------------------
% File     : KGC341-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, or(eq ConsentGiven, eq RenewedConsentGiven) against eq RenewedConsentGiven (witness condition asserted)
% Version  : 1.0
% English  : A controller permits use under given or renewed consent; a processor commits to processing only under renewed consent.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC341-1.p
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
fof(w_kgc341, axiom,
    ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_renewed_consent_given )
| ( dpv_renewed_consent_given = dpv_consent_given & dpv_renewed_consent_given = dpv_renewed_consent_given ) )
| ( ( dpv_consent_given = dpv_renewed_consent_given & dpv_consent_given = dpv_renewed_consent_given )
| ( dpv_renewed_consent_given = dpv_renewed_consent_given & dpv_renewed_consent_given = dpv_renewed_consent_given ) ) )).
%--------------------------------------------------------------------------
