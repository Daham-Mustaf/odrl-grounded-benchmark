%------------------------------------------------------------------------------
% File     : KGC055+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use only while the consent on record may justify processing against use only records whose consent was withdrawn: some use meets both
% Version  : Especial.
% English  : As KGC342, with the valid and invalid branches declared disjoint.
%            This problem states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC343-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC343 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC055) and that no use does (KGC056);
%            here the first is Unsatisfiable and the second Satisfiable. A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+2.ax').

fof(bg_disj_dpv_consent_status_valid_for_processing_disjoint_dpv_consent_status_invalid_for_processing, axiom,
    ! [X] : ~ ( kge_leq(X, dpv_consent_status_valid_for_processing) & kge_leq(X, dpv_consent_status_invalid_for_processing) )).

fof(w_kgc343, axiom,
    kge_leq(dpv_consent_withdrawn, dpv_consent_status_valid_for_processing)).
%------------------------------------------------------------------------------
