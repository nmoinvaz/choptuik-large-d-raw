#!/usr/bin/env bash
# capd_m5's inputs for #208, written by review_189/export_inputs.py from the stored files: the C^1 start set at
# s0 = 405 e^{-3 i pi/4} (ray.json sets["0"]) and the path of every row J = 0..16 (ray legs 1..J, then row J's arc
# with a stop at each disc time). The start and rows 0 and 9 must reproduce I189-mac/inputs byte for byte.
set -u
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a1cd434a46c3bedb1/solver/proof/review_189}
R=${R:-/Users/nathan/Source/choptuik-large-d-raw/I208-mac}
RAW=$(dirname "$R")
PY=${PY:-/Users/nathan/venv-qd/bin/python}
RAY="$RAW/I38-macm3/lemma6b1_runs_M5_cert/ray.json"
cd "$W" || exit 2
"$PY" export_inputs.py start6b1 "$RAY" "$R/inputs/start6b1.txt" || exit 1
for j in $(seq 0 16); do
  jj=$(printf %02d "$j")
  "$PY" export_inputs.py path6b1 "$RAY" "$RAW/I39-mac/disc_inputs/row_$jj.json" "$R/inputs/path6b1_row$jj.txt" || exit 1
done
rc=0
# start6b1.txt's header names the ray.json path, the same file at the same path in both folders
for f in start6b1.txt path6b1_row00.txt path6b1_row09.txt; do
  if cmp "$R/inputs/$f" "$RAW/I189-mac/inputs/$f"; then
    echo "$f: identical to I189-mac/inputs/$f"
  else
    echo "$f: DIFFERS from I189-mac/inputs/$f"
    rc=1
  fi
done
exit $rc
