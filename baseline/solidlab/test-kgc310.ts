/**
 * test-kgc310.ts
 * ==============
 * KGC310 against the SolidLab ODRL Evaluator.
 *
 * The offer permits use for research and development purposes.  The request
 * declares a purpose, and the state of the world says what that purpose is.
 * Three runs differ only in how the state of the world relates the requested
 * purpose to the one the offer names.
 *
 *   A  direct type          ex:project a dpv:ResearchAndDevelopment
 *   B  DPV as published     ex:project a dpv:ScientificResearch,
 *                           dpv:ScientificResearch skos:broader dpv:ResearchAndDevelopment
 *   C  DPV in OWL form      as B, with rdfs:subClassOf instead of skos:broader
 *
 * A is the control: it should be Satisfied, and if it is not the input is
 * malformed rather than the evaluator narrow.  B is the case that matters:
 * DPV publishes exactly this edge, and the offer asks about exactly this
 * pair.  C checks whether the OWL reading fares differently.
 *
 * The rule under test is in src/rules/constraints.n3:
 *
 *     ?leftOperand a ?instance .
 *     ?instance log:equalTo ?rightOperand .
 *
 * One rdf:type hop, then term identity.  Nothing in the rule set mentions
 * skos:broader or rdfs:subClassOf, so B and C are expected to differ from A.
 * Running it is worth more than reading it: the claim in the paper is about
 * behaviour, not about source.
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

// The offer.  Use is permitted for research and development purposes.
const policy = PREFIXES + `
<urn:uuid:kgc310-policy> a odrl:Set ;
    dct:description "BSB permits use of the manuscripts for research and development purposes." ;
    odrl:permission <urn:uuid:kgc310-permission> .

<urn:uuid:kgc310-permission> a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target ex:manuscripts ;
    odrl:assignee ex:bnf ;
    odrl:assigner ex:bsb ;
    odrl:constraint <urn:uuid:kgc310-constraint> .

<urn:uuid:kgc310-constraint> a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:ResearchAndDevelopment .
`;

// The request.  The purpose of the intended use is ex:project.
const request = PREFIXES + `
<urn:uuid:kgc310-request> a odrl:Request ;
    dct:description "BnF requests use of the manuscripts; the purpose is ex:project." ;
    odrl:permission <urn:uuid:kgc310-request-permission> .

<urn:uuid:kgc310-request-permission> a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target ex:manuscripts ;
    odrl:assignee ex:bnf ;
    sotw:context <urn:uuid:kgc310-request-context> .

<urn:uuid:kgc310-request-context> a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ex:project .
`;

const SOTW_HEAD = PREFIXES + `
<urn:uuid:kgc310-sotw> a ex:Sotw ;
    ex:includes temp:currentTime, ex:bsb, ex:bnf .

temp:currentTime dct:issued "2026-08-19T09:00:00.000Z"^^xsd:dateTime .
ex:bsb a foaf:Organization .
ex:bnf a foaf:Organization .
`;

const runs = [
    {
        name: "A  direct type (control)",
        expect: "Satisfied",
        why: "The purpose is typed with the concept the offer names.  One " +
             "rdf:type hop and the rule matches.",
        sotw: SOTW_HEAD + `
ex:project a dpv:ResearchAndDevelopment .
`,
    },
    {
        name: "B  DPV as published (skos:broader)",
        expect: "not Satisfied",
        why: "The purpose is typed with scientific research, and DPV places " +
             "scientific research below research and development.  The rule " +
             "reads rdf:type and stops.",
        sotw: SOTW_HEAD + `
ex:project a dpv:ScientificResearch .
dpv:ScientificResearch skos:broader dpv:ResearchAndDevelopment .
`,
    },
    {
        name: "C  DPV in OWL form (rdfs:subClassOf)",
        expect: "not Satisfied",
        why: "The same pair under the serialisation DPV also publishes, where " +
             "the edge is rdfs:subClassOf.  No rule reads that either.",
        sotw: SOTW_HEAD + `
ex:project a dpv:ScientificResearch .
dpv:ScientificResearch rdfs:subClassOf dpv:ResearchAndDevelopment .
`,
    },
];

async function main() {
    const policyStore = await turtleStringToStore(policy);
    const requestStore = await turtleStringToStore(request);

    for (const run of runs) {
        const sotwStore = await turtleStringToStore(run.sotw);
        const evaluator = new ODRLEvaluator(new ODRLEngineMultipleSteps());
        const report = await evaluator.evaluate(
            policyStore.getQuads(null, null, null, null),
            requestStore.getQuads(null, null, null, null),
            sotwStore.getQuads(null, null, null, null));

        const text = await write(report, { prefixes });
        const m = text.match(/cr:constraint <urn:uuid:kgc310-constraint>[^.]*?cr:satisfactionState (cr:\w+)/s)||text.match(/cr:satisfactionState (cr:\w+)[^.]*?cr:constraintOperator/s);
        const satisfied = m ? m[1] : "none";
        const active = /cr:activationState cr:Active\b/.test(text) ? "Active" : (/cr:activationState cr:Inactive/.test(text) ? "Inactive" : "none");

        console.log("=".repeat(70));
        console.log(run.name);
        console.log("  expected      :", run.expect);
        console.log("  constraint    :", satisfied);
        console.log("  rule          :", active);
        console.log("  ", run.why);
        console.log();
        console.log(text);
        console.log();
    }
}

main();