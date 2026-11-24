#!/bin/bash
# copy the staged k_c 103 D 21.0 folder (files only) into the push worktree's I1025-win/kc103_d21, then commit and push linearly with push_1025.sh
# usage: bash publish_kc103d21_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in readme_first_time.txt),
# and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc103d21_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc103_d21
D=$W/I1025-win/kc103_d21
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in make_kc103d21_1025.py kc103_syscheck_1025_vs_kc95.diff diff_regrid_driver_vs_kc95d21.txt kc103d21_regrid_driver_1025.py kc103d21_scan_driver_1025.py kc103d21_watch_alert_1025.py sample_driver4_1025.ps1 go_kc103d21_1025.cmd keepawake_1025.py session_check_1025.ps1 \
         selftest_scan_dry_1025.txt kc103d21_regrid_driver_stdout.log kc103d21_scan_driver_stdout.log publish_kc103d21_1025.sh prep_kc103d21_pins_1025.txt; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
