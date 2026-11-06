%------------------------------------------------------------------------------
% File     : KGC053+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use only while the consent on record may justify processing against use only records whose consent was withdrawn: some use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The versions have the
%            same status.
% English  : A controller permits use only while the consent on record may
%            justify processing. A processor commits to use only records whose
%            consent was withdrawn, in an erasure audit for the controller.
%            This problem states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC342-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC342 is Unknown. Its two problems state that some use meets the
%            two policies (KGC053) and that no use does (KGC054); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+2.ax').

fof(w_kgc342, axiom,
    ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_withdrawn )
    | kge_leq(dpv_consent_withdrawn, dpv_consent_status_valid_for_processing)
    | ( kge_leq(dpv_consent_expired, dpv_consent_status_valid_for_processing) & dpv_consent_expired = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_given, dpv_consent_status_valid_for_processing) & dpv_consent_given = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_invalidated, dpv_consent_status_valid_for_processing) & dpv_consent_invalidated = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_refused, dpv_consent_status_valid_for_processing) & dpv_consent_refused = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_request_deferred, dpv_consent_status_valid_for_processing) & dpv_consent_request_deferred = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_requested, dpv_consent_status_valid_for_processing) & dpv_consent_requested = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_revoked, dpv_consent_status_valid_for_processing) & dpv_consent_revoked = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_status, dpv_consent_status_valid_for_processing) & dpv_consent_status = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_status_invalid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_invalid_for_processing = dpv_consent_withdrawn )
    | ( kge_leq(dpv_consent_unknown, dpv_consent_status_valid_for_processing) & dpv_consent_unknown = dpv_consent_withdrawn )
    | ( kge_leq(dpv_renewed_consent_given, dpv_consent_status_valid_for_processing) & dpv_renewed_consent_given = dpv_consent_withdrawn ) )).
%------------------------------------------------------------------------------
