%--------------------------------------------------------------------------
% File     : KGC353-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : legal basis, isA dpv:LegalBasis against eq A6-1-a-explicit-consent (witness condition negated)
% Version  : 1.0
% English  : The record of KGC351 and KGC352 against an offer that names the branch rather than enumerating its members. Four assertions of the vocabulary carry explicit consent up to the legal-basis root, and with transitivity the verdict is Compatible in every structure. Read together with KGC352 this is the cost of the enumeration: the same Article, the same record, opposite verdicts, and the certificates say which rests on what.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC353-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-gdprlb.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc353, axiom,
    ~ ( ( ( ( kge_leq(lb_dpv_legal_basis, lb_dpv_legal_basis) & lb_dpv_legal_basis = lb_gdpr_a6_1_a_explicit_consent ) )
| ( ( kge_leq(lb_gdpr_a6_1_a_explicit_consent, lb_dpv_legal_basis) & lb_gdpr_a6_1_a_explicit_consent = lb_gdpr_a6_1_a_explicit_consent ) ) ) )).
%--------------------------------------------------------------------------
