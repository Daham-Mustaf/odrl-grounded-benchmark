"""
report.py
=========
Writes the expected result of a benchmark problem as RDF.

Each problem carries one report per left operand: which resource grounds it,
which sort it declares, and which verdict is expected.  The harness compares
prover output against these, and the baseline comparison reads the same file.

The vocabulary is our own.  It deliberately does not subclass the ODRL
compliance report model: satisfaction of a constraint by a use and
compatibility of two constraint sets are different questions, so
vrep:Compatible is not a kind of report:Satisfied.  Where a problem is also
evaluated by a compliance-report tool, vrep:comparedWith links the two.

Certificate fields are declared but only emitted when a certificate has been
extracted.  Until then a report carries the verdict alone.
"""

from pathlib import Path

NS = "https://w3id.org/odrl-kb/verdict-report#"

PREFIXES = """\
@prefix vrep: <https://w3id.org/odrl-kb/verdict-report#> .
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""

VERDICT = {
    "Compatible":   "vrep:Compatible",
    "Incompatible": "vrep:Incompatible",
    "Unknown":      "vrep:Unknown",
}

SORT = {"nom": "vrep:nom", "tax": "vrep:tax", "mer": "vrep:mer"}


def vocabulary() -> str:
    """The vocabulary itself, written once into the artefact."""
    return PREFIXES + """
<https://w3id.org/odrl-kb/verdict-report> a owl:Ontology ;
    dcterms:title "ODRL Verdict Report Vocabulary"@en ;
    dcterms:description "Terms for recording the verdict on two ODRL "
        "constraint sets over one left operand, under a declared resource "
        "and background theory, together with the evidence for it."@en .

vrep:OperandReport a rdfs:Class ;
    rdfs:label "Operand verdict report"@en ;
    rdfs:comment "The verdict on the constraints two policies place on one "
        "left operand, under a declared resource and background theory."@en .

vrep:leftOperand      a rdf:Property ; rdfs:domain vrep:OperandReport ; rdfs:range odrl:LeftOperand .
vrep:offerConstraint  a rdf:Property ; rdfs:domain vrep:OperandReport ; rdfs:range odrl:Constraint .
vrep:requestConstraint a rdf:Property ; rdfs:domain vrep:OperandReport ; rdfs:range odrl:Constraint .
vrep:resource         a rdf:Property ; rdfs:domain vrep:OperandReport .
vrep:backgroundTheory a rdf:Property ; rdfs:domain vrep:OperandReport .
vrep:sort             a rdf:Property ; rdfs:domain vrep:OperandReport .
vrep:verdict          a rdf:Property ; rdfs:domain vrep:OperandReport ; rdfs:range vrep:Verdict .
vrep:certificate      a rdf:Property ; rdfs:domain vrep:OperandReport ; rdfs:range vrep:Certificate .

vrep:Verdict a rdfs:Class .
vrep:Compatible   a rdfs:Class ; rdfs:subClassOf vrep:Verdict .
vrep:Incompatible a rdfs:Class ; rdfs:subClassOf vrep:Verdict .
vrep:Unknown      a rdfs:Class ; rdfs:subClassOf vrep:Verdict ;
    rdfs:comment "The resource and background theory do not determine "
        "whether a common use exists.  Distinct from the compliance report "
        "model's performance-unknown state."@en .

vrep:nom a vrep:Sort ; rdfs:comment "Identity only."@en .
vrep:tax a vrep:Sort ; rdfs:comment "Subsumption."@en .
vrep:mer a vrep:Sort ; rdfs:comment "Parthood."@en .

vrep:Certificate a rdfs:Class .
vrep:Refutation  a rdfs:Class ; rdfs:subClassOf vrep:Certificate .
vrep:Model       a rdfs:Class ; rdfs:subClassOf vrep:Certificate .
vrep:UngroundedValue a rdfs:Class ; rdfs:subClassOf vrep:Certificate .

vrep:premise       a rdf:Property ; rdfs:domain vrep:Refutation .
vrep:premiseSource a rdf:Property ;
    rdfs:comment "Whether a premise comes from the resource or from the "
        "background theory.  A party may withdraw the second and not the "
        "first."@en .
vrep:fromResource        a vrep:PremiseSource .
vrep:fromBackgroundTheory a vrep:PremiseSource .

vrep:comparedWith a rdf:Property ;
    rdfs:comment "An evaluation of the same problem by another tool."@en .
"""


def _report(p: dict, verdict: str) -> str:
    pid = p["id"]
    lines = [
        f":{pid}-report a vrep:OperandReport ;",
        f'    dcterms:identifier "{pid}" ;',
    ]
    if p.get("left_operand"):
        lines.append(f"    vrep:leftOperan      d odrl:{p['left_operand']} ;")
    if p.get("sort"):
        lines.append(f"    vrep:sort {SORT[p['sort']]} ;")
    if p.get("resource"):
        lines.append(f"    vrep:resource <{p['resource']}> ;")
    if p.get("background_theory"):
        lines.append(f"    vrep:backgroundTheory <{p['background_theory']}> ;")
    if p.get("ungrounded"):
        lines.append(f'    vrep:certificate [ a vrep:UngroundedValue ; '
                     f'dcterms:identifier "{p["ungrounded"]}" ] ;')
    lines.append(f"    vrep:verdict {VERDICT[verdict]} .")
    return "\n".join(lines) + "\n"


def write_report(p: dict, verdict: str, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{p['id']}-report.ttl"
    path.write_text(PREFIXES + "\n" + _report(p, verdict), encoding="utf-8")
    return path


def write_vocabulary(ontology_dir: Path) -> Path:
    ontology_dir.mkdir(parents=True, exist_ok=True)
    path = ontology_dir / "verdict-report.ttl"
    path.write_text(vocabulary(), encoding="utf-8")
    return path