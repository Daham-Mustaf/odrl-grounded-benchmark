%------------------------------------------------------------------------------
% File     : KGC083+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Distribute in any language except English and Italian against distribute in Italian only: some use meets both
% Version  : Especial.
% English  : English and Italian rights were sold separately, so a publisher
%            permits any language except English and Italian. The licensee
%            distributes in Italian. This problem states that some use meets
%            the two policies. It is also a check of KGC378: A translation
%            licence covers a German or a French edition. The licensee
%            publishes in French. There it states that no use meets the two
%            policies. It is also a check of KGC398: A translation licence
%            covers at least one of a German and a French edition. The
%            licensee publishes in both Dutch and French. There it states that
%            no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC377-1 [Mus26]
%          : KGC378-2 [Mus26]
%          : KGC398-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : This problem is 3 checks whose formulas and include lines are the
%            same after renaming the case. KGC377 is Incompatible. Its two
%            problems state that some use meets the two policies (KGC083) and
%            that no use does (KGC084); here the first is Unsatisfiable and
%            the second Satisfiable. KGC378 is Compatible. Its two problems
%            state that some use meets the two policies (KGC085) and that no
%            use does (KGC083); here the first is Satisfiable and the second
%            Unsatisfiable. KGC398 is Compatible. Its two problems state that
%            some use meets the two policies (KGC085) and that no use does
%            (KGC083); here the first is Satisfiable and the second
%            Unsatisfiable. A pair of policies is Incompatible when the first
%            is Unsatisfiable, Compatible when the second is Unsatisfiable,
%            and Unknown when both are Satisfiable; a Satisfiable problem also
%            shows the statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+1.ax').

fof(w_kgc377, axiom,
    ~ ( $true )).
%------------------------------------------------------------------------------
