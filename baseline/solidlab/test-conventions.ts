/**
 * test-conventions.ts
 * ===================
 * How the request must name a purpose, for the SolidLab ODRL Evaluator.
 *
 * The evaluator binds the constraint's left operand from the request:
 *
 *     ?requestContextConstraint odrl:rightOperand ?requestedPurpose .
 *     ?premiseReport report:constraintLeftOperand ?requestedPurpose .
 *
 * Nothing says what kind of term ?requestedPurpose should be, and the
 * operator rules do not agree about it.
 *
 *     isA        ?leftOperand a ?instance . ?instance log:equalTo ?rightOperand .
 *     isNoneOf   ?leftOperand log:equalTo ?rightOperand .  (collected, must be empty)
 *     isAnyOf    ?leftOperand log:equalTo ?rightOperand .
 *     eq         ?leftOperand log:equalTo ?rightOperand .
 *
 * isA dereferences the value's type, so it needs an individual with a type.
 * The other three compare the value with the right operand as terms, so they
 * need the value to be the concept itself.  A request supplies one value, and
 * these are two different values.
 *
 * This script runs the same four constraints under both conventions.
 *
 *   individual   request names ex:project, sotw types it
 *   concept      request names the DPV concept, no typing needed
 *
 * If each operator works under exactly one convention and fails under the
 * other, then no single request satisfies a policy that uses operators from
 * both families.  That is not a defect in the implementation: ODRL fixes no
 * semantics for these operators, and each rule is a reasonable reading taken
 * on its own.  It is what happens when the reading is left to the
 * implementation and the operators are read one at a time.
 *
 * Run this before drawing any conclusion from the earlier baseline suite,
 * which used the individual convention throughout and may therefore have
 * been testing the set operators under the wrong one.
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

function policy(operator: string, rightOperands: string[]) {
    const values = rightOperands.map(v => `odrl:rightOperand ${v}`).join(" ;\n    ");
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
    odrl:operator ${operator} ;
    ${values} .
`;
}

function request(purposeValue: string) {
    return PREFIXES + `
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
    odrl:rightOperand ${purposeValue} .
`;
}

const SOTW_BASE = PREFIXES + `
<urn:uuid:sotw> a ex:Sotw ;
    ex:includes temp:currentTime, ex:bsb, ex:bnf .

temp:currentTime dct:issued "2026-08-19T09:00:00.000Z"^^xsd:dateTime .
ex:bsb a foaf:Organization .
ex:bnf a foaf:Organization .
`;

/** The requested purpose is an individual, typed as scientific research. */
const CONV_INDIVIDUAL = {
    name: "individual",
    request: request("ex:project"),
    sotw: SOTW_BASE + `
ex:project a dpv:ScientificResearch .
`,
};

/** The requested purpose is the concept itself. */
const CONV_CONCEPT = {
    name: "concept",
    request: request("dpv:ScientificResearch"),
    sotw: SOTW_BASE,
};

/**
 * Four constraints.  In every one the requested purpose is scientific
 * research, so the intended answer does not depend on the convention: it is
 * fixed by what the offer says about scientific research.
 */
const constraints = [
    {
        id: "isA-hit",
        what: "isA ScientificResearch",
        intended: "Satisfied",
        why: "the offer names the requested purpose",
        policy: policy("odrl:isA", ["dpv:ScientificResearch"]),
    },
    {
        id: "eq-hit",
        what: "eq ScientificResearch",
        intended: "Satisfied",
        why: "the offer names the requested purpose",
        policy: policy("odrl:eq", ["dpv:ScientificResearch"]),
    },
    {
        id: "isAnyOf-hit",
        what: "isAnyOf {Marketing, ScientificResearch}",
        intended: "Satisfied",
        why: "the requested purpose is among those the offer admits",
        policy: policy("odrl:isAnyOf", ["dpv:Marketing", "dpv:ScientificResearch"]),
    },
    {
        id: "isNoneOf-hit",
        what: "isNoneOf {ScientificResearch}",
        intended: "Unsatisfied",
        why: "the offer excludes exactly the requested purpose",
        policy: policy("odrl:isNoneOf", ["dpv:ScientificResearch"]),
    },
];

function readState(text: string) {
    const m = text.match(/cr:constraint <urn:uuid:constraint>[\s\S]*?cr:satisfactionState (cr:\w+)/)
        ?? text.match(/cr:satisfactionState (cr:\w+)[\s\S]*?cr:constraint <urn:uuid:constraint>/);
    const fired = /cr:constraintOperator/.test(text);
    return {
        state: m ? m[1].replace("cr:", "") : "none",
        fired,
    };
}

async function main() {
    const results: Record<string, Record<string, string>> = {};

    for (const conv of [CONV_INDIVIDUAL, CONV_CONCEPT]) {
        const requestStore = await turtleStringToStore(conv.request);
        const sotwStore = await turtleStringToStore(conv.sotw);

        for (const c of constraints) {
            const policyStore = await turtleStringToStore(c.policy);
            const evaluator = new ODRLEvaluator(new ODRLEngineMultipleSteps());
            const report = await evaluator.evaluate(
                policyStore.getQuads(null, null, null, null),
                requestStore.getQuads(null, null, null, null),
                sotwStore.getQuads(null, null, null, null));

            const text = await write(report, { prefixes });
            const { state, fired } = readState(text);

            results[c.id] ??= {};
            results[c.id][conv.name] = fired ? state : `${state} (rule did not fire)`;
        }
    }

    console.log("=".repeat(78));
    console.log("The requested purpose is scientific research in every case.");
    console.log("The intended answer is therefore fixed by the offer, and does");
    console.log("not depend on how the request names the purpose.");
    console.log("=".repeat(78));
    console.log();
    console.log(`${"constraint".padEnd(38)} ${"intended".padEnd(13)} ` +
                `${"individual".padEnd(26)} concept`);
    console.log("-".repeat(78));
    for (const c of constraints) {
        console.log(`${c.what.padEnd(38)} ${c.intended.padEnd(13)} ` +
                    `${(results[c.id]["individual"] ?? "?").padEnd(26)} ` +
                    `${results[c.id]["concept"] ?? "?"}`);
    }
    console.log();
    console.log("If each operator matches its intended answer under one");
    console.log("convention and not the other, then a policy using operators");
    console.log("from both families cannot be satisfied by any single request.");
}

main();