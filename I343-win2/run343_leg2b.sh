#!/usr/bin/env bash
# #343 leg 2, restart after the stop at the coordinator's order (hc, 2026-11-16 ~23:00 UTC): D 3.04315 stalled at |F| 1.4e-2 from a
# NaN predictor and the fallback start, so the progress file's targets got 3.04325 inserted at the front by hand (the file's .bak is the
# state before; the code's own halving does targets.insert(0, Dm) with Dm = round(0.5 * (Dl + Dt), 6)). This script only runs the
# last line of run343_leg2.sh exactly, with --resume as there and --it_max 8 added, the coordinator's one change (a stalled pass then
# fails after 8 Newton steps and the code halves the step itself). Same worktree (D:/choptuik-i343 at e186ae7a), venv and 10 threads.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I343-win2
cd /d/choptuik-i343/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "343 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_343.txt; }
log "leg2b start (after the stop), main $(git rev-parse --short=8 HEAD), --it_max 8, targets from the progress file start with 3.04325"
"$PY" -u lowD_highM.py --start_w $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M320.npz \
    --start_n $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M384.npz --Ms 320,384 --dD 0.0004 --D_end 3.040 \
    --min_step 0.00005 --diff_max 1e-8 --hours 120 --point_hours 30 --threads 10 --tag lowD343 \
    --states $R/states --out $R/leg2.jsonl --points $R/leg2_points.jsonl --resume --it_max 8 >> $R/leg2.log 2>&1
log "leg2b exit $?"
