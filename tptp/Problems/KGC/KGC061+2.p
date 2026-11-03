%------------------------------------------------------------------------------
% File     : KGC061+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use under any consent status except withdrawn and revoked against use only records whose consent has expired: some use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The two versions have the
%            same status.
% English  : A controller permits use under any consent status except
%            withdrawn and revoked. A processor commits to use only records
%            whose consent has expired, in a consent-renewal campaign. This
%            problem states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC349-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC349 is Compatible. Its two problems state that some use meets
%            the two policies (KGC061) and that no use does (KGC062). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+2.ax').

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_revoked, axiom,
    dpv_consent_withdrawn != dpv_consent_revoked).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_expired, axiom,
    dpv_consent_withdrawn != dpv_consent_expired).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_given, axiom,
    dpv_consent_withdrawn != dpv_consent_given).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_invalidated, axiom,
    dpv_consent_withdrawn != dpv_consent_invalidated).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_refused, axiom,
    dpv_consent_withdrawn != dpv_consent_refused).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_request_deferred, axiom,
    dpv_consent_withdrawn != dpv_consent_request_deferred).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_requested, axiom,
    dpv_consent_withdrawn != dpv_consent_requested).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_status, axiom,
    dpv_consent_withdrawn != dpv_consent_status).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_withdrawn != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_withdrawn != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_withdrawn_dpv_consent_unknown, axiom,
    dpv_consent_withdrawn != dpv_consent_unknown).

fof(bg_dist_dpv_consent_withdrawn_dpv_renewed_consent_given, axiom,
    dpv_consent_withdrawn != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_revoked_dpv_consent_expired, axiom,
    dpv_consent_revoked != dpv_consent_expired).

fof(bg_dist_dpv_consent_revoked_dpv_consent_given, axiom,
    dpv_consent_revoked != dpv_consent_given).

fof(bg_dist_dpv_consent_revoked_dpv_consent_invalidated, axiom,
    dpv_consent_revoked != dpv_consent_invalidated).

fof(bg_dist_dpv_consent_revoked_dpv_consent_refused, axiom,
    dpv_consent_revoked != dpv_consent_refused).

fof(bg_dist_dpv_consent_revoked_dpv_consent_request_deferred, axiom,
    dpv_consent_revoked != dpv_consent_request_deferred).

fof(bg_dist_dpv_consent_revoked_dpv_consent_requested, axiom,
    dpv_consent_revoked != dpv_consent_requested).

fof(bg_dist_dpv_consent_revoked_dpv_consent_status, axiom,
    dpv_consent_revoked != dpv_consent_status).

fof(bg_dist_dpv_consent_revoked_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_revoked != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_revoked_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_revoked != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_revoked_dpv_consent_unknown, axiom,
    dpv_consent_revoked != dpv_consent_unknown).

fof(bg_dist_dpv_consent_revoked_dpv_renewed_consent_given, axiom,
    dpv_consent_revoked != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_expired_dpv_consent_given, axiom,
    dpv_consent_expired != dpv_consent_given).

fof(bg_dist_dpv_consent_expired_dpv_consent_invalidated, axiom,
    dpv_consent_expired != dpv_consent_invalidated).

fof(bg_dist_dpv_consent_expired_dpv_consent_refused, axiom,
    dpv_consent_expired != dpv_consent_refused).

fof(bg_dist_dpv_consent_expired_dpv_consent_request_deferred, axiom,
    dpv_consent_expired != dpv_consent_request_deferred).

fof(bg_dist_dpv_consent_expired_dpv_consent_requested, axiom,
    dpv_consent_expired != dpv_consent_requested).

fof(bg_dist_dpv_consent_expired_dpv_consent_status, axiom,
    dpv_consent_expired != dpv_consent_status).

fof(bg_dist_dpv_consent_expired_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_expired != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_expired_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_expired != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_expired_dpv_consent_unknown, axiom,
    dpv_consent_expired != dpv_consent_unknown).

fof(bg_dist_dpv_consent_expired_dpv_renewed_consent_given, axiom,
    dpv_consent_expired != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_given_dpv_consent_invalidated, axiom,
    dpv_consent_given != dpv_consent_invalidated).

fof(bg_dist_dpv_consent_given_dpv_consent_refused, axiom,
    dpv_consent_given != dpv_consent_refused).

fof(bg_dist_dpv_consent_given_dpv_consent_request_deferred, axiom,
    dpv_consent_given != dpv_consent_request_deferred).

fof(bg_dist_dpv_consent_given_dpv_consent_requested, axiom,
    dpv_consent_given != dpv_consent_requested).

fof(bg_dist_dpv_consent_given_dpv_consent_status, axiom,
    dpv_consent_given != dpv_consent_status).

fof(bg_dist_dpv_consent_given_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_given != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_given_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_given != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_given_dpv_consent_unknown, axiom,
    dpv_consent_given != dpv_consent_unknown).

fof(bg_dist_dpv_consent_given_dpv_renewed_consent_given, axiom,
    dpv_consent_given != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_invalidated_dpv_consent_refused, axiom,
    dpv_consent_invalidated != dpv_consent_refused).

fof(bg_dist_dpv_consent_invalidated_dpv_consent_request_deferred, axiom,
    dpv_consent_invalidated != dpv_consent_request_deferred).

fof(bg_dist_dpv_consent_invalidated_dpv_consent_requested, axiom,
    dpv_consent_invalidated != dpv_consent_requested).

fof(bg_dist_dpv_consent_invalidated_dpv_consent_status, axiom,
    dpv_consent_invalidated != dpv_consent_status).

