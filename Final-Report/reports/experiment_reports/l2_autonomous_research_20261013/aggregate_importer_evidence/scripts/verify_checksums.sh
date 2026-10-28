#!/usr/bin/env bash
# Verify that data/{core,extended}/ files match their manifest.json checksums.
#
# Usage:
#   bash scripts/verify_checksums.sh              # verify ./data/{core,extended}
#   bash scripts/verify_checksums.sh /tmp/rebuild # verify a fresh rebuild dir
set -euo pipefail

TARGET="${1:-.}"
overall=0

for tier in core extended; do
    manifest="$TARGET/data/$tier/manifest.json"
    if [[ ! -f "$manifest" ]]; then
        echo "(skip) $tier — manifest.json not present"
        continue
    fi
    echo "verifying $tier against $manifest"
    if python3 - "$manifest" "$TARGET/data/$tier" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

manifest_path, base = sys.argv[1], Path(sys.argv[2])
m = json.loads(Path(manifest_path).read_text())
bad = 0
files = m.get("files", {})
if not files:
    print("  (manifest lists no files)")
for name, expected in sorted(files.items()):
    p = base / name
    if not p.exists():
        print(f"  MISSING  {name}")
        bad += 1
        continue
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    if h.hexdigest() == expected:
        print(f"  OK       {name}")
    else:
        print(f"  MISMATCH {name}")
        bad += 1
sys.exit(1 if bad else 0)
PY
    then :; else overall=1; fi
done

if [[ $overall -eq 0 ]]; then
    echo "verify_checksums: OK"
else
    echo "verify_checksums: FAILED" >&2
fi
exit $overall
