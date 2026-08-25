%--------------------------------------------------------------------------
% File     : KGC345-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, xone(eq ConsentGiven, eq ConsentWithdrawn) against eq ConsentGiven, the two states declared distinct (witness condition asserted)
% Version  : 1.0
% English  : The constraints of KGC344 with the two states declared distinct.  Every structure then separates them, the first alternative holds and the second does not, and the verdict is Compatible.  The declaration is what makes the exclusive requirement decidable: with it the offer means what it appears to mean, and without it the same offer is open.  This is the pair to read together.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC345-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').
include('axioms/DPV-consent-declared.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc345, axiom,
    ( ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given ) )
| ( ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given ) ) ) & ( ( ( dpv_consent_given = dpv_consent_given & dpv_consent_given = dpv_consent_given & ~ ( dpv_consent_given = dpv_consent_withdrawn ) ) )
| ( ( dpv_consent_withdrawn = dpv_consent_given & dpv_consent_withdrawn = dpv_consent_given & ~ ( dpv_consent_withdrawn = dpv_consent_withdrawn ) ) ) ) )
| ( ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given ) )
| ( ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given ) ) ) & ( ( ( dpv_consent_given = dpv_consent_withdrawn & dpv_consent_given = dpv_consent_given & ~ ( dpv_consent_given = dpv_consent_given ) ) )
| ( ( dpv_consent_withdrawn = dpv_consent_withdrawn & dpv_consent_withdrawn = dpv_consent_given & ~ ( dpv_consent_withdrawn = dpv_consent_given ) ) ) ) )).
%--------------------------------------------------------------------------
