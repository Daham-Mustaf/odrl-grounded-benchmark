#!/usr/bin/env bash
# What the container runs by default: the environment, then full-run.sh.
#
# The container checks exactly what full-run.sh checks, and exits with its
# status. Everything is written into the container's copy of the
# repository, so the host is untouched unless a volume is mounted.

set -u
cd /benchmark

echo "=== environment"
cat ENVIRONMENT

PROVER_LIMIT="${PROVER_LIMIT:-300}" bash full-run.sh
exit $?
