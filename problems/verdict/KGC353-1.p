%--------------------------------------------------------------------------
% File     : KGC353-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : legal basis, isA dpv:LegalBasis against eq A6-1-a-explicit-consent (witness condition asserted)
% Version  : 1.0
% English  : A controller permits processing under the legal-basis hierarchy, while a processor requests processing on the basis of explicit consent under Article 6(1)(a).
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC353-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-gdprlb.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc353, axiom,
    ( ( kge_leq(lb_dpv_legal_basis, lb_dpv_legal_basis) & lb_dpv_legal_basis = lb_gdpr_a6_1_a_explicit_consent )
| ( kge_leq(lb_gdpr_a6_1_a_explicit_consent, lb_dpv_legal_basis) & lb_gdpr_a6_1_a_explicit_consent = lb_gdpr_a6_1_a_explicit_consent ) )).
%--------------------------------------------------------------------------
