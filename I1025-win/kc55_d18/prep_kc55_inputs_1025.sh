#!/bin/bash
# #1025 winb, the k_c 55 test at D 18 (coordinator order 2026-11-21 22:0x UTC): the scanner, the reader, the k_c 55 D 18 state and its records, and the k_c 63 D 18 scan, from raw origin/main by git show, each checked by git hash-object --no-filters against its pinned blob.
set -euo pipefail
P=/c/Users/nathan/Source/kc55_1025
RAWW=/c/Users/nathan/Source/choptuik-large-d-raw-754
git -C "$RAWW" fetch -q origin
n=0
while read -r b p; do
  mkdir -p "$P/raw/$(dirname "$p")"
  git -C "$RAWW" show "origin/main:$p" > "$P/raw/$p"
  h=$(git hash-object --no-filters "$P/raw/$p")
  [ "$h" = "$b" ] || { echo "MISMATCH $p: got $h, pinned $b"; exit 1; }
  echo "ok $b $p"; n=$((n+1))
done < "$P/prep_kc55_pins_1025.txt" > "$P/prep_kc55_inputs_1025.log"
echo "prep ok $n files"