fof(bg_dist_dpv_consent_invalidated_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_invalidated != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_invalidated_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_invalidated != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_invalidated_dpv_consent_unknown, axiom,
    dpv_consent_invalidated != dpv_consent_unknown).

fof(bg_dist_dpv_consent_invalidated_dpv_renewed_consent_given, axiom,
    dpv_consent_invalidated != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_refused_dpv_consent_request_deferred, axiom,
    dpv_consent_refused != dpv_consent_request_deferred).

fof(bg_dist_dpv_consent_refused_dpv_consent_requested, axiom,
    dpv_consent_refused != dpv_consent_requested).

fof(bg_dist_dpv_consent_refused_dpv_consent_status, axiom,
    dpv_consent_refused != dpv_consent_status).

fof(bg_dist_dpv_consent_refused_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_refused != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_refused_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_refused != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_refused_dpv_consent_unknown, axiom,
    dpv_consent_refused != dpv_consent_unknown).

fof(bg_dist_dpv_consent_refused_dpv_renewed_consent_given, axiom,
    dpv_consent_refused != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_request_deferred_dpv_consent_requested, axiom,
    dpv_consent_request_deferred != dpv_consent_requested).

fof(bg_dist_dpv_consent_request_deferred_dpv_consent_status, axiom,
    dpv_consent_request_deferred != dpv_consent_status).

fof(bg_dist_dpv_consent_request_deferred_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_request_deferred != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_request_deferred_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_request_deferred != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_request_deferred_dpv_consent_unknown, axiom,
    dpv_consent_request_deferred != dpv_consent_unknown).

fof(bg_dist_dpv_consent_request_deferred_dpv_renewed_consent_given, axiom,
    dpv_consent_request_deferred != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_requested_dpv_consent_status, axiom,
    dpv_consent_requested != dpv_consent_status).

fof(bg_dist_dpv_consent_requested_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_requested != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_requested_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_requested != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_requested_dpv_consent_unknown, axiom,
    dpv_consent_requested != dpv_consent_unknown).

fof(bg_dist_dpv_consent_requested_dpv_renewed_consent_given, axiom,
    dpv_consent_requested != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_status_dpv_consent_status_invalid_for_processing, axiom,
    dpv_consent_status != dpv_consent_status_invalid_for_processing).

fof(bg_dist_dpv_consent_status_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_status != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_status_dpv_consent_unknown, axiom,
    dpv_consent_status != dpv_consent_unknown).

fof(bg_dist_dpv_consent_status_dpv_renewed_consent_given, axiom,
    dpv_consent_status != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_status_invalid_for_processing_dpv_consent_status_valid_for_processing, axiom,
    dpv_consent_status_invalid_for_processing != dpv_consent_status_valid_for_processing).

fof(bg_dist_dpv_consent_status_invalid_for_processing_dpv_consent_unknown, axiom,
    dpv_consent_status_invalid_for_processing != dpv_consent_unknown).

fof(bg_dist_dpv_consent_status_invalid_for_processing_dpv_renewed_consent_given, axiom,
    dpv_consent_status_invalid_for_processing != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_status_valid_for_processing_dpv_consent_unknown, axiom,
    dpv_consent_status_valid_for_processing != dpv_consent_unknown).

fof(bg_dist_dpv_consent_status_valid_for_processing_dpv_renewed_consent_given, axiom,
    dpv_consent_status_valid_for_processing != dpv_renewed_consent_given).

fof(bg_dist_dpv_consent_unknown_dpv_renewed_consent_given, axiom,
    dpv_consent_unknown != dpv_renewed_consent_given).

fof(w_kgc349, axiom,
    ( ( dpv_consent_expired != dpv_consent_withdrawn & dpv_consent_expired != dpv_consent_revoked )
    | ( dpv_consent_given != dpv_consent_withdrawn & dpv_consent_given != dpv_consent_revoked & dpv_consent_given = dpv_consent_expired )
    | ( dpv_consent_invalidated != dpv_consent_withdrawn & dpv_consent_invalidated != dpv_consent_revoked & dpv_consent_invalidated = dpv_consent_expired )
    | ( dpv_consent_refused != dpv_consent_withdrawn & dpv_consent_refused != dpv_consent_revoked & dpv_consent_refused = dpv_consent_expired )
    | ( dpv_consent_request_deferred != dpv_consent_withdrawn & dpv_consent_request_deferred != dpv_consent_revoked & dpv_consent_request_deferred = dpv_consent_expired )
    | ( dpv_consent_requested != dpv_consent_withdrawn & dpv_consent_requested != dpv_consent_revoked & dpv_consent_requested = dpv_consent_expired )
    | ( dpv_consent_status != dpv_consent_withdrawn & dpv_consent_status != dpv_consent_revoked & dpv_consent_status = dpv_consent_expired )
    | ( dpv_consent_status_invalid_for_processing != dpv_consent_withdrawn & dpv_consent_status_invalid_for_processing != dpv_consent_revoked & dpv_consent_status_invalid_for_processing = dpv_consent_expired )
    | ( dpv_consent_status_valid_for_processing != dpv_consent_withdrawn & dpv_consent_status_valid_for_processing != dpv_consent_revoked & dpv_consent_status_valid_for_processing = dpv_consent_expired )
    | ( dpv_consent_unknown != dpv_consent_withdrawn & dpv_consent_unknown != dpv_consent_revoked & dpv_consent_unknown = dpv_consent_expired )
    | ( dpv_renewed_consent_given != dpv_consent_withdrawn & dpv_renewed_consent_given != dpv_consent_revoked & dpv_renewed_consent_given = dpv_consent_expired ) )).
%------------------------------------------------------------------------------
