#!/bin/bash
# copy the staged k_c 103 D 22.875 folder (files only) into the push worktree's I1025-win/kc103_d22875, then commit and push linearly with push_1025.sh
# usage: bash publish_kc103d22875_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in readme_first_time.txt),
# and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc103d22875_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc103_d22875
D=$W/I1025-win/kc103_d22875
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
if [ -d "$O/secant" ]; then   # the secant refinement's folder: its README has its own first-publish time
  mkdir -p "$D/secant"
  [ -f "$S/readme_first_time_secant.txt" ] || echo "$T" > "$S/readme_first_time_secant.txt"
  SWT=$(cat "$S/readme_first_time_secant.txt")
  for f in "$O"/secant/*; do [ -f "$f" ] && cp "$f" "$D/secant/"; done
  [ -f "$D/secant/README.md" ] && sed -i "s/@@WT@@/$SWT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/secant/README.md"
fi
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in make_kc103d22875_1025.py kc103_syscheck_1025_vs_kc95.diff diff_regrid_driver_vs_prev.txt kc103d22875_regrid_driver_1025.py kc103d22875_scan_driver_1025.py kc103d22875_watch_alert_1025.py sample_driver4_1025.ps1 go_kc103d22875_1025.cmd keepawake_1025.py session_check_1025.ps1 \
         selftest_scan_dry_1025.txt kc103d22875_regrid_driver_stdout.log kc103d22875_scan_driver_stdout.log kc103d22875_secant_driver_stdout.log kc103d22875_secant_driver_1025.py sample_driver_secant_1025.ps1 go_secant_kc103d22875_1025.cmd prep_secant_selftests_by_hand.txt selftest_secant_dry_1025.txt publish_kc103d22875_1025.sh prep_kc103d22875_pins_1025.txt prep_source_checks_by_hand.txt; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
