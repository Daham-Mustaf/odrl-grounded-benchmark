#!/usr/bin/env python3
"""
check_vendored.py
=================
Every vendored file is byte for byte the file its source publishes.

    uv run generators/check_vendored.py [--dir vocabularies]

vocabularies/MANIFEST lists each vendored file with its sha256, the URL it
was taken from and the upstream commit or retrieval date.  This checks that
every listed file is there with that sha256, that each entry names its
source and upstream, and that every file in the folder is listed.  The
README.md files are this project's notes and are not listed.

A builder reads these files, and a resource header records some of their
hashes, so a file that has drifted, even by a final newline, makes every
figure built from it unreproducible.  Exit 1 on any difference.
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_ENTRY = re.compile(r"^([0-9a-f]{64})  (\S.*)$")
_FIELD = re.compile(r"^    (source|upstream)\s+(\S.*)$")


def read_manifest(path: Path) -> dict:
    """path -> {"sha256", "source", "upstream"}."""
    entries, current = {}, None
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        m = _ENTRY.match(line)
        if m:
            if m.group(2) in entries:
                raise SystemExit(f"{path}:{n}: {m.group(2)} is listed twice")
            current = entries[m.group(2)] = {"sha256": m.group(1)}
            continue
        f = _FIELD.match(line)
        if f and current is not None:
            current[f.group(1)] = f.group(2)
            continue
        raise SystemExit(f"{path}:{n}: cannot read {line!r}")
    return entries


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dir", default=ROOT / "vocabularies", type=Path)
    args = ap.parse_args()

    manifest = args.dir / "MANIFEST"
    if not manifest.exists():
        print(f"no {manifest}", file=sys.stderr)
        return 1
    entries = read_manifest(manifest)
    failures = []
    for rel, e in sorted(entries.items()):
        path = args.dir / rel
        for field in ("source", "upstream"):
            if field not in e:
                failures.append(f"{rel}: the entry has no {field}")
        if not path.is_file():
            failures.append(f"{rel}: listed, not found")
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != e["sha256"]:
            failures.append(f"{rel}: sha256 {got}, the manifest says {e['sha256']}")
    on_disk = {str(p.relative_to(args.dir)) for p in args.dir.rglob("*")
               if p.is_file() and p.name not in ("MANIFEST", "README.md")}
    for rel in sorted(on_disk - set(entries)):
        failures.append(f"{rel}: vendored, not in the manifest")

    for f in failures:
        print(f"    FAIL {f}")
    print(f"{len(entries)} vendored files listed; "
          + (f"{len(failures)} differences" if failures
             else "every sha256 matches, and every file is listed"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
