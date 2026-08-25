"""
certify_patch.py
================
The replacement for the certificate-writing block of run_certify.py.

Apply by hand: the three sections below replace the `to_turtle` call in the
refutation branch, add a certificate to the Unknown branch, and add the
report write that both branches share.

Three things this fixes, beyond the naming
-------------------------------------------
The artefact path was wrong.  The proof was written to
`certificates/KGC330-2.tstp` and the certificate pointed at
`proofs/KGC330-2.tstp`, a directory that does not exist.  The link has been
dead in every certificate written so far.

An Unknown verdict produced no artefact at all.  The console printed the
concepts the two models differ on and nothing was written, so the only
Unknown evidence in the repository is a line of terminal output.  Definition
Certificate says an Unknown verdict is certified by a model of each query,
and the models are already computed; they were being discarded.

And no report existed.  The verdict lived in the console and in the expected
values of problem_data_*.py, so a reader of the artefact could see the
premises of a refutation without being able to see what it concluded.

On the statuses
---------------
The prover statuses are normalised to sat/unsat before verdict_of sees them,
so the report can record them directly.  Where per-prover statuses are
available separately, pass both; where the pipeline has already reconciled
them into s1 and s2, pass those under a single key and let proversAgree be
true, which is what the reconciliation established.
"""

# ---------------------------------------------------------------------------
# 1.  At the top of run_certify.py, beside the other imports.
# ---------------------------------------------------------------------------

IMPORTS = '''
from report_writer import write_report, write_certificate
'''

# ---------------------------------------------------------------------------
# 2.  Before the problem loop, beside the certificates directory.
#     `odir` is the certificates directory; the reports go beside it.
# ---------------------------------------------------------------------------

SETUP = '''
    rdir = odir.parent / "reports"
    rdir.mkdir(parents=True, exist_ok=True)
'''

# ---------------------------------------------------------------------------
# 3.  Replace the Unknown branch's `continue` block.
#
#     Currently the models are computed, printed and dropped.  The verdict has
#     an artefact now: the two models, and the concepts they disagree about.
#     That disagreement is the question the vocabulary leaves open, and it is
#     what a party would have to declare to get a definite verdict.
# ---------------------------------------------------------------------------

UNKNOWN_BRANCH = '''
            # Unknown.  Both queries have models; report what they differ on.
            diff = []
            if use_z and zout1 and zout2:
                syms = constants_of(q1path.with_suffix(".smt2"))
                m1 = model_literals(zout1, syms)
                m2 = model_literals(zout2, syms)
                diff = compare_models(m1, m2)
                (odir / f"{pid}-1.model").write_text(zout1, encoding="utf-8")
                (odir / f"{pid}-2.model").write_text(zout2, encoding="utf-8")
                if diff:
                    print(f"    two models, differing on: {', '.join(diff)}")
                    print(f"    that difference is the question the resource "
                          f"leaves open")
                else:
                    print("    two models; they agree on the constants, so "
                          "the difference lies in the order relation")
            else:
                print("    Unknown: two models; no refutation to attribute.")

            write_report(pid, "Unknown", {prover_key: (s1, s2)},
                         problem, rdir / f"{pid}-report.ttl")
            if use_z and zout1 and zout2:
                write_certificate(
                    pid, "Unknown", "Models",
                    odir / f"{pid}-certificate.ttl",
                    prover="Z3",
                    models=(f"{pid}-1.model", f"{pid}-2.model"),
                    differing=diff,
                    comment=("Both queries are satisfiable.  The models differ "
                             "on the concepts listed, which is what neither "
                             "the resource nor the background theory settles."
                             if diff else
                             "Both queries are satisfiable.  The models agree "
                             "on the constants, so the difference lies in the "
                             "order relation."))
                print(f"    -> {rdir / f'{pid}-report.ttl'}")
                print(f"    -> {odir / f'{pid}-certificate.ttl'}")
            continue
'''

# ---------------------------------------------------------------------------
# 4.  Replace the `to_turtle` block in the refutation branch.
#
#     `classified` maps a provenance to the formula names under it, and
#     `withdrawable` returns the names a party may retract.  Both are already
#     computed above; this turns them into the two artefacts.
#
#     The label is the formula name for now.  A human-readable gloss would be
#     better and belongs with the problem data, where the English description
#     of each premise already lives.
# ---------------------------------------------------------------------------

REFUTATION_BRANCH = '''
        if classified_v is not None:
            for source, ns in classified_v.items():
                if ns and source != "unclassified":
                    print(f"    {source:24s} {', '.join(ns)}")
            if classified_v["unclassified"]:
                print(f"    UNCLASSIFIED             "
                      f"{', '.join(classified_v['unclassified'])}")
            w = withdrawable(classified_v)
            print(f"    withdrawable             "
                  f"{', '.join(w) if w else 'none'}")

            premises = [(source, name, name)
                        for source, ns in classified_v.items()
                        if source != "unclassified"
                        for name in ns]

            write_report(pid, verdict, {prover_key: (s1, s2)},
                         problem, rdir / f"{pid}-report.ttl")
            write_certificate(
                pid, verdict, "Refutation",
                odir / f"{pid}-certificate.ttl",
                prover="Vampire",
                premises=premises,
                withdrawable=set(w),
                artefact=f"{pid}-{which}.tstp",
                comment=problem.get("certificate", {}).get("comment"))
            print(f"    -> {rdir / f'{pid}-report.ttl'}")
            print(f"    -> {odir / f'{pid}-certificate.ttl'}")
'''

# ---------------------------------------------------------------------------
# What you must supply
# ---------------------------------------------------------------------------
#
# `problem`   the dict from problem_data_*.py for this pid, for the operand,
#             the sort, the resource and the background theory.  If the loop
#             does not already carry it, pass {} and the report omits those
#             fields rather than guessing them.
#
# `verdict`   verdict_of(s1, s2), which the loop computes above.
#
# `prover_key`  where the pipeline has reconciled the two provers into s1 and
#             s2, use "Vampire+Z3" or similar and proversAgree is true, which
#             is what the reconciliation established.  Where the per-prover
#             statuses are still separate, pass both entries instead and let
#             the writer compare them.
#
# The old `-observed.ttl` files can stay until the new ones are checked, then
# go in one commit:  git rm certificates/*-observed.ttl