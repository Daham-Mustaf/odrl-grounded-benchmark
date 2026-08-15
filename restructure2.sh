#!/usr/bin/env bash
# Resumes the restructure from step 4 of restructure.sh.
#
# Target layout:
#
#   generators/          the code that writes everything below
#   problems/            everything a prover reads
#     axioms/            the shared theory
#     resources/         R, one file per resource
#     background/        B, one file per generated rule
#     verdict/           KGC3xx, two queries each
#     wellsorted/        KGC1xx, no queries; the drafting-time check
#     stability/         KGC8xx, paired runs
#   cases/               one .ttl per problem: policies and expected report
#   ontology/            the verdict-report vocabulary
#
# Group directories are named for the result each validates, not for a
# verdict or a theorem number.  Cases sit at the top level because they are
# read by people, not by provers.
#
# Uses plain mv; git detects the renames from content once staged.
# Run from the repository root.

set -eu
cd "$(git rev-parse --show-toplevel)"

echo "== generators =="
if [ -d Generators/KGConstraints ]; then
  mkdir -p generators
  mv Generators/KGConstraints/* generators/ 2>/dev/null || true
  mv Generators/KGConstraints/.[!.]* generators/ 2>/dev/null || true
  rmdir Generators/KGConstraints
  [ -f Generators/header.py ] && mv -f Generators/header.py generators/header.py
  rm -rf Generators/__pycache__ generators/__pycache__
  rmdir Generators 2>/dev/null || true
  echo "  -> generators/"
else
  echo "  already done"
fi

echo "== problems =="
if [ -d Problems/ODRL/KGConstraints ]; then
  mkdir -p problems
  mv Problems/ODRL/KGConstraints/* problems/ 2>/dev/null || true
  rmdir Problems/ODRL/KGConstraints Problems/ODRL Problems 2>/dev/null || true
  echo "  -> problems/"
else
  echo "  already done"
fi

echo "== group directories =="
cd problems
# Kept, renamed for what they hold.
for pair in "Axioms:axioms" "Resources:resources" "Verdict:verdict"; do
  from="${pair%%:*}"; to="${pair##*:}"
  [ -d "$from" ] || continue
  mv "$from" "${from}__tmp" && mv "${from}__tmp" "$to"
  echo "  $from -> $to"
done
# The old single-query groups.  Superseded; the two-query problems replace
# them and the results two of them validated are no longer in the paper.
for d in Conflict Composition Monotonicity Runtime; do
  [ -d "$d" ] && { rm -rf "$d"; echo "  $d removed (superseded)"; }
done
# Policies and Reports become cases/, at the top level.
rm -rf Policies Reports
mkdir -p background wellsorted stability
cd ..
mkdir -p cases ontology

echo "== duplicated axiom copies =="
# Twelve .ax files were copied into every problem directory; TPTP include
# resolves against problems/axioms, so the copies only drift.
find problems -mindepth 2 -type d \( -name axioms -o -name Axioms \) \
  -exec rm -rf {} + 2>/dev/null || true

echo "== background theory out of resources =="
for f in problems/resources/*uniqueness*.ttl problems/resources/*-bt.ttl; do
  [ -f "$f" ] && { mv "$f" problems/background/; echo "  $(basename "$f")"; }
done

echo "== stale axiom files =="
# Results these supported are no longer in the paper.
for f in REFINE000-0.ax ALIGN000-0.ax RUNTIME000-0.ax MONO000-0.ax \
         COMPOSE000-0.ax COMPOSE001-0.ax; do
  [ -f "problems/axioms/$f" ] && { rm -f "problems/axioms/$f"; echo "  $f"; }
done

echo "== stage =="
git add -A
echo
git status --short | head -40
echo
git diff --cached --stat -M | tail -3