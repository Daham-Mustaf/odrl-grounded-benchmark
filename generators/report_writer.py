"""
report_writer.py
================
Writes the three artefacts a decided problem produces: the case, the report
and the certificate.

    from report_writer import write_report, write_certificate

Three artefacts, one identifier
--------------------------------
A problem produces three things, and they answer three different questions.
Keeping them in three files with one identifier is what lets a reader follow
the chain without reading the pipeline.

    cases/KGC330.ttl                     what was compared
    reports/KGC330-report.ttl            what the answer is
    certificates/KGC330-certificate.ttl  why the answer holds
    certificates/KGC330-2.tstp           the prover's own output

The case is the input: an offer, a request, and the profile binding the
operand.  It is written by the problem generator and is not this module's
business.

The report is the output.  It names the verdict, records the status each
prover returned for each of the two queries, and points at the case it
decided and the certificate that supports it.  It is the artefact a reader
consults to learn what the answer was.

The certificate is the evidence.  For a definite verdict it is a refutation:
the premises it used, where each came from, and which of them a party may
withdraw.  For an Unknown verdict it is a pair of models and the concepts
they disagree about.  It is the artefact a reader consults to learn why, and
to disagree with a premise rather than with the answer.

Why the certificate does not carry the verdict
-----------------------------------------------
It would be shorter to write one file.  The separation is worth its cost
because the two have different authorities and different lifetimes.  A
verdict is what this pipeline concluded on one run with two provers; a
certificate is a mathematical object that stands or falls on its own, and a
reader who reconstructs the refutation from the premises does not need to
trust the run that found it.  Merging them invites a reader to take the
verdict on the certificate's authority, which is backwards: the certificate
is what gives the verdict its authority.

The separation also makes the withdrawability claim legible.  A verdict
resting on a background theory reopens when a party withdraws the
declaration.  Saying so belongs with the premises, not with the answer, and a
reader deciding whether to contest a verdict reads the certificate.
"""

from datetime import date

PREFIXES = """\
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
"""

VERDICT_IRI = {
    "Compatible":   "vrep:Compatible",
    "Incompatible": "vrep:Incompatible",
    "Unknown":      "vrep:Unknown",
}

SOURCE_IRI = {
    "fromResource":         "vrep:fromResource",
    "fromBackgroundTheory": "vrep:fromBackgroundTheory",
    "fromConstraints":      "vrep:fromConstraints",
    "fromOrderAxiom":       "vrep:fromOrderAxiom",
    "fromEqualityAxiom":    "vrep:fromEqualityAxiom",
}


def _esc(s: str) -> str:
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def write_report(pid, verdict, statuses, problem, path,
                 today=None) -> str:
    """The report: what the answer is, and what was run to get it.

    `statuses` maps a prover name to the pair of statuses it returned, as
    (query 1, query 2).  Both provers are recorded whether or not they
    agreed: a disagreement is a fact about the run and hiding it would make
    the artefact less useful than the console output.

    The two queries are named rather than numbered in the prose, since
    "query 1" means nothing to a reader who has not just read Section 6.
    """
    today = today or date.today().isoformat()
    agree = len({tuple(v) for v in statuses.values()}) == 1

    lines = [
        "# What the pipeline concluded for this problem, and what it ran.",
        "#",
        "# The verdict follows from the two queries of Definition Verdict: the",
        "# first asks whether some model admits a use satisfying both",
        "# constraint sets, the second whether some model rules such a use",
        "# out.  Incompatible is the first coming back unsatisfiable,",
        "# Compatible the second, and Unknown both satisfiable.",
        "#",
        "# The evidence is in the certificate this file points at.  A reader",
        "# who wants to know why the verdict holds, or which premises a party",
        "# could withdraw to reopen it, reads that rather than this.",
        "",
        PREFIXES,
        f"kgc:{pid}-report a vrep:VerdictReport ;",
        f'    dcterms:title "Verdict for {pid}"@en ;',
        f'    dcterms:date "{today}"^^xsd:date ;',
        f"    vrep:case <../cases/{pid}.ttl> ;",
        f"    vrep:certificate <../certificates/{pid}-certificate.ttl> ;",
        f"    vrep:verdict {VERDICT_IRI[verdict]} ;",
    ]

    if problem.get("left_operand"):
        lines.append(f'    vrep:leftOperand "{_esc(problem["left_operand"])}" ;')
    if problem.get("sort"):
        lines.append(f"    vrep:sort vrep:{problem['sort']} ;")
    if problem.get("resource"):
        lines.append(f"    vrep:resource <{problem['resource']}> ;")
    if problem.get("background_theory"):
        lines.append(f"    vrep:backgroundTheory <{problem['background_theory']}> ;")

    lines.append(f"    vrep:proversAgree {'true' if agree else 'false'} ;")

    runs = []
    for prover, (q1, q2) in sorted(statuses.items()):
        runs.append(f"""\
        [ vrep:prover "{_esc(prover)}" ;
          vrep:query1Status "{_esc(q1)}" ;
          vrep:query2Status "{_esc(q2)}" ]""")
    lines.append("    vrep:proverRun\n" + " ,\n".join(runs) + " .")

    if not agree:
        lines += [
            "",
            "# The provers returned different statuses for this problem.  The",
            "# verdict above is what the pipeline concluded; the disagreement",
            "# is recorded because it bears on how much the conclusion is",
            "# worth, and a reader should see it without rerunning anything.",
        ]

    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")
    return text


