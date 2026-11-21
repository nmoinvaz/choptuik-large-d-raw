#!/bin/bash
# copy the staged D 18.125 folder (files only) into the push worktree's I1025-win/d18mid, then commit and push linearly with push_1025.sh
# usage: bash publish_d18mid_1025.sh "commit message"; stops at the first failing step; the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/d18mid_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
O=$S/I1025-win/d18mid
D=$W/I1025-win/d18mid
mkdir -p "$D/rows" "$D/vtest"
cp "$O/README.md" "$D/"
for f in d18mid_w.log d18mid_scanA_1025.jsonl d18mid_scanB_1025.jsonl d18mid_scan_1025.jsonl d18mid_scanA.log d18mid_scanB.log; do [ -f "$O/$f" ] && cp "$O/$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
for f in prep_d18mid_inputs_1025.sh prep_d18mid_pins_1025.txt prep_d18mid_inputs_1025.log d18mid_driver_1025.py sample_driver_1025.ps1 merge_d18mid_1025.py read_d18mid_1025.py \
         start_d18mid_1025.cmd d18mid_driver_selftest.log d18mid_driver_selftest_samples.csv publish_d18mid_1025.sh d18mid_driver_stdout.log; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
for f in read_d18_scan_1025.log read_d185_scan_1025.log merge_selftest.log; do [ -f "$S/vtest/$f" ] && cp "$S/vtest/$f" "$D/vtest/"; done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
