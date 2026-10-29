%--------------------------------------------------------------------------
% File     : KGC321-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, eq ft:PDF against eq ft:PDFA1A, under a declared distinctness (witness condition asserted)
% Version  : 1.0
% English  : As KGC320, with the two formats declared distinct.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
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
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_ft_pdf_distinct_ft_pdfa1a, axiom,
    ft_pdf != ft_pdfa1a).

% --- witness condition asserted ------------------------------------------
fof(w_kgc321, axiom,
    ( ( ft_pdf = ft_pdf & ft_pdf = ft_pdfa1a )
| ( ft_pdfa1a = ft_pdf & ft_pdfa1a = ft_pdfa1a ) )).
%--------------------------------------------------------------------------
