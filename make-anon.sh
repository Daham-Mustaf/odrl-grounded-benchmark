#!/usr/bin/env bash
# An anonymous copy of the repository at HEAD, for double-blind review.
#
#     bash make-anon.sh [DIR]      # default ../odrl-grounded-benchmark-anon
#
# DIR must not exist and must lie outside this git repository.  The copy has
# no git history.  The generated headers and the TPTP export are rewritten
# there under ODRL_ANON=1, then the whole copy is searched: exit 1 if any
# file matches daham, mustaf or mhamad, ignoring case.  Nothing in this
# repository is changed.

set -u
ROOT="$(cd "$(dirname "$0")" && git rev-parse --show-toplevel)" || exit 1
OUT="${1:-$ROOT/../odrl-grounded-benchmark-anon}"

die() { echo "FAILED: $1" >&2; exit 1; }

[ ! -e "$OUT" ] || die "$OUT already exists"
mkdir -p "$OUT" || die "cannot create $OUT"
OUT="$(cd "$OUT" && pwd -P)"
case "$OUT/" in
  "$(cd "$ROOT" && pwd -P)"/*) rmdir "$OUT"; die "$OUT is inside the repository" ;;
esac
if git -C "$OUT" rev-parse --git-dir >/dev/null 2>&1; then
  rmdir "$OUT"; die "$OUT is inside a git repository"
fi

git -C "$ROOT" archive HEAD | tar -x -C "$OUT" || die "git archive"
cd "$OUT" || exit 1

export ODRL_ANON=1
uv run generators/gen_primitives.py >/dev/null || die gen_primitives
for g in gen_motivating gen_geonames gen_dpv gen_dpvloc gen_filetype \
         gen_consent gen_tom gen_bcp47_problems gen_wellsorted; do
  uv run "generators/$g.py" >/dev/null || die "$g"
done
uv run generators/export_tptp.py >/dev/null || die export_tptp

# The generators hold the real names for ODRL_ANON unset; the copy does not.
python3 - <<'PY' || die "could not take the identity out of the generators"
import re
from pathlib import Path
p = Path("generators/header.py")
t = p.read_text(encoding="utf-8")
t, n = re.subn(r"_REAL = \{.*?\n\}\n", "_REAL = {}\n", t, flags=re.S)
if n != 1:
    raise SystemExit("no _REAL block in generators/header.py")
t = t.replace('return (_ANON if ANONYMOUS else _REAL)[fieldname]', 'return _ANON[fieldname]')
p.write_text(t, encoding="utf-8")
p = Path("generators/export_tptp.py")
t = p.read_text(encoding="utf-8")
t, n = re.subn(r'REF = \(header\.identity\("ref"\) if header\.ANONYMOUS else\n.*?\n',
               'REF = header.identity("ref")\n', t, flags=re.S)
if n != 1:
    raise SystemExit("no REF in generators/export_tptp.py")
t, n = re.subn(r'CITE = .*\n', 'CITE = "[Anon26]"\n', t)
if n != 1:
    raise SystemExit("no CITE in generators/export_tptp.py")
p.write_text(t, encoding="utf-8")
PY
rm -rf .venv
rm -f make-anon.sh

if grep -rIilE 'daham|mustaf|mhamad' . ; then
  die "the files above still name an author; $OUT is not anonymous"
fi
echo "wrote $OUT: no match for daham, mustaf or mhamad"
