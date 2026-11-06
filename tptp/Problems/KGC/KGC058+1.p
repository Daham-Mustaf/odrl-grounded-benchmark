%------------------------------------------------------------------------------
% File     : KGC058+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use only while the consent on record may justify processing against use only records whose consent was withdrawn: no use meets both
% Version  : Especial.
% English  : As KGC342, with the consent states declared distinct from one
%            another. This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC348-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC348 is Unknown. Its two problems state that some use meets the
%            two policies (KGC057) and that no use does (KGC058); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+2.ax').

fof(bg_dist_dpv_consent_status_valid_for_processing_dpv_consent_withdrawn, axiom,
    dpv_consent_status_valid_for_processing != dpv_consent_withdrawn).

fof(w_kgc348, axiom,
    ~ ( kge_leq(dpv_consent_withdrawn, dpv_consent_status_valid_for_processing) )).
%------------------------------------------------------------------------------
