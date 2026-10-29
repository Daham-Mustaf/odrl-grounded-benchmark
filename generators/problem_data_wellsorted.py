"""
problem_data_wellsorted.py
==========================
The drafting-time check.  Nine problems: ill-sorted constraints, one per
sort, the two parthood operators at nom and hasPart at tax, and one
well-sorted control per sort.

These build no queries.  Well-sortedness is decided by the signature alone,
before any resource is opened, so a rejected constraint never reaches a
prover.  That is the claim, and the absence of query files is the evidence
for it.

    KGC100  spatial  isA        gn:Europe    mer   rejected
    KGC101  purpose  isPartOf   dpv:NCP      tax   rejected
    KGC105  purpose  hasPart    dpv:NCP      tax   rejected
    KGC102  language isA        bcp:de       nom   rejected
    KGC103  language isPartOf   bcp:de       nom   rejected
    KGC104  language hasPart    bcp:de       nom   rejected
    KGC110  spatial  isPartOf   gn:Europe    mer   accepted
    KGC111  purpose  isA        dpv:NCP      tax   accepted
    KGC112  language eq         bcp:de       nom   accepted

The six rejections are the same error in three settings: an operator put to
a resource that supplies a different relation.  KGC100 is the case the paper
uses throughout, a gazetteer asked about kinds.
"""

VALUE = {
    "gn:Europe":  "<https://sws.geonames.org/6255148/>",
    "dpv:NCP":    "dpv:NonCommercialPurpose",
    "dpv:NCR":    "dpv:NonCommercialResearch",
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
    "KGC100": "Use in places that are a kind of Europe only",
    "KGC101": "Use within non-commercial purposes",
    "KGC105": "Use for a purpose that includes non-commercial research",
    "KGC102": "Use in a kind of German only",
    "KGC103": "Use within German",
    "KGC104": "Use in a language that includes German",
    "KGC110": "Use within Europe",
    "KGC111": "Use for non-commercial purposes or any narrower purpose",
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


def _problem(pid, operand, operator, value, sort, accepted, description,
             summary, reason):
    """summary and reason are what a reader sees.  The signature decides
    whether the constraint is accepted; gen_wellsorted checks that against
    `accepted` and never uses its message as text."""
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
        "summary":           summary,
        "reason":            reason,
        "ttl":               _ttl(pid, operand, operator, value),
        "binding":           BINDING[operand],
    }


