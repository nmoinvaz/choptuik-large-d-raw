#!/bin/bash
# copy the staged k_c 87 D 22.875 secant folder (files only) into the push worktree's I1025-win/kc87_d22875_secant, then commit and push linearly with push_1025.sh
# usage: bash publish_kc87d22875s_1025.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in
# readme_first_time.txt) and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/kc87d22875s_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1025-win/kc87_d22875_secant
D=$W/I1025-win/kc87_d22875_secant
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows" "$D/in"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
cp "$O/in/"* "$D/in/"
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in make_kc87d22875s_1025.py diff_secant_driver_vs_kc95.txt kc87d22875s_secant_driver_1025.py kc87d22875s_watch_alert_1025.py sample_driver_secant_1025.ps1 go_kc87d22875s_1025.cmd keepawake_1025.py session_check_1025.ps1 \
         selftest_secant_dry_1025.txt kc87d22875s_secant_driver_stdout.log publish_kc87d22875s_1025.sh prep_kc87d22875s_pins_1025.txt prep_source_checks_by_hand.txt prep_secant_selftests_by_hand.txt; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
