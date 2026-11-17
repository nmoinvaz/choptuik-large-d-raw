#!/usr/bin/env bash
# #945 step 1 as the coordinator gave it (hc, 2026-11-17): plan_floor.py on the D 3.04315 _fail state, then the pass-1 state.
# It only runs the command and logs the exit. Worktree D:/choptuik-i932 at origin/main fa922af9, venv-i600, 8 threads.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_945.txt; }
log "plan_floor start, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u plan_floor.py $R/plan_floor.jsonl $RAW/I932-win2/states/lowD343_D3.043150_M320_fail.npz \
    $RAW/I932-win2/states/lowD343_p1_D3.043150_M320.npz --threads 8 > $R/plan_floor.log 2>&1
rc=$?
log "plan_floor exit $rc wall $(( $(date +%s) - t ))s"
