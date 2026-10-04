#!/usr/bin/env python3
"""
validate_cases.py
=================
Checks the shape of every case file against the agreed case shape.

    uv run generators/validate_cases.py [--cases cases] [--problems problems]

Errors (exit 1):
    - the file does not parse as Turtle, or lacks the generated-file header
    - a term of the Compliance Report Model, or odrl:Offer / odrl:Request
    - a policy without odrl:uid equal to its own IRI
    - odrl:profile dpv-odrl: present without a dpv-odrl operand, or missing
      with one
    - a set operator whose right operand is not an RDF list, or another
      operator with a list or with more than one value
    - an operand verdict report whose policies or constraints are not the
      ones in the file, or that lacks binding, background theory or
      verdict; an Unknown without a reason, a reason without an Unknown,
      a definite verdict without a certificate
    - vrep:readAgainst pointing at a case that does not exist or does not
      point back

Warnings (reported, exit 0):
    - a binding IRI that no profile file under problems/resources declares
    - a background theory IRI that no file under problems/background
      declares
    - a constraint on a dpv-odrl left operand whose operator the operand's
      DPV-ODRL usage note does not allow

The first two warnings are the known binding drift. The third lists the
cases that break the operator notes of the profile they declare; which of
them change, and which notes change, is being settled with the DPV-ODRL
editors. All are listed rather than failed so that they stay visible.
"""

import argparse
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, Namespace, RDF, URIRef, BNode
from rdflib.namespace import RDFS, DCTERMS
from rdflib.collection import Collection

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
VREP = Namespace("https://w3id.org/odrl-kb/verdict-report#")
DPVODRL = "https://w3id.org/dpv/mappings/odrl#"
CRM = "https://w3id.org/force/compliance-report#"
SET_OPERATORS = {"isAnyOf", "isAllOf", "isNoneOf"}

# The skos:note of each DPV-ODRL left operand: "Only the ... operators MUST
# be used."  Copied from mappings/odrl/dpv-odrl.ttl on the dev branch of
# https://github.com/w3c-cg/dpv (commit 8a50545, 6 August 2026).  The
# measure operands all carry the same note as TechnicalOrganisationalMeasure.
_FIVE = {"isA", "eq", "neq", "isAnyOf", "isNoneOf"}
OPERATOR_NOTES = {
    "LegalBasis": {"isA", "eq", "neq"},
    "Purpose": _FIVE,
    "Location": {"eq", "neq", "isAnyOf", "isNoneOf"},
    "Status": _FIVE,
    "TechnicalOrganisationalMeasure": _FIVE,
    "TechnicalMeasure": _FIVE,
    "OrganisationalMeasure": _FIVE,
}
from writers import GENERATED_HEADER as HEADER


def declared(paths, pattern):
    out = set()
    for p in paths:
        g = Graph().parse(p, format="turtle")
        out |= {str(s) for s in g.subjects(RDF.type, pattern)}
    return out


def rules_constraints(g, policy):
    rules = [o for pred in (ODRL.permission, ODRL.prohibition, ODRL.obligation)
             for o in g.objects(policy, pred)]
    return {c for r in rules for c in g.objects(r, ODRL.constraint)}


def atomic(g, c):
    """The atomic constraints under c, through a Logical Constraint."""
    out = []
    for conn in (ODRL["and"], ODRL["or"], ODRL.xone, ODRL.andSequence):
        for lst in g.objects(c, conn):
            for m in Collection(g, lst):
                out += atomic(g, m)
    return out or [c]


