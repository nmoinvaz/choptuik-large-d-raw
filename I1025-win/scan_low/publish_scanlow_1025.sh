#!/bin/bash
# copy the staged low-lambda scan folder (files only) into the push worktree's I1025-win/scan_low, then commit and push linearly with push_1025.sh
# usage: bash publish_scanlow_1025.sh "commit message"; stops at the first failing step; the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/scanlow_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
O=$S/I1025-win/scan_low
D=$W/I1025-win/scan_low
mkdir -p "$D/rows" "$D/vtest"
cp "$O/README.md" "$D/"
for f in "$O"/scanlow_w.log "$O"/scan_*_1025.jsonl "$O"/scan_*_coarse.log "$O"/scan_*_fine.log "$O"/read_*.log; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
for f in prep_scanlow_inputs_1025.sh prep_scanlow_pins_1025.txt prep_scanlow_inputs_1025.log scanlow_driver_1025.py read_scanlow_1025.py sample_driver3_1025.ps1 start_scanlow_1025.cmd \
         scanlow_driver_selftest.log publish_scanlow_1025.sh scanlow_driver_stdout.log; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
for f in d1825_reader_control.log; do [ -f "$S/vtest/$f" ] && cp "$S/vtest/$f" "$D/vtest/"; done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
