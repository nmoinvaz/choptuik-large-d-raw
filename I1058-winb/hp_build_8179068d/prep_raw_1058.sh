#!/bin/bash
# #1058 winb: the stored references of the hp checks, taken from raw origin/main by git show into a plain folder (bytes as stored),
# each checked against its blob with git hash-object --no-filters. Reads the live raw clone only (no checkout, no pull).
set -euo pipefail
R=/c/Users/nathan/Source/choptuik-large-d-raw
D=/c/Users/nathan/Source/hp1058_winb/raw
git -C "$R" fetch -q origin
echo "raw origin/main $(git -C "$R" rev-parse --short origin/main)"
for p in T81/ref_main.json T81/scaled_main.json anm-mac/jets_inputs/jets_inputs.json anm-mac/jets_inputs/jets_inputs_inputs.npz; do
  mkdir -p "$D/$(dirname "$p")"
  git -C "$R" show "origin/main:$p" > "$D/$p"
  want=$(git -C "$R" rev-parse "origin/main:$p")
  got=$(git hash-object --no-filters "$D/$p")
  size=$(wc -c < "$D/$p")
  if [ "$want" = "$got" ]; then
    echo "ok $got $p ($size bytes)"
  else
    echo "MISMATCH $p want $want got $got"
    exit 1
  fi
done
