#!/usr/bin/env bash
# lemma 6a(5): capd_m5 c1 (double C^1 doubleton) from the hull of y and sigma(y) at xi1 = 0.3 (I103's box file, w at
# x^ = ZEROS[5] as I103's run had it) to xi_a = 0.067, then compare.py a against I103's X and B. a_clean_I103.log was
# made by this command (first run as the scratch test a_test2, then copied); run under nice -n 10.
set -u
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=${R:-/Users/nathan/Source/choptuik-large-d-raw/I189-mac}
RAW=$(dirname "$R")
PY=${PY:-/Users/nathan/venv-qd/bin/python}
TAG=${TAG:-I103}
START=${START:-$R/inputs/start6a_I103.txt}
B=${B:-$RAW/I103-macm3/B_M5_sub1e-18.json}
export CAPD_M5_PROGRESS=1
"$W/run.sh" "$R/a_clean_$TAG.log" "$W/build/capd_m5" c1 "$START" "$R/inputs/path6a.txt" --order=20 --tol=1e-17
cd "$W" && "$W/run.sh" "$R/cmp_a_clean_$TAG.log" "$PY" compare.py a "$R/a_clean_$TAG.log" "$B" \
  --json="$R/cmp_a_clean_$TAG.json"
