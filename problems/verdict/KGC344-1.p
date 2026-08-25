%--------------------------------------------------------------------------
% File     : KGC344-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, xone(eq ConsentGiven, eq ConsentWithdrawn) against eq ConsentGiven (witness condition asserted)
% Version  : 1.0
% English  : The offer requires the record to be settled: in exactly one of the given and withdrawn states.  The record is given, so the answer looks immediate.  It is not.  Expanded, the first alternative requires the state to be given and not withdrawn, and DPV publishes nothing that separates the two: a structure may interpret them as one state, in which case the record is both and neither alternative holds alone.  Verdict: Unknown.  Counting alternatives requires knowing when two of them are the same.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC344-1.p
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
fof(w_kgc344, axiom,
    ( ( ( ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given ) )
| ( ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given ) ) ) & ( ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given ) & ~ ( dpv_consent_given = dpv_consent_withdrawn ) ) )
| ( ( ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given ) & ~ ( dpv_consent_withdrawn = dpv_consent_withdrawn ) ) ) ) ) )
| ( ( ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given ) )
| ( ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given ) ) ) & ( ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given ) & ~ ( dpv_consent_given = dpv_consent_given ) ) )
| ( ( ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given ) & ~ ( dpv_consent_withdrawn = dpv_consent_given ) ) ) ) ) ) )).
%--------------------------------------------------------------------------
