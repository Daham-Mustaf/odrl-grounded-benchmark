%------------------------------------------------------------------------------
% File     : KGC051+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use only while the consent on record may justify processing against use only under given consent: some use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The two versions have the
%            same status.
% English  : A controller permits use while the consent on record may justify
%            processing; a processor commits to processing only under given
%            consent. This problem states that some use meets the two
%            policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC340-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC340 is Compatible. Its two problems state that some use meets
%            the two policies (KGC051) and that no use does (KGC052). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+2.ax').

fof(w_kgc340, axiom,
    ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_given )
    | kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing)
    | ( kge_leq(dpv_consent_expired, dpv_consent_status_valid_for_processing) & dpv_consent_expired = dpv_consent_given )
    | ( kge_leq(dpv_consent_invalidated, dpv_consent_status_valid_for_processing) & dpv_consent_invalidated = dpv_consent_given )
    | ( kge_leq(dpv_consent_refused, dpv_consent_status_valid_for_processing) & dpv_consent_refused = dpv_consent_given )
    | ( kge_leq(dpv_consent_request_deferred, dpv_consent_status_valid_for_processing) & dpv_consent_request_deferred = dpv_consent_given )
    | ( kge_leq(dpv_consent_requested, dpv_consent_status_valid_for_processing) & dpv_consent_requested = dpv_consent_given )
    | ( kge_leq(dpv_consent_revoked, dpv_consent_status_valid_for_processing) & dpv_consent_revoked = dpv_consent_given )
    | ( kge_leq(dpv_consent_status, dpv_consent_status_valid_for_processing) & dpv_consent_status = dpv_consent_given )
    | ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_given )
    | ( kge_leq(dpv_consent_unknown, dpv_consent_status_valid_for_processing) & dpv_consent_unknown = dpv_consent_given )
    | ( kge_leq(dpv_consent_withdrawn, dpv_consent_status_valid_for_processing) & dpv_consent_withdrawn = dpv_consent_given )
    | ( kge_leq(dpv_renewed_consent_given, dpv_consent_status_valid_for_processing) & dpv_renewed_consent_given = dpv_consent_given ) )).
%------------------------------------------------------------------------------
