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
    "bcp:de":     "odrlkb:de",
}

PREFIX = {
    "spatial":  ("gn",      "@prefix gn:      <https://sws.geonames.org/> ."),
    "purpose":  ("dpv",     "@prefix dpv:     <https://w3id.org/dpv#> ."),
    "language": ("odrlkb",  "@prefix odrlkb:  <https://w3id.org/odrl-kb/bcp47#> ."),
}

RESOURCE = {
    "spatial":  ("https://w3id.org/odrl-kb/geonames-europe",
                 "https://w3id.org/odrl-kb/geonames-europe/admin-siblings"),
    "purpose":  ("https://w3id.org/odrl-kb/dpv-purpose",
                 "https://w3id.org/odrl-kb/dpv-purpose/declared"),
    "language": ("https://w3id.org/odrl-kb/bcp47",
                 "https://w3id.org/odrl-kb/bcp47/uniqueness"),
}

BINDING = {
    "spatial":  "https://w3id.org/odrl-kb/profile/b-spatial-geonames",
    "purpose":  "https://w3id.org/odrl-kb/profile/b-purpose-dpv",
    "language": "https://w3id.org/odrl-kb/profile/b-language-bcp47",
}

def _ttl(pid: str, operand: str, operator: str, value: str) -> str:
    _, prefix_line = PREFIX[operand]
    return f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
{prefix_line}
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .
@prefix bind:    <https://w3id.org/odrl-kb/binding#> .
@prefix report:  <https://w3id.org/force/compliance-report#> .

drk:manuscripts a dcterms:Dataset ;
    dcterms:title "Digitised manuscripts, Bavarian State Library"@en .

drk:offer a odrl:Offer ;
    dcterms:title "BSB offer, {operand} constrained by {operator}"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:{operand} ;
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