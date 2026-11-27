#!/bin/bash
# copy the staged k_c 143 D 23.0 folder (files only, and secant/) into the push worktree's I1025-win/kc143_d23, then commit and push linearly with push_1025.sh
# usage: bash publish_kc143d23_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in
# readme_first_time.txt) and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc143d23_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc143_d23
D=$W/I1025-win/kc143_d23
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows" "$D/secant"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
cp "$O/secant/"* "$D/secant/" 2>/dev/null || true
if [ -d "$O/dry_rust_vs_ddm_kc31" ]; then mkdir -p "$D/dry_rust_vs_ddm_kc31"; cp "$O/dry_rust_vs_ddm_kc31/"* "$D/dry_rust_vs_ddm_kc31/"; fi
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in make_kc143d23_1025.py diff_regrid_driver_vs_kc127.txt diff_scan_driver_vs_kc127.txt diff_secant_driver_vs_kc127.txt kc143d23_regrid_driver_1025.py kc143d23_scan_driver_1025.py kc143d23_secant_driver_1025.py kc143d23_watch_alert_1025.py sample_driver_kc143_1025.ps1 go_kc143d23_1025.cmd go_secant_kc143d23_1025.cmd keepawake_1025.py session_check_1025.ps1 prep_kc143d23_pins_1025.txt selftest_scan_dry_1025.txt selftest_secant_dry_1025.txt dry_tests_scan_1025.sh dry_test_secant_1025.sh dry_rust_scan_kc31_1025.sh compare_dry_rust_kc31.py prep_source_checks_by_hand.sh prep_source_checks_by_hand.txt kc143d23_regrid_driver_stdout.log kc143d23_scan_driver_stdout.log kc143d23_secant_driver_stdout.log publish_kc143d23_1025.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
