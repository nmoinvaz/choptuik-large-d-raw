#!/usr/bin/env bash
# #945 fifth launch (coordinator's hc, 2026-11-17 ~19:00 UTC): the pass-1 state's --delta_corr again with --threads 10 (#932's leg's thread
# count, which made the record), the same command otherwise, after the fourth launch (stalled state, 8 threads) has exited. Glue only: it waits
# for the 945d exit line, runs the command and logs the exit. The jsonl is a separate file so the 10-thread record is not mixed with the 8-thread one.
# Worktree D:/choptuik-i932 at 808b1fac, venv-i600. usage: bash run945e.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945e $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_945.txt; }
until grep -q '945d plan_floor exit' $R/exits_945.txt 2>/dev/null; do sleep 10; done
log "plan_floor --delta_corr --threads 10 start, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u plan_floor.py $R/plan_floor_t10.jsonl $RAW/I932-win2/states/lowD343_p1_D3.043150_M320.npz \
    --skip_plans --delta_corr --threads 10 > $R/plan_floor_delta_t10.log 2>&1
rc=$?
log "plan_floor exit $rc wall $(( $(date +%s) - t ))s"
