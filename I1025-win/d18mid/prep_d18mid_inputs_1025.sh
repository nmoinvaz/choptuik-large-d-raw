#!/bin/bash
# #1025 winb, the D 18.125 scan (coordinator's order of 2026-11-21 13:2x UTC): xfkappa's scanner, the leap state and the leap record, and the D 18 and D 18.5 scans
# (for the reader's tests and its D 18 comparison), from raw origin/main by git show, each checked by git hash-object --no-filters against its pinned blob.
set -euo pipefail
P=/c/Users/nathan/Source/d18mid_1025
RAWW=/c/Users/nathan/Source/choptuik-large-d-raw-754
git -C "$RAWW" fetch -q origin
n=0
while read -r b p; do
  mkdir -p "$P/raw/$(dirname "$p")"
  git -C "$RAWW" show "origin/main:$p" > "$P/raw/$p"
  h=$(git hash-object --no-filters "$P/raw/$p")
  [ "$h" = "$b" ] || { echo "MISMATCH $p: got $h, pinned $b"; exit 1; }
  echo "ok $b $p"; n=$((n+1))
done < "$P/prep_d18mid_pins_1025.txt" > "$P/prep_d18mid_inputs_1025.log"
echo "prep ok $n files"
