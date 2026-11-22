#!/bin/bash
# #1025 winb, the k_c 79 convergence check at D 18.5 (coordinator order 2026-11-22 03:3x UTC): win2s k_c 71 D 18.5 state and record, its acceptance check and README, and xfkappas scanner and readers, from raw origin/main by git show, each checked by git hash-object --no-filters against its pinned blob.
P=/c/Users/nathan/Source/kc79_1025
RAWW=/c/Users/nathan/Source/choptuik-large-d-raw-754
git -C "$RAWW" fetch -q origin
n=0
while read -r b p; do
  mkdir -p "$P/raw/$(dirname "$p")"
  git -C "$RAWW" show "origin/main:$p" > "$P/raw/$p"
  h=$(git hash-object --no-filters "$P/raw/$p")
  [ "$h" = "$b" ] || { echo "MISMATCH $p: got $h, pinned $b"; exit 1; }
  echo "ok $b $p"; n=$((n+1))
done < "$P/prep_kc79_pins_1025.txt" > "$P/prep_kc79_inputs_1025.log"
echo "prep ok $n files"
