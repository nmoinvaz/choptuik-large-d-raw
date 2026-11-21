#!/bin/bash
# copy the staged lambda 1.20 folder (files only) into the push worktree's I1025-win/d18ref120, then commit and push linearly with push_1025.sh
# usage: bash publish_ref120_1025.sh "commit message"; stops at the first failing step; the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/ref120_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
O=$S/I1025-win/d18ref120
D=$W/I1025-win/d18ref120
mkdir -p "$D/rows"
cp "$O/README.md" "$O/"stub_*.jsonl "$D/"
for f in ref120_w.log; do [ -f "$O/$f" ] && cp "$O/$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
for f in prep_ref120_inputs_1025.sh prep_ref120_pins_1025.txt prep_ref120_inputs_1025.log make_stubs_ref120_1025.py make_stubs_ref120_1025.log smoke_syscheck_ref120_1025.cmd \
         smoke_syscheck_D18.log smoke_syscheck_D18.0625.log selftest_ddm_ref120_1025.cmd ref120_driver_1025.py read_ref120_1025.py sample_driver2_1025.ps1 start_ref120_1025.cmd \
         ref120_driver_selftest.log ref120_driver_selftest_samples.csv publish_ref120_1025.sh ref120_driver_stdout.log; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