def check(path: Path, bindings, theories, errs, warns, twins, notes):
    text = path.read_text(encoding="utf-8")
    e = lambda msg: errs.append(f"{path.name}: {msg}")
    if not text.startswith(HEADER):
        e("no generated-file header")
    if CRM in text or re.search(r"\breport:[A-Za-z]", text):
        e("uses the Compliance Report Model")
    if re.search(r"odrl:(Offer|Request)\b", text):
        e("odrl:Offer or odrl:Request")
    try:
        g = Graph().parse(data=text, format="turtle")
    except Exception as x:                            # noqa: BLE001
        e(f"does not parse: {x}")
        return

    policies = set(g.subjects(RDF.type, ODRL.Set))
    for pol in policies:
        uid = list(g.objects(pol, ODRL.uid))
        if uid != [pol]:
            e(f"{pol} has odrl:uid {uid}, expected itself")
        cons = [a for c in rules_constraints(g, pol) for a in atomic(g, c)]
        uses = any(str(lo).startswith(DPVODRL)
                   for c in cons for lo in g.objects(c, ODRL.leftOperand))
        prof = URIRef(DPVODRL) in set(g.objects(pol, ODRL.profile))
        if uses != prof:
            e(f"{pol}: odrl:profile dpv-odrl: {'missing' if uses else 'without a dpv-odrl operand'}")
        rejected = any(o.toPython() is False
                       for o in g.objects(None, VREP.wellSorted))
        for c in cons:
            op = str(next(g.objects(c, ODRL.operator), "")).rsplit("/", 1)[-1]
            for lo in g.objects(c, ODRL.leftOperand):
                name = str(lo)[len(DPVODRL):] if str(lo).startswith(DPVODRL) else None
                allowed = OPERATOR_NOTES.get(name)
                if allowed is not None and op not in allowed:
                    notes.append(f"{path.stem}: dpv-odrl:{name} with {op}"
                                 + (" (ill-sorted by design)" if rejected else ""))
            ros = list(g.objects(c, ODRL.rightOperand))
            is_list = len(ros) == 1 and (ros[0] == RDF.nil or
                                         (ros[0], RDF.first, None) in g)
            if op in SET_OPERATORS and not is_list:
                e(f"{c}: {op} right operand is not an RDF list")
            if op not in SET_OPERATORS and (len(ros) != 1 or is_list):
                e(f"{c}: {op} takes one value, has {len(ros)}"
                  + (" (a list)" if is_list else ""))

    # Every report says what the policies ask (dcterms:description) and why
    # the verdict is what it is (rdfs:comment), in words that do not suggest
    # an ODRL evaluation request.
    for rep in set(g.subjects(RDF.type, VREP.OperandVerdictReport)) | \
            set(g.subjects(RDF.type, VREP.WellSortednessReport)):
        for prop, label in ((DCTERMS.description, "dcterms:description"),
                            (RDFS.comment, "rdfs:comment")):
            vals = list(g.objects(rep, prop))
            if len(vals) != 1:
                e(f"report needs exactly one {label}, has {len(vals)}")
            for v in vals:
                if re.search(r"\b(offer|request)", str(v), re.I):
                    warns.append(f"{path.name}: {label} says offer or request")

    for rep in g.subjects(RDF.type, VREP.WellSortednessReport):
        cs = list(g.objects(rep, VREP.constraint))
        if len(cs) != 1 or (cs[0], RDF.type, ODRL.Constraint) not in g:
            e("well-sortedness report: vrep:constraint is not a constraint in the file")
        if len(list(g.objects(rep, VREP.wellSorted))) != 1:
            e("well-sortedness report: no vrep:wellSorted")
        for b in g.objects(rep, VREP.binding):
            if str(b) not in bindings:
                warns.append(f"{path.name}: binding {b} is declared by no profile")

    for rep in g.subjects(RDF.type, VREP.OperandVerdictReport):
        one = lambda p: list(g.objects(rep, p))
        ref, cmp_ = one(VREP.referencePolicy), one(VREP.comparedPolicy)
        if len(ref) != 1 or len(cmp_) != 1 or ref == cmp_:
            e("report must name two distinct policies")
            continue
        if {ref[0], cmp_[0]} != policies:
            e(f"report policies {ref + cmp_} are not the policies in the file")
        for pol, prop in ((ref[0], VREP.referenceConstraint),
                          (cmp_[0], VREP.comparedConstraint)):
            if set(one(prop)) != rules_constraints(g, pol):
                e(f"{prop.fragment} is not the constraint of {pol}")
        b, bt = one(VREP.binding), one(VREP.backgroundTheory)
        if len(b) != 1:
            e("report needs exactly one vrep:binding")
        elif str(b[0]) not in bindings:
            warns.append(f"{path.name}: binding {b[0]} is declared by no profile")
        if len(bt) != 1:
            e("report needs exactly one vrep:backgroundTheory")
        elif str(bt[0]) not in theories:
            warns.append(f"{path.name}: background theory {bt[0]} is declared by no file")
        st = one(VREP.compatibilityState)
        if len(st) != 1 or st[0] not in (VREP.Compatible, VREP.Incompatible, VREP.Unknown):
            e(f"compatibility state {st}")
            continue
        unknown = st[0] == VREP.Unknown
        reason = one(VREP.unknownReason)
        if unknown and (len(reason) != 1 or reason[0] not in (VREP.Epistemic, VREP.Ungrounded)):
            e("Unknown without one vrep:unknownReason")
        if not unknown and reason:
            e("vrep:unknownReason on a definite verdict")
        if bool(one(VREP.ungroundedValue)) != (reason == [VREP.Ungrounded]):
            e("vrep:ungroundedValue present exactly when the reason is Ungrounded")
        cert = one(VREP.certificate)
        if unknown and cert:
            e("certificate on an Unknown verdict")
        if not unknown:
            want = "-1.tstp" if st[0] == VREP.Incompatible else "-2.tstp"
            if len(cert) != 1 or not str(cert[0]).endswith(want):
                e(f"definite verdict needs one certificate ending {want}")
        for t in one(VREP.readAgainst):
            twins[path.stem].add(str(t).rsplit("/", 1)[-1].replace("-report", ""))


def main() -> int:
    # A literal that fails its datatype is a problem for the file's own
    # checker, not for this one; keep rdflib's traceback out of the report.
    logging.getLogger("rdflib").setLevel(logging.CRITICAL)
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="cases", type=Path)
    ap.add_argument("--problems", default="problems", type=Path)
    args = ap.parse_args()

    bind = Namespace("https://w3id.org/odrl-kb/binding#")
    bt = Namespace("https://w3id.org/odrl-kb/background#")
    bindings = declared(sorted((args.problems / "resources").glob("profile-*.ttl")),
                        bind.OperandBinding)
    theories = declared(sorted((args.problems / "background").glob("*.ttl")),
                        bt.BackgroundTheory)

    errs, warns, twins, notes = [], [], defaultdict(set), []
    files = sorted(args.cases.glob("*.ttl"))
    for f in files:
        check(f, bindings, theories, errs, warns, twins, notes)
    names = {f.stem for f in files}
    for a, bs in twins.items():
        for b in bs:
            if b not in names:
                errs.append(f"{a}.ttl: vrep:readAgainst {b}, no such case")
            elif a not in twins.get(b, set()):
                errs.append(f"{a}.ttl: vrep:readAgainst {b}, which does not point back")

    for w in sorted(set(warns)):
        print("warning:", w)
    for n in sorted(set(notes)):
        print("note:   ", n)
    for x in errs:
        print("ERROR:  ", x)
    print(f"\n{len(files)} case files, {len(errs)} errors, "
          f"{len(set(warns))} warnings, "
          f"{len(set(notes))} operator-note conflicts, "
          f"{sum(len(v) for v in twins.values()) // 2} read-against pairs")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
