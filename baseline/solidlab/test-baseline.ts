/**
 * test-baseline.ts
 * ================
 * The knowledge-grounded problems of the benchmark, run against the SolidLab
 * ODRL Evaluator, for the operand and operators it supports.
 *
 * Scope is set by the evaluator, not by us.  Its support table marks
 * odrl:purpose as the only externally-grounded left operand implemented;
 * spatial, fileFormat, language, recipient, industry and media are not.  Of
 * the eight operators of the fragment it implements eq, neq, isA, isAnyOf and
 * isNoneOf, and not isPartOf, hasPart or isAllOf.  So the comparison is one
 * operand and five operators, and no problem at the mereological sort can be
 * run at all.
 *
 * Every case below uses the same offer/request shape and differs only in the
 * operator and in what the state of the world says about the requested
 * purpose.  The vocabulary is DPV, and the edge that matters is the one DPV
 * actually publishes:
 *
 *     dpv:ScientificResearch skos:broader dpv:ResearchAndDevelopment
 *
 * Neither this nor the rdfs:subClassOf form of the same edge is read by any
 * rule in the evaluator's rule set.  The cases show what follows.
 *
 * Two kinds of divergence appear, and they are not the same kind.
 *
 *   Restrictive.  isA over the published order returns Unsatisfied where the
 *   vocabulary places the requested purpose below the offered one.  A use the
 *   parties would agree on is refused.
 *
 *   Permissive.  isNoneOf over the published order returns Satisfied where
 *   the requested purpose lies below an excluded one.  A use the offer
 *   excludes is allowed.  This is the more serious of the two, and it is the
 *   direction a policy author is least likely to test for.
 *
 * Neither is a defect in the implementation.  ODRL fixes no semantics for
 * these operators, so reading isA as one rdf:type hop is as conformant as
 * reading it as the order a profile declares.  That is the point the
 * comparison is here to make, and the paper should state it that way rather
 * than as a scoreboard.
 */

import { ODRLEngineMultipleSteps, ODRLEvaluator, prefixes, turtleStringToStore } from "../dist/index";
import { write } from '@jeswr/pretty-turtle';

const PREFIXES = `
@prefix odrl: <http://www.w3.org/ns/odrl/2/>.
@prefix ex: <http://example.org/>.
@prefix dpv: <https://w3id.org/dpv#>.
@prefix temp: <http://example.com/request/>.
@prefix sotw: <https://w3id.org/force/sotw#>.
@prefix dct: <http://purl.org/dc/terms/>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix skos: <http://www.w3.org/2004/02/skos/core#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
`;

/** An offer whose single constraint is the one under test. */
function policy(operator: string, rightOperands: string[], description: string) {
    const values = rightOperands.map(v => `odrl:rightOperand ${v}`).join(" ;\n    ");
    return PREFIXES + `
<urn:uuid:policy> a odrl:Set ;
    dct:description "${description}" ;
    odrl:permission <urn:uuid:permission> .

<urn:uuid:permission> a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target ex:manuscripts ;
    odrl:assignee ex:bnf ;
    odrl:assigner ex:bsb ;
    odrl:constraint <urn:uuid:constraint> .

<urn:uuid:constraint> a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator ${operator} ;
    ${values} .
`;
}

/** A request that names the purpose of the intended use. */
const request = PREFIXES + `
<urn:uuid:request> a odrl:Request ;
    dct:description "BnF requests use; the purpose of the use is ex:project." ;
    odrl:permission <urn:uuid:request-permission> .

<urn:uuid:request-permission> a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target ex:manuscripts ;
    odrl:assignee ex:bnf ;
    sotw:context <urn:uuid:request-context> .

<urn:uuid:request-context> a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ex:project .
`;

const SOTW = PREFIXES + `
<urn:uuid:sotw> a ex:Sotw ;
    ex:includes temp:currentTime, ex:bsb, ex:bnf .

temp:currentTime dct:issued "2026-08-19T09:00:00.000Z"^^xsd:dateTime .
ex:bsb a foaf:Organization .
ex:bnf a foaf:Organization .
`;

/** ex:project is typed directly with the concept the offer names. */
const DIRECT = (concept: string) => SOTW + `
ex:project a ${concept} .
`;

/** ex:project is typed below the offered concept, as DPV publishes it. */
const BELOW_SKOS = SOTW + `
ex:project a dpv:ScientificResearch .
dpv:ScientificResearch skos:broader dpv:ResearchAndDevelopment .
`;

/** The same, in the OWL serialisation DPV also publishes. */
const BELOW_OWL = SOTW + `
ex:project a dpv:ScientificResearch .
dpv:ScientificResearch rdfs:subClassOf dpv:ResearchAndDevelopment .
`;

interface Case {
    id: string;
    what: string;
    ours: string;
    expectTheirs: string;
    note: string;
    policy: string;
    sotw: string;
}

