#!/bin/bash
# copy the staged k_c 79 folder (files only) into the push worktree's I1025-win/kc79_d185, then commit and push linearly with push_1025.sh
# usage: bash publish_kc79_1025.sh "commit message"; stops at the first failing step; @@T@@ in the staged README is replaced by `date -u` now; the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/kc79_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc79_d185
D=$W/I1025-win/kc79_d185
T=$(date -u '+%Y-%m-%d %H:%M:%S')
sed -i "s/@@T@@/$T/g" "$O/README.md"
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
for f in prep_kc79_inputs_1025.sh prep_kc79_pins_1025.txt prep_kc79_inputs_1025.log kc79_regrid_driver_1025.py kc79_scan_driver_1025.py kc79_watch_alert_1025.py read_kc79_1025.py kc79_syscheck_1025.py \
         sample_driver4_1025.ps1 start_kc79_regrid_1025.cmd start_kc79_scan_1025.cmd kc79_regrid_driver_selftest.log kc79_read_selftest.log kc79_regrid_driver_stdout.log kc79_scan_driver_stdout.log publish_kc79_1025.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
