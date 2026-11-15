#!/usr/bin/env bash
# #343 on win2: the corrected low-D leg (notes/LOW_D.md 16, procedure fixed before the run). lowD_highM.py from T105's
# converged pair at D 3.04375 (M 320 and 384), steps of 0.0004 to D 3.040, Newton at every D at both resolutions,
# 10 threads beside #603, worktree D:/choptuik-i343 at main, venv-i600. Resumable: rerun with --resume after a stop.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I343-win2
cd /d/choptuik-i343/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "343 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_343.txt; }
log "start, main $(git rev-parse --short=8 HEAD) $*"
"$PY" -u lowD_highM.py --start_w $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M320.npz \
    --start_n $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M384.npz --Ms 320,384 --dD 0.0004 --D_end 3.040 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 8 --threads 10 --tag lowD343 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl "$@" >> $R/leg.log 2>&1
log "leg exit $?"
