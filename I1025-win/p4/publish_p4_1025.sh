#!/bin/bash
# copy the staged P4 folder (files only) into the push worktree's I1025-win/p4, then commit and push linearly with push_1025.sh
# usage: bash publish_p4_1025.sh "commit message"; stops at the first failing step; the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/p4_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
O=$S/I1025-win/p4
D=$W/I1025-win/p4
mkdir -p "$D/p4_rows"
cp "$O/README.md" "$O/p4_driver_w.sh" "$D/"
for f in p4_w.log ell_p4_hybrid_1025_w.jsonl; do [ -f "$O/$f" ] && cp "$O/$f" "$D/"; done
cp "$O/p4_rows/"*.log "$D/p4_rows/" 2>/dev/null || true
for f in start_p4_1025.cmd start_p4b_1025.cmd start_p4c_1025.cmd start_prio_p4_1025.cmd prio_p4_1025.ps1 prio_p4_1025.log \
         prep_p4_inputs_1025.sh prep_p4_inputs_1025.log driver_trace.log driver_trace2.log publish_p4_1025.sh; do
  cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
