#!/bin/bash
# copy the staged k_c 87 D 21.09375 folder (files only) into the push worktree's I1025-win/kc87_leg_lambda/21.09375, then commit and push linearly with push_1025.sh
# usage: bash publish_kc87_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in readme_first_time.txt),
# and "Pushed @@T@@ UTC." becomes the time of this push. The master README (kc87leg_1025) is copied to I1025-win/kc87_leg_lambda/README.md. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc87d2109375_1025
M=/c/Users/nathan/Source/kc87leg_1025/I1025-win/kc87_leg_lambda
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc87_leg_lambda/21.09375
D=$W/I1025-win/kc87_leg_lambda/21.09375
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
[ -f "$M/README.md" ] && cp "$M/README.md" "$W/I1025-win/kc87_leg_lambda/README.md"
for f in kc87_scan_driver_1025.py kc87_watch_alert_1025.py sample_driver4_1025.ps1 go_kc87_1025.cmd keepawake_1025.py session_check_1025.ps1 selftest_scan_dry_1025.txt kc87_scan_driver_stdout.log publish_kc87_1025.sh prep_pins_1025.txt point.json; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
