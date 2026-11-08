#!/usr/bin/env bash
# lemma 6b1(5): capd_m5 c0 from the stored C^1 start at s0 through the 17 ray legs and row 17's arc, then compare.py b1.
# Run from anywhere under nice -n 10. R = this raw folder, W = the review_189 code directory.
set -u
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=${R:-/Users/nathan/Source/choptuik-large-d-raw/I189-mac}
RAW=$(dirname "$R")
PY=${PY:-/Users/nathan/venv-qd/bin/python}
export CAPD_M5_PROGRESS=5
"$W/run.sh" "$R/b1_clean.log" "$W/build/capd_m5" c0 "$R/inputs/start6b1.txt" "$R/inputs/path6b1.txt" --prec=128 --order=32 \
  --tol=1e-26
cd "$W" && "$W/run.sh" "$R/cmp_b1_clean.log" "$PY" compare.py b1 "$R/b1_clean.log" \
  "$RAW/I38-macm3/lemma6b1_runs_M5_cert/ray.json" "$RAW/I39-mac/disc_inputs/row_17.json" --json="$R/cmp_b1_clean.json"
