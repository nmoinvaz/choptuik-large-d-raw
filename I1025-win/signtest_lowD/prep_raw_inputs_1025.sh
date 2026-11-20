#!/bin/bash
# #1025 (win) low-D signtests: build the driver's RAW folder from git blobs (no checkout anywhere): every "RAW" path of the driver's INPUTS list plus I1025-mac/signtest.py,
# each taken by git show from origin/main of the push worktree's repo and checked with git hash-object --no-filters against the pinned blob. Prints 'prep ok N files' or the first failure.
set -euo pipefail
S=/c/Users/nathan/Source/signtest_lowD_1025
RAWW=/c/Users/nathan/Source/choptuik-large-d-raw-754
DRV=$S/I1025-win/signtest_lowD/signtest_lowD_driver_v2.sh
n=0
{ grep -E '^[0-9a-f]{40} RAW ' "$DRV"; echo "179ea09681b0a75f7cefdff98984b48051b3f085 RAW I1025-mac/signtest.py"; } | while read -r b w p; do
  mkdir -p "$S/raw/$(dirname "$p")"
  git -C "$RAWW" show "origin/main:$p" > "$S/raw/$p"
  h=$(git hash-object --no-filters "$S/raw/$p")
  [ "$h" = "$b" ] || { echo "MISMATCH $p: got $h, pinned $b"; exit 1; }
  echo "ok $b $p"
done > "$S/prep_raw_inputs_1025.log"
echo "prep ok $(grep -c '^ok ' "$S/prep_raw_inputs_1025.log") files"
