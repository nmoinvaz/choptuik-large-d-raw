#!/bin/bash
# copy the staged I1111-win folder (files only, and rows/) into the push worktree's I1111-win, then commit and push linearly with push_1025.sh
# usage: bash publish_k127d23_1111.sh "commit message"; stops at the first failing step. In the copy only: @@WT@@ (README line 3) becomes the time of the first publish (README first; kept in
# readme_first_time.txt) and "Pushed @@T@@ UTC." becomes the time of this push. The running job is never touched (read-only copies).
set -euo pipefail
S=/c/Users/nathan/Source/k127d23_1111
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
cd "$W"
[ "$(basename "$(git rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
[ -z "$(git status --porcelain)" ]
git fetch -q origin
git checkout -q --detach origin/main
O=$S/I1111-win
D=$W/I1111-win
T=$(date -u '+%Y-%m-%d %H:%M:%S')
[ -f "$S/readme_first_time.txt" ] || echo "$T" > "$S/readme_first_time.txt"
WT=$(cat "$S/readme_first_time.txt")
mkdir -p "$D/rows"
for f in "$O"/*; do [ -f "$f" ] && cp "$f" "$D/"; done
cp "$O/rows/"* "$D/rows/" 2>/dev/null || true
sed -i "s/@@WT@@/$WT/g; s/^Pushed @@T@@ UTC\./Pushed $T UTC./" "$D/README.md"
for f in w127_1111_driver.py k127_watch_alert_1111.py sample_driver_1111.ps1 go_w127_1111.cmd keepawake_1111.py session_check_1111.ps1 publish_1111.sh push_1111.sh selftest_driver_dry_1111.txt driver_stdout_1111.log; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/k127d23_1111/push_1111.sh "$1"
