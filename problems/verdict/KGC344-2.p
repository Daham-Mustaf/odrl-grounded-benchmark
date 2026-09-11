%--------------------------------------------------------------------------
% File     : KGC344-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, xone(eq ConsentGiven, eq ConsentWithdrawn) against eq ConsentGiven (witness condition negated)
% Version  : 1.0
% English  : An offer requires the record to be in exactly one of the given and withdrawn states; a processor commits to processing only under given consent.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC344-2.p
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
fof(w_kgc344, axiom,
    ~ ( ( ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given )
| ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given ) ) & ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given ) & ~ ( dpv_consent_given = dpv_consent_withdrawn ) )
| ( ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given ) & ~ ( dpv_consent_withdrawn = dpv_consent_withdrawn ) ) ) )
| ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given )
| ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given ) ) & ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given ) & ~ ( dpv_consent_given = dpv_consent_given ) )
| ( ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given ) & ~ ( dpv_consent_withdrawn = dpv_consent_given ) ) ) ) ) )).
%--------------------------------------------------------------------------
