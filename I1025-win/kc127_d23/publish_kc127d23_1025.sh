#!/bin/bash
# copy the staged k_c 127 D 23.0 folder (files only, and secant/) into the push worktree's I1025-win/kc127_d23, then commit and push linearly with push_1025.sh
# usage: bash publish_kc127d23_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in
# readme_first_time.txt) and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc127d23_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc127_d23
D=$W/I1025-win/kc127_d23
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows" "$D/secant"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
cp "$O/secant/"* "$D/secant/" 2>/dev/null || true
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in make_kc127d23_1025.py make_kc127d23_part2_1025.py diff_regrid_driver_vs_kc103.txt diff_scan_driver_vs_kc103.txt diff_secant_driver_vs_kc87.txt kc127d23_regrid_driver_1025.py kc127d23_scan_driver_1025.py          kc127d23_secant_driver_1025.py kc127d23_watch_alert_1025.py sample_driver_kc127_1025.ps1 go_kc127d23_1025.cmd go_secant_kc127d23_1025.cmd keepawake_1025.py session_check_1025.ps1 prep_kc127d23_pins_1025.txt          prep_source_checks_by_hand.txt prep_secant_selftests_by_hand.txt selftest_scan_dry_1025.txt kc127d23_regrid_driver_stdout.log kc127d23_scan_driver_stdout.log kc127d23_secant_driver_stdout.log publish_kc127d23_1025.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
