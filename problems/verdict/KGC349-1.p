%--------------------------------------------------------------------------
% File     : KGC349-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, isNoneOf {ConsentWithdrawn, ConsentRevoked} against eq ConsentExpired, states declared distinct (witness condition asserted)
% Version  : 1.0
% English  : A controller permits use under any consent status except withdrawn and revoked. A processor commits to use only records whose consent has expired, in a consent-renewal campaign.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC349-1.p
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
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_dpv_consent_expired_dpv_consent_withdrawn, axiom,
    dpv_consent_expired != dpv_consent_withdrawn).
fof(bg_dist_dpv_consent_expired_dpv_consent_revoked, axiom,
    dpv_consent_expired != dpv_consent_revoked).

% --- witness condition asserted ------------------------------------------
fof(w_kgc349, axiom,
    ( ( ( dpv_consent_withdrawn != dpv_consent_withdrawn & dpv_consent_withdrawn != dpv_consent_revoked ) & dpv_consent_withdrawn = dpv_consent_expired )
| ( ( dpv_consent_revoked != dpv_consent_withdrawn & dpv_consent_revoked != dpv_consent_revoked ) & dpv_consent_revoked = dpv_consent_expired )
| ( ( dpv_consent_expired != dpv_consent_withdrawn & dpv_consent_expired != dpv_consent_revoked ) & dpv_consent_expired = dpv_consent_expired ) )).
%--------------------------------------------------------------------------
