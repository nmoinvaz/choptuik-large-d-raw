#!/bin/bash
# copy the staged k_c 55 folder (files only) into the push worktree's I1025-win/kc55_d18, then commit and push linearly with push_1025.sh
# usage: bash publish_kc55_1025.sh "commit message"; stops at the first failing step; the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/kc55_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
O=$S/I1025-win/kc55_d18
D=$W/I1025-win/kc55_d18
mkdir -p "$D/rows" "$D/vtest"
cp "$O/README.md" "$O/stub_kc55_D18.jsonl" "$D/"
for f in "$O"/kc55_w.log "$O"/scan_kc55_D18_1025.jsonl "$O"/scan_kc55_D18.log "$O"/read_*.log; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
for f in prep_kc55_inputs_1025.sh prep_kc55_pins_1025.txt prep_kc55_inputs_1025.log kc55_driver_1025.py read_kc55_1025.py sample_driver3_1025.ps1 start_kc55_1025.cmd \
         smoke_syscheck_kc55_1025.cmd smoke_syscheck_kc55.log kc55_driver_selftest.log publish_kc55_1025.sh kc55_driver_stdout.log; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
[ -f "$S/vtest/kc63_D18_control.log" ] && cp "$S/vtest/kc63_D18_control.log" "$D/vtest/"
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
