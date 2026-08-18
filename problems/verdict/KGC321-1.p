%--------------------------------------------------------------------------
% File     : KGC321-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, eq ft:PDF against eq ft:PDFA1A, under a declared distinctness (witness condition asserted)
% Version  : 1.0
% English  : The constraints of KGC320 under a background theory in which the parties declare the two formats distinct.  Incompatible, and the sole premise is the declaration: the table contributed nothing, so withdrawing the declaration returns the verdict to Unknown and there is nothing else holding it.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC321-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/EUFT-filetype.ax').
include('axioms/EUFT-filetype-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: one declared distinctness, from
% EUFT-filetype-declared.ax.  The table separates nothing itself.

% --- witness condition asserted ------------------------------------------
fof(w_kgc321, axiom,
    ( ( ft_pdf = ft_pdf & ft_pdf = ft_pdfa1a )
| ( ft_pdfa1a = ft_pdf & ft_pdfa1a = ft_pdfa1a ) )).
%--------------------------------------------------------------------------
