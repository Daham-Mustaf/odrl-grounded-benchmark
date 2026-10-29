"""
targets.py
==========

The resources the policies are about.  A policy names its target by IRI;
this module gives each IRI a type and a title, once, so that every case
file describes the thing the rule applies to and no family words it
differently.

    drk:manuscripts   digitised manuscripts a library holds
    drk:dataset       personal data a controller holds
    drk:traffic-data  traffic sensor data a city's data platform holds
    drk:work          a work a publisher distributes

The data collections are dcat:Dataset.  The work is
dcterms:BibliographicResource.  The case writers call `with_targets` on
the policy Turtle, so a generator never writes a target node by hand.
"""

import re

DCAT_PREFIX = "@prefix dcat:    <http://www.w3.org/ns/dcat#> ."

# IRI -> (rdf:type, title in plain words)
TARGETS = {
    "drk:manuscripts": ("dcat:Dataset", "Digitised manuscripts of a library"),
    "drk:dataset":     ("dcat:Dataset", "Personal data held by a controller"),
    "drk:traffic-data": ("dcat:Dataset", "Traffic sensor data of a city"),
    "drk:work":        ("dcterms:BibliographicResource",
                        "A work distributed by a publisher"),
}


def target_node(iri: str) -> str:
    kind, title = TARGETS[iri]
    return f'{iri} a {kind} ;\n    dcterms:title "{title}"@en .'


def with_targets(ttl: str) -> str:
    """Add a typed, titled node for each target the policies name.

    The nodes go straight after the prefix block, so a comment written
    above a policy stays with that policy, and a blank line separates them
    from whatever follows.  A target already described in the text is left
    alone, so the helper can be applied twice.
    """
    named = []
    for iri in re.findall(r"odrl:target\s+(drk:[\w-]+)", ttl):
        if iri not in named:
            named.append(iri)
    nodes = [target_node(iri) for iri in named
             if not re.search(rf"^{re.escape(iri)}\s+a\s", ttl, re.M)]
    if not nodes:
        return ttl
    end = list(re.finditer(r"^@prefix[^\n]*$", ttl, re.M))[-1].end()
    prefix = ""
    if "dcat:" in "".join(nodes) and not re.search(r"^@prefix dcat:", ttl, re.M):
        prefix = "\n" + DCAT_PREFIX
    rest = ttl[end:]
    if not rest.startswith("\n\n"):
        rest = "\n" + rest
    return ttl[:end] + prefix + "\n\n" + "\n\n".join(nodes) + rest
