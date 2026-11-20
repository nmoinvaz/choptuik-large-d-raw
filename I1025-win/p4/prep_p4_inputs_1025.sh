#!/bin/bash
# #1025 P4 share (win): build the driver's RAW folder from git blobs (no checkout): I1025-mac/p4_hybrid.py (blob a402559b...) and the 7 files of the driver's INPUTS list,
# each by git show from origin/main of the push worktree's repo and checked by git hash-object --no-filters against its pinned blob.
set -euo pipefail
P=/c/Users/nathan/Source/p4_1025
RAWW=/c/Users/nathan/Source/choptuik-large-d-raw-754
DRV=$P/I1025-win/p4/p4_driver_w.sh
{ grep -E '^[0-9a-f]{40} I[0-9]' "$DRV"; echo "a402559b5d37661b49da50f07f877af21fd29b3a I1025-mac/p4_hybrid.py"; } | while read -r b p; do
  mkdir -p "$P/raw/$(dirname "$p")"
  git -C "$RAWW" show "origin/main:$p" > "$P/raw/$p"
  h=$(git hash-object --no-filters "$P/raw/$p")
  [ "$h" = "$b" ] || { echo "MISMATCH $p: got $h, pinned $b"; exit 1; }
  echo "ok $b $p"
done > "$P/prep_p4_inputs_1025.log"
echo "prep ok $(grep -c '^ok ' "$P/prep_p4_inputs_1025.log") files"
