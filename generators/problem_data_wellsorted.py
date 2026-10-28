"""
problem_data_wellsorted.py
==========================
The drafting-time check.  Six problems: one ill-sorted constraint per sort
and one well-sorted control per sort.

These build no queries.  Well-sortedness is decided by the signature alone,
before any resource is opened, so a rejected constraint never reaches a
prover.  That is the claim, and the absence of query files is the evidence
for it.

    KGC100  spatial  isA        gn:Europe    mer   rejected
    KGC101  purpose  isPartOf   dpv:NCP      tax   rejected
    KGC102  language isA        bcp:de       nom   rejected
    KGC110  spatial  isPartOf   gn:Europe    mer   accepted
    KGC111  purpose  isA        dpv:NCP      tax   accepted
    KGC112  language eq         bcp:de       nom   accepted

The three rejections are the same error in three settings: an operator put to
a resource that supplies a different relation.  KGC100 is the case the paper
uses throughout, a gazetteer asked about kinds.
"""

VALUE = {
    "gn:Europe":  "<https://sws.geonames.org/6255148/>",
    "dpv:NCP":    "dpv:NonCommercialPurpose",
    "bcp:de":     "bcp47:de",
}

PREFIX = {
    # GeoNames IRIs end in a slash, so they are written in full and need
    # no prefix.
    "spatial":  ("gn",      ""),
    "purpose":  ("dpv",     "@prefix dpv:     <https://w3id.org/dpv#> .\n"
                            "@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> ."),
    "language": ("bcp47",   "@prefix bcp47:   <https://w3id.org/odrl-kb/bcp47#> ."),
}

RESOURCE = {
    "spatial":  ("https://w3id.org/odrl-kb/geonames-europe",
                 "https://w3id.org/odrl-kb/geonames-europe/empty"),
    "purpose":  ("https://w3id.org/odrl-kb/dpv-purposes",
                 "https://w3id.org/odrl-kb/dpv-purposes/empty"),
    "language": ("https://w3id.org/odrl-kb/bcp47",
                 "https://w3id.org/odrl-kb/bcp47/distinct"),
}

# The left operand each problem writes.  Purposes are DPV concepts, so the
# DPV-ODRL operand is used, as DPV-ODRL recommends; the GeoNames and BCP 47
# values are not from DPV and keep the ODRL operands.
LEFT = {
    "spatial":  "odrl:spatial",
    "purpose":  "dpv-odrl:Purpose",
    "language": "odrl:language",
}

BINDING = {
    "spatial":  "https://w3id.org/odrl-kb/profile/b-spatial-geonames",
    "purpose":  "https://w3id.org/odrl-kb/profile/b-purpose",
    "language": "https://w3id.org/odrl-kb/profile/b-language-bcp47",
}

# The policy title is the rule in plain words, starting with the action and
# following the operator: only for isA, within for isPartOf.
TITLE = {
    "KGC100": "Use in a kind of Europe only",
    "KGC101": "Use within non-commercial purposes",
    "KGC102": "Use in a kind of German only",
    "KGC110": "Use within Europe",
    "KGC111": "Use for non-commercial purposes only",
    "KGC112": "Use in German only",
}


def _ttl(pid: str, operand: str, operator: str, value: str) -> str:
    _, prefix_line = PREFIX[operand]
    profile = ("\n    odrl:profile dpv-odrl: ;"
               if LEFT[operand].startswith("dpv-odrl:") else "")
    # Only the prefixes the file uses.
    prefixes = "\n".join(line for line in (
        "@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        prefix_line,
        "@prefix drk:     <https://w3id.org/odrl-kb/drk/> .",
        "@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .",
    ) if line)
    return f"""\
{prefixes}

drk:policy-{pid[3:]}-1 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-1 ;{profile}
    dcterms:title "{TITLE[pid]}"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:{pid}-p1-r1 .

kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-p1-c1 .

kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand {LEFT[operand]} ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {VALUE[value]} ."""


def _problem(pid, operand, operator, value, sort, accepted, description):
    resource, background = RESOURCE[operand]
    return {
        "id":                pid,
        "subdir":            "wellsorted",
        "name":              f"{operand}, {operator} {value}",
        "left_operand":      operand,
        "operator":          operator,
        "value":             value,
        "arity":             1,
        "sort":              sort,
        "resource":          resource,
        "background_theory": background,
        "accepted":          accepted,
        "description":       description,
        "ttl":               _ttl(pid, operand, operator, value),
        "binding":           BINDING[operand],
    }


PROBLEMS = [

    _problem("KGC100", "spatial", "isA", "gn:Europe", "mer", False,
             "The operand is grounded in a gazetteer, which supplies "
             "parthood.  isA requires subsumption.  The constraint asks "
             "whether a region is a kind of Europe rather than a part of it, "
             "and is rejected before GeoNames is opened."),

    _problem("KGC101", "purpose", "isPartOf", "dpv:NCP", "tax", False,
             "The operand is grounded in a purpose taxonomy, which supplies "
             "subsumption.  isPartOf requires parthood.  The constraint is "
             "rejected before the vocabulary is opened."),

    _problem("KGC102", "language", "isA", "bcp:de", "nom", False,
             "The operand is grounded in a registry, which supplies identity "
             "and no order.  isA requires subsumption.  The constraint is "
             "rejected before the registry is opened."),

    _problem("KGC110", "spatial", "isPartOf", "gn:Europe", "mer", True,
             "Control.  isPartOf requires parthood and the gazetteer supplies "
             "it, so the constraint is well sorted and proceeds to the "
             "verdict."),

    _problem("KGC111", "purpose", "isA", "dpv:NCP", "tax", True,
             "Control.  isA requires subsumption and the taxonomy supplies "
             "it."),

    _problem("KGC112", "language", "eq", "bcp:de", "nom", True,
             "Control.  eq requires only identity, which every resource "
             "supplies, so it is well sorted at every sort."),
]