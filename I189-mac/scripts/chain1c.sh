#!/usr/bin/env bash
# after chain1b: the kmin check at p^ and its mutation control (each a few seconds)
set -u
D=$(cd "$(dirname "$0")" && pwd)
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=$(dirname "$D")
RAW=$(dirname "$R")
PY=/Users/nathan/venv-qd/bin/python
until grep -q '^series_check' "$R/exits.txt" 2>/dev/null; do sleep 10; done
PHAT=$(cat "$RAW/I184-macm3/phat.txt")
cd "$W" && "$W/run.sh" "$R/kmin_check_phat.log" "$PY" -u kmin_check.py --x="$PHAT"
"$W/run.sh" "$R/kmin_check_mut_series.log" "$PY" -u kmin_check.py --mutate=series
