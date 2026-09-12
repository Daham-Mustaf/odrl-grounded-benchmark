%--------------------------------------------------------------------------
% File     : KGC360-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAllOf(Encryption, AccessControlMethod) against isA TechnicalMeasure (witness condition asserted)
% Version  : 1.0
% English  : A controller requires encryption and access control, while a processor applies technical measures.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC360-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-tom.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc360, axiom,
    ( kge_leq(tm_encryption, tm_technical_measure) & kge_leq(tm_access_control_method, tm_technical_measure) & ( kge_leq(tm_encryption, tm_technical_measure)
| kge_leq(tm_access_control_method, tm_technical_measure)
| kge_leq(tm_technical_measure, tm_technical_measure) ) )).
%--------------------------------------------------------------------------
