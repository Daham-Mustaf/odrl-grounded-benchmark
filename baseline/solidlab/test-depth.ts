/**
 * test-depth.ts
 * =============
 * Does the divergence on isA depend on how far apart the two purposes are?
 *
 * The evaluator's rule for isA is one dereference and a term comparison:
 *
 *     ?leftOperand a ?instance .
 *     ?instance log:equalTo ?rightOperand .
 *
 * It reads the requested purpose's type and compares it with the offered
 * concept.  There is no recursion and no traversal, so on the face of it the
 * answer should be the same at one hop and at six.  This script measures
 * that rather than assuming it, since the claim in the paper is that the
 * divergence is structural and not a matter of degree.
 *
 * Four offers, one request shape, DPV's own edges in the state of the world.
 * The chain is the one the purposes module actually publishes, measured from
 * the file:
 *
 *     RecruitmentInterviewScheduling
 *       < RecruitmentInterviewManagement
 *       < RecruitmentManagement
 *       < PersonnelHiring
 *       < PersonnelManagement
 *       < HumanResourceManagement
 *       < Purpose
 *
 * six edges, each with a single parent, and the longest chain in the module.
 *
 * The corresponding verdicts on our side are KGC310 at one hop, KGC311 at
 * two, and KGC315 at six.  All three are Compatible, and what grows with the
 * distance is the certificate: KGC310 cites one resource assertion, KGC311
 * two and an instance of transitivity, KGC315 six and transitivity.  If the
 * evaluator refuses all of them alike, the two accounts differ in kind and
 * not in reach, and the certificates are the only thing that varies with
 * depth.
 *
 * The convention here is `individual`: the request names ex:project and the
 * state of the world types it.  That is the convention isA requires, as
 * test-conventions.ts establishes, so this comparison is on the evaluator's
 * own terms.
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
`;

function policy(offered: string) {
    return PREFIXES + `
<urn:uuid:policy> a odrl:Set ;
    odrl:permission <urn:uuid:permission> .

<urn:uuid:permission> a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target ex:manuscripts ;
    odrl:assignee ex:bnf ;
    odrl:assigner ex:bsb ;
    odrl:constraint <urn:uuid:constraint> .

<urn:uuid:constraint> a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand ${offered} .
`;
}

const request = PREFIXES + `
<urn:uuid:request> a odrl:Request ;
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

const SOTW_BASE = PREFIXES + `
<urn:uuid:sotw> a ex:Sotw ;
    ex:includes temp:currentTime, ex:bsb, ex:bnf .

temp:currentTime dct:issued "2026-08-19T09:00:00.000Z"^^xsd:dateTime .
ex:bsb a foaf:Organization .
ex:bnf a foaf:Organization .
`;

/** The edges DPV publishes, as skos:broader, measured from purposes.ttl. */
const DPV_EDGES = `
dpv:ScientificResearch skos:broader dpv:ResearchAndDevelopment .
dpv:ResearchAndDevelopment skos:broader dpv:Purpose .
dpv:NonCommercialResearch skos:broader dpv:NonCommercialPurpose .
dpv:NonCommercialPurpose skos:broader dpv:Purpose .
dpv:RecruitmentInterviewScheduling skos:broader dpv:RecruitmentInterviewManagement .
dpv:RecruitmentInterviewManagement skos:broader dpv:RecruitmentManagement .
dpv:RecruitmentManagement skos:broader dpv:PersonnelHiring .
dpv:PersonnelHiring skos:broader dpv:PersonnelManagement .
dpv:PersonnelManagement skos:broader dpv:HumanResourceManagement .
dpv:HumanResourceManagement skos:broader dpv:Purpose .
`;

const cases = [
    {
        id: "D0",
        hops: 0,
        ours: "Compatible, no resource premise needed",
        offered: "dpv:ScientificResearch",
        requested: "dpv:ScientificResearch",
        note: "Control.  The offered and requested purposes are the same, so " +
              "the type matches directly and no traversal is called for.",
    },
    {
        id: "D1",
        hops: 1,
        ours: "Compatible, one resource premise (KGC310)",
        offered: "dpv:ResearchAndDevelopment",
        requested: "dpv:ScientificResearch",
        note: "One edge.  DPV places scientific research directly below " +
              "research and development.",
    },
    {
        id: "D2",
        hops: 2,
        ours: "Compatible, two premises and transitivity (KGC311)",
        offered: "dpv:Purpose",
        requested: "dpv:NonCommercialResearch",
        note: "Two edges, through non-commercial purpose.  The first case " +
              "whose refutation on our side needs the transitivity axiom.",
    },
    {
        id: "D6",
        hops: 6,
        ours: "Compatible, six premises and transitivity (KGC315)",
        offered: "dpv:Purpose",
        requested: "dpv:RecruitmentInterviewScheduling",
        note: "The longest chain in the purposes module.  If the answer here " +
              "is the same as at one hop, the divergence does not depend on " +
              "distance.",
    },
];

function readState(text: string) {
    const m = text.match(/cr:constraint <urn:uuid:constraint>[\s\S]*?cr:satisfactionState (cr:\w+)/)
        ?? text.match(/cr:satisfactionState (cr:\w+)[\s\S]*?cr:constraint <urn:uuid:constraint>/);
    return m ? m[1].replace("cr:", "") : "none";
}

async function main() {
    const requestStore = await turtleStringToStore(request);
    const rows: string[] = [];

    for (const c of cases) {
        const sotw = SOTW_BASE + `
ex:project a ${c.requested} .
` + DPV_EDGES;

        const policyStore = await turtleStringToStore(policy(c.offered));
        const sotwStore = await turtleStringToStore(sotw);

        const evaluator = new ODRLEvaluator(new ODRLEngineMultipleSteps());
        const report = await evaluator.evaluate(
            policyStore.getQuads(null, null, null, null),
            requestStore.getQuads(null, null, null, null),
            sotwStore.getQuads(null, null, null, null));

        const state = readState(await write(report, { prefixes }));

        const offered = c.offered.replace("dpv:", "");
        const requested = c.requested.replace("dpv:", "");
        rows.push(
            `${c.id.padEnd(4)} ${String(c.hops).padEnd(5)} ` +
            `${(`isA ${offered} / ${requested}`).padEnd(52)} ${state}`);

        console.log("=".repeat(78));
        console.log(`${c.id}  ${c.hops} hop(s):  isA ${offered}  against  ${requested}`);
        console.log(`  ours   : ${c.ours}`);
        console.log(`  theirs : ${state}`);
        console.log(`  ${c.note}`);
    }

    console.log();
    console.log("=".repeat(78));
    console.log(`${"id".padEnd(4)} ${"hops".padEnd(5)} ${"constraint / requested purpose".padEnd(52)} theirs`);
    console.log("-".repeat(78));
    rows.forEach(r => console.log(r));
    console.log();
    console.log("All four states of the world contain the same DPV edges.  The");
    console.log("only difference between the rows is how far apart the two");
    console.log("purposes are in the vocabulary.");
}

main();