%--------------------------------------------------------------------------
% File     : KGC341-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, or(eq ConsentGiven, eq RenewedConsentGiven) against eq RenewedConsentGiven (witness condition asserted)
% Version  : 1.0
% English  : The same policy as KGC340, written by enumerating the two states rather than by naming the branch that holds them.  The verdict is again Compatible, and the certificate cites no resource assertion: the second alternative is the requested state, and nothing needs to be looked up.  The offer is fixed against the vocabulary as it stands, where KGC340's is not.
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
    ( ( ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_renewed_consent_given ) )
| ( ( dpv_renewed_consent_given = dpv_consent_given & dpv_renewed_consent_given = dpv_renewed_consent_given ) ) ) )
| ( ( ( ( dpv_consent_given = dpv_renewed_consent_given & dpv_consent_given = dpv_renewed_consent_given ) )
| ( ( dpv_renewed_consent_given = dpv_renewed_consent_given & dpv_renewed_consent_given = dpv_renewed_consent_given ) ) ) ) )).
%--------------------------------------------------------------------------
