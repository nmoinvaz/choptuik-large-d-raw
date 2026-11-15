#!/usr/bin/env bash
# #343 leg 2 on win2 (the coordinator): the leg continued after the first run's rule stop. lowD_highM_leg.py copies its
# progress file to leg2.jsonl.progress.json with the stop cleared and the targets below. lowD_highM.py then resumes with
# wider time limits (--point_hours 30, --hours 120), because D 3.04335's pass 1 alone took more than the old 8 h. Same
# worktree, venv and arguments as run343.sh otherwise. Run it only after leg.log shows the stop. 10 threads.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I343-win2
cd /d/choptuik-i343/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "343 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_343.txt; }
grep -q '"done"' $R/leg.jsonl.progress.json || { log "leg2: the first run has not stopped (no done in its progress file)"; exit 9; }
"$PY" -u lowD_highM_leg.py $R/leg.jsonl.progress.json $R/leg2.jsonl \
    --targets 3.04295,3.04255,3.04215,3.04175,3.04135,3.04095,3.04055,3.04015 --states $R/states >> $R/leg2.log 2>&1 \
    || { log "leg2: lowD_highM_leg.py exit $?"; exit 9; }
log "leg2 start, main $(git rev-parse --short=8 HEAD)"
"$PY" -u lowD_highM.py --start_w $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M320.npz \
    --start_n $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M384.npz --Ms 320,384 --dD 0.0004 --D_end 3.040 \
    --min_step 0.00005 --diff_max 1e-8 --hours 120 --point_hours 30 --threads 10 --tag lowD343 \
    --states $R/states --out $R/leg2.jsonl --points $R/leg2_points.jsonl --resume >> $R/leg2.log 2>&1
log "leg2 exit $?"
