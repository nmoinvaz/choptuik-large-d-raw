#!/bin/bash
# copy the staged follow-on folder (files only) into the push worktree's I1025-win/p4_highD, then commit and push linearly with push_1025.sh
# usage: bash publish_p4hi_1025.sh "commit message"; stops at the first failing step; the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/p4hi_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
O=$S/I1025-win/p4_highD
D=$W/I1025-win/p4_highD
mkdir -p "$D/rows"
cp "$O/README.md" "$O/"stub_*.jsonl "$D/"
for f in d185_w.log ell_p4_hybrid_1025_w_highD_d185.jsonl d185_driver_selftest.log d185_driver_selftest_samples.csv read_ddB_selftest_1025.log p4hi_w.log ddB_w.log ddB_driver_selftest.log ell_p4_hybrid_1025_w_highD.jsonl; do [ -f "$O/$f" ] && cp "$O/$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
for f in prep_p4hi_inputs_1025.sh prep_p4hi_inputs_1025.log make_stubs_p4hi_1025.py make_stubs_p4hi_1025.log smoke_syscheck_p4hi_1025.cmd \
         smoke_syscheck_A.log smoke_syscheck_B.log prep_d185_inputs_1025.sh prep_d185_inputs_1025.log make_stub_d185_1025.py make_stub_d185_1025.log smoke_syscheck_d185_1025.cmd smoke_syscheck_d185.log d185_driver_1025.py verdict_d185_1025.py start_d185_1025.cmd sample_d185_1025.ps1 ddB_driver_1025.py read_ddB_1025.py read_ddB_1025_v1.py read_ddB_selftest_1025.py selftest_ddm_p4hi_1025.cmd start_ddB_1025.cmd ddB_w.log p4hi_driver_1025.sh verdict_p4hi_1025.py verdict_p4hi_1025_v1.py start_p4hi_1025.cmd driver_trace_p4hi.log publish_p4hi_1025.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
