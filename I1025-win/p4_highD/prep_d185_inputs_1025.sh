#!/bin/bash
# #1025 winb, the D 18.5 root (coordinator's order of 2026-11-21 10:3x UTC): the leap state and the leap record, from raw origin/main by git show,
# each checked by git hash-object --no-filters against its pinned blob.
set -euo pipefail
P=/c/Users/nathan/Source/p4hi_1025
RAWW=/c/Users/nathan/Source/choptuik-large-d-raw-754
git -C "$RAWW" fetch -q origin
cat <<'PINS' | while read -r b p; do
33c1a58b82229d55661cbd5e79d2c1fce0c0717c I1025-mac/d18/sol_l1kc63Wm1025_D18.500000.npy
08f4dbf367edba55814e5cf989ccd32a9a5dbe67 I1025-mac/d18/l1kc63Wm1025.jsonl
PINS
  mkdir -p "$P/raw/$(dirname "$p")"
  git -C "$RAWW" show "origin/main:$p" > "$P/raw/$p"
  h=$(git hash-object --no-filters "$P/raw/$p")
  [ "$h" = "$b" ] || { echo "MISMATCH $p: got $h, pinned $b"; exit 1; }
  echo "ok $b $p"
done > "$P/prep_d185_inputs_1025.log"
echo "prep ok $(grep -c '^ok ' "$P/prep_d185_inputs_1025.log") files"
