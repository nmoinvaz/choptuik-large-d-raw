#!/bin/bash
# copy the staged k_c 87 D 19 folder (files only) into the push worktree's I1025-win/kc87_d19, then commit and push linearly with push_1025.sh
# usage: bash publish_kc87d19_1025.sh "commit message"; stops at the first failing step; @@T@@ in the staged README is replaced by `date -u` in the copy only (the staged README keeps the placeholder); the running job is never touched (read-only copies)
set -euo pipefail
S=/c/Users/nathan/Source/kc87d19_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc87_d19
D=$W/I1025-win/kc87_d19
T=$(date -u '+%Y-%m-%d %H:%M:%S')
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
mkdir -p "$D/combined"
cp "$O/combined/"* "$D/combined/" 2>/dev/null || true
sed -i "s/@@T@@/$T/g" "$D/README.md"
for f in make_kc87d19_1025.py diff_scan_driver_vs_gap.txt diff_watcher_vs_gap.txt diff_regrid_driver_vs_d19.txt prep_kc87d19_pins_1025.txt kc87d19_regrid_driver_1025.py kc87d19_scan_driver_1025.py kc87d19_watch_alert_1025.py sample_driver4_1025.ps1 \
         go_kc87d19_1025.cmd keepawake_1025.py session_check_1025.ps1 selftest_scan_dry_1025.txt kc87d19_regrid_driver_stdout.log kc87d19_scan_driver_stdout.log publish_kc87d19_1025.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
