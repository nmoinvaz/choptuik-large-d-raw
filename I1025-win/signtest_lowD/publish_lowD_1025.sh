#!/bin/bash
# copy the staged low-D signtest folder into the push worktree's I1025-win/signtest_lowD (files only, no -u), then commit and push linearly with push_1025.sh
# usage: bash publish_lowD_1025.sh "commit message"
set -euo pipefail
S=/c/Users/nathan/Source/signtest_lowD_1025
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
D=$W/I1025-win/signtest_lowD
mkdir -p "$D/signtest_lowD_rows"
cp "$S/I1025-win/signtest_lowD/"*.md "$S/I1025-win/signtest_lowD/"*.sh "$D/"
for f in signtest_lowD.log signtest_lowD.jsonl signtest_lowD_planted.log; do [ -f "$S/I1025-win/signtest_lowD/$f" ] && cp "$S/I1025-win/signtest_lowD/$f" "$D/"; done
cp "$S/I1025-win/signtest_lowD/signtest_lowD_rows/"*.log "$D/signtest_lowD_rows/" 2>/dev/null || true
cp "$S/prep_raw_inputs_1025.sh" "$S/prep_raw_inputs_1025.log" "$S/start_lowD_1025.cmd" "$S/publish_lowD_1025.sh" "$D/"
bash /c/Users/nathan/Source/choptuik-i1025/push_1025.sh "$1"
