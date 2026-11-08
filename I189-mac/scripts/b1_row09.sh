#!/usr/bin/env bash
# lemma 6b1(5) row 9: capd_m5 c0 from the stored C^1 start at s0 = 405 e^{-3 i pi/4} along the first 9 ray legs and
# row 9's arc (|u| = 165.24, 17 disc times), then compare.py b1 against I39-mac/disc_inputs/row_09.json. Run under
# nice -n 10.
set -u
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=${R:-/Users/nathan/Source/choptuik-large-d-raw/I189-mac}
RAW=$(dirname "$R")
PY=${PY:-/Users/nathan/venv-qd/bin/python}
export CAPD_M5_PROGRESS=10
"$W/run.sh" "$R/b1_row09.log" "$W/build/capd_m5" c0 "$R/inputs/start6b1.txt" "$R/inputs/path6b1_row09.txt" --prec=128 \
  --order=32 --tol=1e-26
cd "$W" && "$W/run.sh" "$R/cmp_b1_row09.log" "$PY" compare.py b1 "$R/b1_row09.log" \
  "$RAW/I38-macm3/lemma6b1_runs_M5_cert/ray.json" "$RAW/I39-mac/disc_inputs/row_09.json" --json="$R/cmp_b1_row09.json"
