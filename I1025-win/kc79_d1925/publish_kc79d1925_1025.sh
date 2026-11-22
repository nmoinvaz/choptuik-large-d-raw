#!/bin/bash
# copy the staged k_c 79 D 19.25 folder (files only) into the push worktree's I1025-win/kc79_d1925, then commit and push linearly with push_1025.sh
# usage: bash publish_kc79d1925_1025.sh "commit message"; stops at the first failing step; @@T@@ in the staged README is replaced by `date -u` in the copy only (the staged README keeps the placeholder); the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/kc79d1925_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc79_d1925
D=$W/I1025-win/kc79_d1925
T=$(date -u '+%Y-%m-%d %H:%M:%S')
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
sed -i "s/@@T@@/$T/g" "$D/README.md"
for f in make_d1925_1025.py diff_regrid_driver_vs_d19.txt diff_scan_driver_vs_d19.txt diff_watcher_vs_d19.txt diff_find_vs_d19.txt prep_kc79d1925_find_1025.py prep_kc79d1925_pins_fixed.txt prep_kc79d1925_pins_1025.txt kc79d1925_cfg_1025.txt \
         kc79d1925_regrid_driver_1025.py kc79d1925_scan_driver_1025.py kc79d1925_watch_alert_1025.py kc79_syscheck_1025.py sample_driver4_1025.ps1 start_kc79d1925_regrid_1025.cmd start_kc79d1925_scan_1025.cmd \
         selftest_find_1025.txt find_run_1025.txt selftest_scan_dry_1025.txt kc79_regrid_driver_selftest.log kc79d1925_regrid_driver_stdout.log kc79d1925_scan_driver_stdout.log publish_kc79d1925_1025.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
