#!/bin/bash
# copy the staged I1104-win folder (files only, and secant/) into the push worktree's I1104-win, then commit and push linearly with push_1025.sh
# usage: bash publish_k050d23_1104.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in
# readme_first_time.txt) and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/k050d23_1104
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1104-win
D=$W/I1104-win
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows" "$D/secant"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
cp "$O/secant/"* "$D/secant/" 2>/dev/null || true
if [ -d "$O/dry_rust_vs_ddm_kc31" ]; then mkdir -p "$D/dry_rust_vs_ddm_kc31"; cp "$O/dry_rust_vs_ddm_kc31/"* "$D/dry_rust_vs_ddm_kc31/"; fi
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in make_k050d23_1104.py k050d23_regrid_driver_1104.py k050d23_watch_alert_1104.py sample_driver_k050_1104.ps1 go_k050d23_1104.cmd keepawake_1104.py session_check_1104.ps1 steps_check_1104.py steps_check_1104.txt k050d23_scan_driver_1104.py k050d23_secant_driver_1104.py make_k050d23_1104_part2.py go_secant_k050d23_1104.cmd k050d23_regrid_driver_stdout.log k050d23_scan_driver_stdout.log k050d23_secant_driver_stdout.log selftest_scan_dry_1104.txt selftest_secant_dry_1104.txt dry_tests_scan_1104.sh dry_test_secant_1104.sh publish_k050d23_1104.sh push_1104.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
cp "$S/inputs/gate_k050_1104.py" "$D/"
bash /c/Users/nathan/Source/k050d23_1104/push_1104.sh "$1"
