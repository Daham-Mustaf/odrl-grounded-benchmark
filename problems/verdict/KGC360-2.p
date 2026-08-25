%--------------------------------------------------------------------------
% File     : KGC360-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAllOf(Encryption, AccessControlMethod) against isA TechnicalMeasure (witness condition negated)
% Version  : 1.0
% English  : The controller requires encryption and access control to be in place together; the processor states that the measures it applies are technical ones. Both required measures lie below dpv:TechnicalMeasure in the resource, so a use supplying just those two satisfies the requirement and the statement at once, and it does so in every structure. Verdict: Compatible.
%           : 
%           : This is the superset mode carried by the order: isAllOf asks that its two values lie inside what the use supplies, the request bounds what the use may supply to the technical measures, and the two published assertions place the values within that bound.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC360-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-tom.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc360, axiom,
    ~ ( ( kge_leq(tm_encryption, tm_technical_measure) & kge_leq(tm_access_control_method, tm_technical_measure) & ( kge_leq(tm_encryption, tm_technical_measure)
| kge_leq(tm_access_control_method, tm_technical_measure)
| kge_leq(tm_technical_measure, tm_technical_measure) ) ) )).
%--------------------------------------------------------------------------