def write_certificate(pid, verdict, kind, path, today=None,
                      prover=None, premises=(), withdrawable=(),
                      artefact=None, models=(), differing=(), comment=None) -> str:
    """The certificate: why the verdict holds.

    For a definite verdict, a refutation with its premises attributed to
    where each came from.  The premises a party may withdraw are marked, and
    that marking is the certificate's practical point: a verdict resting on
    what an authority published is not open to the parties, and one resting
    on what they declared is.

    For Unknown, the two models and the concepts they disagree about.  That
    disagreement is the question the vocabulary leaves open, and naming it
    tells a reader what a declaration would have to settle.
    """
    today = today or date.today().isoformat()

    head = [
        "# Why the verdict for this problem holds.",
        "#",
    ]
    if kind == "Refutation":
        head += [
            "# A refutation of one of the two queries, with the premises it",
            "# used.  Each premise is attributed: an assertion the authority",
            "# published, a declaration the parties made, the constraints",
            "# themselves, or an instance of an axiom of the order.",
            "#",
            "# The declarations are the premises a party may withdraw.  Doing",
            "# so reopens the verdict, and the verdict then becomes Unknown",
            "# rather than reversing: withdrawing a declaration removes what",
            "# settled the question, it does not settle it the other way.",
        ]
    else:
        head += [
            "# Two models, one for each query, and the concepts they disagree",
            "# about.  Both queries were satisfiable, so the resource and the",
            "# background theory leave the question open, and the difference",
            "# below is what a declaration would have to settle.",
        ]
    head += ["", PREFIXES]

    lines = head + [
        f"kgc:{pid}-certificate a vrep:Certificate, vrep:{kind} ;",
        f'    dcterms:date "{today}"^^xsd:date ;',
        f"    vrep:certifies kgc:{pid}-report ;",
        f"    vrep:verdict {VERDICT_IRI[verdict]} ;",
    ]

    if comment:
        lines.append(f'    rdfs:comment "{_esc(comment)}"@en ;')
    if prover:
        lines.append(f'    vrep:producedBy "{_esc(prover)}" ;')
    if artefact:
        lines.append(f"    vrep:proofArtefact <{artefact}> ;")

    if kind == "Refutation":
        blocks = []
        for source, name, label in premises:
            entry = [
                "        [ vrep:premiseSource "
                f"{SOURCE_IRI.get(source, 'vrep:' + source)} ;",
                f'          vrep:formulaName "{_esc(name)}" ;',
                f'          rdfs:label "{_esc(label)}"@en ;',
                f"          vrep:withdrawable "
                f"{'true' if name in withdrawable else 'false'} ]",
            ]
            blocks.append("\n".join(entry))
        lines.append("    vrep:attributedAssertion\n" + " ,\n".join(blocks) + " ;")
        lines.append(
            f"    vrep:withdrawablePremiseCount {len(withdrawable)} .")

        if withdrawable:
            lines += [
                "",
                "# This verdict rests on what the parties declared.  Any of",
                "# the premises marked withdrawable can be retracted by the",
                "# party that made it, and the verdict reopens as Unknown.",
            ]
        else:
            lines += [
                "",
                "# No premise of this refutation is a party declaration.  The",
                "# verdict rests on the constraints and on what the authority",
                "# published, and no party can reopen it by withdrawing an",
                "# assertion of their own.",
            ]
    else:
        for i, m in enumerate(models, start=1):
            lines.append(f"    vrep:model [ vrep:query {i} ; "
                         f"vrep:modelArtefact <{m}> ] ;")
        if differing:
            for c in differing:
                lines.append(f'    vrep:differsOn "{_esc(c)}" ;')
        lines.append(f"    vrep:differingConceptCount {len(differing)} .")

    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")
    return text