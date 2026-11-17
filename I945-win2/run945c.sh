#!/usr/bin/env bash
# #945 third launch, as the coordinator gave it (hc, 2026-11-17 ~13:05 UTC): plan_floor.py on the _ckpt_failed state with
# --skip_plans --by_block --newton f64g --it_max 6. It only runs the command and logs the exit as 945c.
# Worktree D:/choptuik-i932 at origin/main 043834d9, venv-i600, 8 threads.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945c $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_945.txt; }
log "plan_floor --by_block --newton f64g start, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u plan_floor.py $R/plan_floor.jsonl $RAW/I932-win2/states/lowD343_D3.043150_M320_ckpt_failed.npz \
    --skip_plans --by_block --newton f64g --it_max 6 --threads 8 > $R/plan_floor_newton.log 2>&1
rc=$?
log "plan_floor exit $rc wall $(( $(date +%s) - t ))s"
