%--------------------------------------------------------------------------
% File     : KGC345-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, xone(eq ConsentGiven, eq ConsentWithdrawn) against eq ConsentGiven, the two states declared distinct (witness condition negated)
% Version  : 1.0
% English  : As KGC344, with the given and withdrawn states declared distinct.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC345-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').
include('axioms/DPV-consent-declared.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc345, axiom,
    ~ ( ( ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given )
| ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given ) ) & ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given ) & ~ ( dpv_consent_given = dpv_consent_withdrawn ) )
| ( ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given ) & ~ ( dpv_consent_withdrawn = dpv_consent_withdrawn ) ) ) )
| ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given )
| ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given ) ) & ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given ) & ~ ( dpv_consent_given = dpv_consent_given ) )
| ( ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given ) & ~ ( dpv_consent_withdrawn = dpv_consent_given ) ) ) ) ) )).
%--------------------------------------------------------------------------
