#!/usr/bin/env bash
# Scratch from a day's exploration, and the unwired architecture modules.
# Run from the repository root, read before running.
set -eu

# Root-level scratch files: intermediate output from the registry and
# hierarchy exploration, none of them inputs to anything.
git rm --cached -q europe-ids.txt hierarchy.txt hierarchy.zip macro.txt \
                   parents.txt preferred.txt 2>/dev/null || true
rm -f europe-ids.txt hierarchy.txt hierarchy.zip macro.txt \
      parents.txt preferred.txt

# The registry belongs with the other vendored vocabularies, not in a
# directory of its own at the root.
if [ -f ontology/language-subtag-registry.txt ]; then
  mkdir -p vocabularies/bcp47-20260826
  mv ontology/language-subtag-registry.txt vocabularies/bcp47-20260826/
  rmdir ontology 2>/dev/null || true
fi

# The schemas are ours; vocabularies/ holds what authorities published.
mkdir -p vocab
for f in background.ttl binding.ttl verdict-report.ttl; do
  [ -f "vocabularies/$f" ] && git mv "vocabularies/$f" "vocab/$f"
done

# Empty directories from vocabulary candidates that were never built.
rmdir vocabularies/cpv-2008 vocabularies/nace-2.1 2>/dev/null || true

# The stale axiom file from the first BCP 47 run.
rm -f problems/axioms/BCP47-uniqueness.ax

# The nine architecture modules are not wired into anything yet; keeping
# them beside the working generators invites importing half a pipeline.
mkdir -p design
for f in vocabulary.py problem.py grounding.py signature.py fixture.py \
         query.py encoding.py runner.py certificate.py; do
  [ -f "generators/$f" ] && git mv "generators/$f" "design/$f"
done

echo "moved; git status to review, then commit"