#!/usr/bin/env bash
# #343 leg 2 on win2 (the coordinator): the leg continued after the first run's rule stop. lowD_highM_leg.py copies its
# progress file to leg2.jsonl.progress.json with the stop cleared and the targets below. lowD_highM.py then resumes with
# wider time limits (--point_hours 30, --hours 120), because D 3.04335's pass 1 alone took more than the old 8 h. Same
# worktree, venv and arguments as run343.sh otherwise. Run it only after leg.log shows the stop. 10 threads. The
# history states are searched in I343-win2/states and in T105-win2/states, where the first run's start pair lives.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I343-win2
cd /d/choptuik-i343/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "343 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_343.txt; }
"$PY" -c "import json, sys; sys.exit(0 if json.load(open(sys.argv[1])).get('done') else 1)" $R/leg.jsonl.progress.json \
    || { log "leg2: the first run has not stopped (its progress file's done is empty)"; exit 9; }
# targets from the run's last converged D in steps of 2e-4 down to 3.040: 4e-4 failed at M 384 from 3.04375 (#343)
TARGETS=$("$PY" -c "import json, sys; d = json.load(open(sys.argv[1]))['hist_n'][-1][0]; n = int(round((d - 3.040) / 2e-4)); print(','.join('%.5f' % (d - 2e-4 * k) for k in range(1, n + 1)))" $R/leg.jsonl.progress.json)
[ -n "$TARGETS" ] || { log "leg2: no targets from the progress file"; exit 9; }
log "leg2 targets $TARGETS"
# both folders as Windows paths: Git Bash converts a lone path argument, not the second one of a comma-separated list
STATES="$(cygpath -m "$R/states"),$(cygpath -m "$RAW/T105-win2/states")" || { log "leg2: cygpath failed"; exit 9; }
log "leg2 states $STATES"
"$PY" -u lowD_highM_leg.py $R/leg.jsonl.progress.json $R/leg2.jsonl \
    --targets $TARGETS --states "$STATES" >> $R/leg2.log 2>&1 \
    || { log "leg2: lowD_highM_leg.py exit $?"; exit 9; }
log "leg2 start, main $(git rev-parse --short=8 HEAD)"
"$PY" -u lowD_highM.py --start_w $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M320.npz \
    --start_n $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M384.npz --Ms 320,384 --dD 0.0004 --D_end 3.040 \
    --min_step 0.00005 --diff_max 1e-8 --hours 120 --point_hours 30 --threads 10 --tag lowD343 \
    --states $R/states --out $R/leg2.jsonl --points $R/leg2_points.jsonl --resume >> $R/leg2.log 2>&1
log "leg2 exit $?"
