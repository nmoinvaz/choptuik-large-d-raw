#!/usr/bin/env bash
# #945 ninth launch (coordinator's hc, 2026-11-19 ~00:20 UTC, Nathan approved chord steps for the low-D solve): the resume of run945i.sh's command, unchanged (--resume, --prefer_start predictor,
# --accept 1e-20, --point_hours 30, 10 threads) plus --chord_from 1e-16, after M 384's pass 1 printed its converged line and the leg of run945i.sh was stopped by its exact pids.
# The worktree D:/choptuik-i932 is fast-forwarded to origin/main 82412047 first (Python only). Glue: it does NOT restore the progress file (run945i.sh's setup is not repeated, the file
# keeps the state of the leg that was stopped), it chains the one command and logs the start and the exit in exits_945.txt. The file's stop rules are watched by w945i.sh. usage: bash run945j.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2/leg
X=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945j $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_945.txt; }
log "resume of step 2 (--accept 1e-20 --prefer_start predictor --chord_from 1e-16) start, main $(git rev-parse --short=8 HEAD), progress file kept as the stopped leg left it"
t=$(date +%s)
"$PY" -u lowD_highM.py --start_w $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --start_n $RAW/I343-win2/states/lowD343_D3.043350_M384.npz --Ms 320,384 --dD 0.0002 --D_end 3.0431 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 30 --threads 10 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl --resume --it_max 8 \
    --sonic_refine 4 --sonic_stop --accept 1e-20 --prefer_start predictor --chord_from 1e-16 >> $R/leg.log 2>&1
log "resume of step 2 exit $? wall $(( $(date +%s) - t ))s"