PROBLEMS = [

    _problem("KGC100", "spatial", "isA", "gn:Europe", "mer", False,
             "A policy that gives a place relies on a gazetteer, which states "
             "which place is part of which.  isA asks whether one value is a "
             "kind of another, and a place is not a kind of Europe; it is a "
             "part of it.  The operator does not apply to this kind of "
             "value, and the policy is rejected before GeoNames is opened.",
             "A German library's policy uses isA with Europe, a place in "
             "GeoNames.",
             "isA asks whether one value is a kind of another.  GeoNames "
             "only states which place is part of which, so the operator does "
             "not apply to this kind of value."),

    _problem("KGC101", "purpose", "isPartOf", "dpv:NCP", "tax", False,
             "A policy that gives a purpose relies on DPV, which arranges "
             "purposes as kinds.  isPartOf asks whether one value is part of "
             "another.  The operator does not apply to this kind of value, "
             "and the policy is rejected before DPV is opened.",
             "A German library's policy uses isPartOf with non-commercial "
             "purposes, a purpose in DPV.",
             "isPartOf asks whether one value is part of another.  DPV only "
             "states which purpose is a kind of which, so the operator does not "
             "apply to this kind of value."),

    _problem("KGC105", "purpose", "hasPart", "dpv:NCR", "tax", False,
             "A policy that gives a purpose relies on DPV, which arranges "
             "purposes as kinds.  hasPart asks whether one value has another "
             "as a part.  The operator does not apply to this kind of value, "
             "and the policy is rejected before DPV is opened.",
             "A German library's policy uses hasPart with non-commercial "
             "research, a purpose in DPV.",
             "hasPart asks whether one value has another as a part.  DPV "
             "only states which purpose is a kind of which, so the operator "
             "does not apply to this kind of value."),

    _problem("KGC102", "language", "isA", "bcp:de", "nom", False,
             "A policy that gives a language relies on the IANA registry.  "
             "For the fifteen languages used here the registry states no "
             "order, and this reading takes languages as names only.  isA asks whether one value is a kind of another.  "
             "The operator does not apply, and the policy is rejected before "
             "the registry is opened.",
             "A German library's policy uses isA with German, a language in "
             "the IANA registry.",
             "isA asks whether one value is a kind of another.  This reading takes languages as names only: none of the fifteen languages used here belongs to a larger language in the IANA registry (RFC 5646), and the reading takes no order from the registry, so the operator does not apply to this kind of value."),

    _problem("KGC103", "language", "isPartOf", "bcp:de", "nom", False,
             "A policy that gives a language relies on the IANA registry.  "
             "For the fifteen languages used here the registry states no "
             "order, and this reading takes languages as names only.  isPartOf asks whether one value is part of another.  "
             "The operator does not apply, and the policy is rejected before "
             "the registry is opened.",
             "A German library's policy uses isPartOf with German, a language in "
             "the IANA registry.",
             "isPartOf asks whether one value is part of another.  This reading takes languages as names only: none of the fifteen languages used here belongs to a larger language in the IANA registry (RFC 5646), and the reading takes no order from the registry, so the operator does not apply to this kind of value."),

    _problem("KGC104", "language", "hasPart", "bcp:de", "nom", False,
             "A policy that gives a language relies on the IANA registry.  "
             "For the fifteen languages used here the registry states no "
             "order, and this reading takes languages as names only.  hasPart asks whether one value has another as a part.  "
             "The operator does not apply, and the policy is rejected before "
             "the registry is opened.  A drafter who means a language that includes German among the languages of the use writes isAllOf with the single value German.",
             "A German library's policy uses hasPart with German, a language in "
             "the IANA registry.",
             "hasPart asks whether one value has another as a part.  This reading takes languages as names only: none of the fifteen languages used here belongs to a larger language in the IANA registry (RFC 5646), and the reading takes no order from the registry, so the operator does not apply to this kind of value."),

    _problem("KGC110", "spatial", "isPartOf", "gn:Europe", "mer", True,
             "Control.  isPartOf asks whether one value is part of another, "
             "and a gazetteer states which place is part of which, so the "
             "operator applies and the policy goes on to a verdict.",
             "A German library's policy uses isPartOf with Europe, a place "
             "in GeoNames.",
             "isPartOf asks whether one value is part of another, and "
             "GeoNames states which place is part of which, so the operator "
             "applies to this kind of value and the policy goes on to a "
             "verdict."),

    _problem("KGC111", "purpose", "isA", "dpv:NCP", "tax", True,
             "Control.  isA asks whether one value is a kind of another, and "
             "DPV arranges purposes as kinds, so the operator applies.",
             "A German library's policy uses isA with non-commercial "
             "purposes, a purpose in DPV.",
             "isA asks whether one value is a kind of another, and DPV states "
             "which purpose is a kind of which, so the operator applies to "
             "this kind of value and the policy goes on to a verdict."),

    _problem("KGC112", "language", "eq", "bcp:de", "nom", True,
             "Control.  eq asks only whether two values are the same, a "
             "question that makes sense for every kind of value, so the "
             "operator applies to every kind of value.",
             "A German library's policy uses eq with German, a language in "
             "the IANA registry.",
             "eq asks only whether two values are the same, a question that "
             "makes sense for languages, so the operator applies and the "
             "policy goes on to a verdict.  Whether the registry decides that "
             "question is a separate matter (KGC371)."),
]