const cases: Case[] = [

    // ---------------------------------------------------------------- isA
    {
        id: "B00",
        what: "isA R&D, purpose typed R&D directly",
        ours: "Compatible",
        expectTheirs: "Satisfied",
        note: "Control.  One rdf:type hop and the rule matches.  If this " +
              "fails the input is malformed and nothing below means anything.",
        policy: policy("odrl:isA", ["dpv:ResearchAndDevelopment"],
                       "Use is permitted for research and development purposes."),
        sotw: DIRECT("dpv:ResearchAndDevelopment"),
    },
    {
        id: "B01",
        what: "isA R&D, purpose typed SR, DPV skos:broader",
        ours: "Compatible",
        expectTheirs: "Unsatisfied",
        note: "KGC310.  DPV places scientific research below research and " +
              "development.  The rule reads rdf:type and stops, so a use the " +
              "vocabulary supports is refused.  Restrictive divergence.",
        policy: policy("odrl:isA", ["dpv:ResearchAndDevelopment"],
                       "Use is permitted for research and development purposes."),
        sotw: BELOW_SKOS,
    },
    {
        id: "B02",
        what: "isA R&D, purpose typed SR, DPV rdfs:subClassOf",
        ours: "Compatible",
        expectTheirs: "Unsatisfied",
        note: "The same pair in the OWL serialisation DPV also publishes.  " +
              "Neither form of the edge is read, so this is not a matter of " +
              "having chosen the wrong file.",
        policy: policy("odrl:isA", ["dpv:ResearchAndDevelopment"],
                       "Use is permitted for research and development purposes."),
        sotw: BELOW_OWL,
    },

    // ----------------------------------------------------------- isNoneOf
    {
        id: "B10",
        what: "isNoneOf {SR}, purpose typed SR directly",
        ours: "Incompatible",
        expectTheirs: "Unsatisfied",
        note: "Control for the exclusion.  The excluded purpose is exactly " +
              "the requested one, so both refuse it.",
        policy: policy("odrl:isNoneOf", ["dpv:ScientificResearch"],
                       "Use is permitted for any purpose other than scientific research."),
        sotw: DIRECT("dpv:ScientificResearch"),
    },
    {
        id: "B11",
        what: "isNoneOf {R&D}, purpose typed SR, DPV skos:broader",
        ours: "Unknown",
        expectTheirs: "Satisfied",
        note: "The offer excludes research and development.  The requested " +
              "purpose lies below it in DPV, and the rule compares named " +
              "values only, so the exclusion is escaped and the use is " +
              "allowed.  Permissive divergence, and the direction an author " +
              "is least likely to test.  Our verdict is Unknown rather than " +
              "Incompatible because isNoneOf at tax excludes the concept and " +
              "not its subtypes: the offer as written does not exclude this " +
              "use either, and saying so is the point.",
        policy: policy("odrl:isNoneOf", ["dpv:ResearchAndDevelopment"],
                       "Use is permitted for any purpose other than research and development."),
        sotw: BELOW_SKOS,
    },

    // ---------------------------------------------------------------- eq
    {
        id: "B20",
        what: "eq R&D, purpose typed SR, DPV skos:broader",
        ours: "Unknown",
        expectTheirs: "Unsatisfied",
        note: "Identity rather than order.  Nothing in DPV says the two " +
              "purposes are distinct, so a structure may identify them and " +
              "the verdict is open.  A two-valued report has no way to say " +
              "that and returns a definite refusal.",
        policy: policy("odrl:eq", ["dpv:ResearchAndDevelopment"],
                       "Use is permitted for research and development purposes."),
        sotw: BELOW_SKOS,
    },

    // ------------------------------------------------------------ isAnyOf
    {
        id: "B30",
        what: "isAnyOf {R&D, SR}, purpose typed SR directly",
        ours: "Compatible",
        expectTheirs: "Satisfied",
        note: "A genuine set-valued right operand.  Worth running because " +
              "the rule matches one right operand at a time; this checks " +
              "that a two-member set behaves as the operator's definition " +
              "requires.",
        policy: policy("odrl:isAnyOf",
                       ["dpv:ResearchAndDevelopment", "dpv:ScientificResearch"],
                       "Use is permitted for research and development or scientific research."),
        sotw: DIRECT("dpv:ScientificResearch"),
    },
];

/** The satisfaction state of the constraint report, and the rule's activation. */
function readReport(text: string) {
    const constraint = text.match(/cr:constraint <urn:uuid:constraint>[\s\S]*?cr:satisfactionState (cr:\w+)/)
        ?? text.match(/cr:satisfactionState (cr:\w+)[\s\S]*?cr:constraint <urn:uuid:constraint>/);
    const activation = text.match(/cr:activationState (cr:\w+)/);
    return {
        constraint: constraint ? constraint[1].replace("cr:", "") : "none",
        rule: activation ? activation[1].replace("cr:", "") : "none",
    };
}

async function main() {
    const requestStore = await turtleStringToStore(request);
    const rows: string[] = [];

    for (const c of cases) {
        const policyStore = await turtleStringToStore(c.policy);
        const sotwStore = await turtleStringToStore(c.sotw);

        const evaluator = new ODRLEvaluator(new ODRLEngineMultipleSteps());
        const report = await evaluator.evaluate(
            policyStore.getQuads(null, null, null, null),
            requestStore.getQuads(null, null, null, null),
            sotwStore.getQuads(null, null, null, null));

        const text = await write(report, { prefixes });
        const { constraint, rule } = readReport(text);
        const asExpected = constraint === c.expectTheirs ? "" : "   <-- NOT AS EXPECTED";

        console.log("=".repeat(72));
        console.log(`${c.id}  ${c.what}`);
        console.log(`  ours        : ${c.ours}`);
        console.log(`  theirs      : ${constraint} (rule ${rule})${asExpected}`);
        console.log(`  expected    : ${c.expectTheirs}`);
        console.log(`  ${c.note}`);
        console.log();
        console.log(text);
        console.log();

        rows.push(`${c.id.padEnd(5)} ${c.what.padEnd(52)} ` +
                  `${c.ours.padEnd(13)} ${constraint}${asExpected}`);
    }

    console.log("=".repeat(72));
    console.log("SUMMARY");
    console.log("=".repeat(72));
    console.log(`${"id".padEnd(5)} ${"case".padEnd(52)} ${"ours".padEnd(13)} theirs`);
    rows.forEach(r => console.log(r));
}

main();