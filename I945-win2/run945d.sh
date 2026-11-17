#!/usr/bin/env bash
# #945 fourth launch (coordinator's hc, 2026-11-17 ~17:19 UTC): the floor's linearised effect on Delta, --delta_corr on the pass-1 state (the check,
# its record's dDelta_est -1.831e-17) and the _ckpt_failed state. Glue only: runs the command as given and logs the exit.
# Worktree D:/choptuik-i932 at 808b1fac, venv-i600, 8 threads. usage: bash run945d.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945d $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_945.txt; }
log "plan_floor --delta_corr start, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u plan_floor.py $R/plan_floor.jsonl $RAW/I932-win2/states/lowD343_p1_D3.043150_M320.npz \
    $RAW/I932-win2/states/lowD343_D3.043150_M320_ckpt_failed.npz --skip_plans --delta_corr --threads 8 > $R/plan_floor_delta.log 2>&1
rc=$?
log "plan_floor exit $rc wall $(( $(date +%s) - t ))s"
