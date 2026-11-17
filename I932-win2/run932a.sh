#!/usr/bin/env bash
# #932 steps 0 and 1 (coordinator's hc 2026-11-17 ~03:45 UTC and the file I926-mac/runner_task_M320.md, with main in place of wip/sa-926,
# folder I932-win2, 10 threads). It only chains the file's commands and logs each exit: the planted check of the gate (must exit 0),
# its control (--mutate norefine, must exit 1), then the starts. A failed planted check stops the chain, as a failed check does.
# Worktree D:/choptuik-i932 at origin/main 65ec482f, venv-i600. usage: bash run932a.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I932-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "932a $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_932.txt; }
run() { n=$1; shift; t=$(date +%s); log "$n start"; "$PY" -u sonic_valley.py "$@" > $R/$n.log 2>&1; rc=$?; echo "exit $rc" >> $R/$n.log; log "$n exit $rc wall $(( $(date +%s) - t ))s"; return $rc; }
T=$RAW/I343-win2/states/lowD343_D3.043350_M320.npz
C=$RAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M320.npz
for f in $T $C; do [ -f $f ] || { log "missing $f"; exit 9; }; done
log "start, worktree $(git rev-parse --short=8 HEAD)"
run planplant planplant $R/planplant.jsonl $T $C --refine 4 --levels 2 --delta 1e-8 --threads 10
rc0=$?
run planplant_control planplant $R/planplant_control.jsonl $T $C --refine 4 --levels 2 --delta 1e-8 --threads 10 --mutate norefine
rc1=$?
[ $rc0 -eq 0 ] && [ $rc1 -eq 1 ] || { log "step 0 failed (planplant $rc0, control $rc1), chain stopped"; exit 1; }
run startcase startcase $R/startcase.jsonl \
    $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M320.npz \
    $RAW/I343-win2/states/lowD343_D3.0436_M320.npz $T \
    --predict 3.04315 --plan own --tol_step 1e-32 --refine 4 --levels 2 --threads 10 || { log "startcase failed, chain stopped"; exit 1; }
log "steps 0 and 1 done"
