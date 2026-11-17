#!/usr/bin/env bash
# #932 after the failed step 0 (coordinator's hc, 2026-11-17 ~04:05 UTC): the diagnostic, the same planplant command as step 0 with
# --delta 1e-10 and then --delta 1e-12 (it measures whether the moved truth becomes finite at split 4 or 16, it does not redefine
# step 0's pass), then step 1 (startcase) as written. It only chains those commands and logs each exit; a diagnostic's exit 1 does not stop it.
# Worktree D:/choptuik-i932 at origin/main 65ec482f, venv-i600, 10 threads. usage: bash run932c.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I932-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "932c $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_932.txt; }
run() { n=$1; shift; t=$(date +%s); log "$n start"; "$PY" -u sonic_valley.py "$@" > $R/$n.log 2>&1; rc=$?; echo "exit $rc" >> $R/$n.log; log "$n exit $rc wall $(( $(date +%s) - t ))s"; return $rc; }
T=$RAW/I343-win2/states/lowD343_D3.043350_M320.npz
C=$RAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M320.npz
log "diagnostic and step 1 start, worktree $(git rev-parse --short=8 HEAD)"
run planplant_d1e-10 planplant $R/planplant_d1e-10.jsonl $T $C --refine 4 --levels 2 --delta 1e-10 --threads 10
run planplant_d1e-12 planplant $R/planplant_d1e-12.jsonl $T $C --refine 4 --levels 2 --delta 1e-12 --threads 10
run startcase startcase $R/startcase.jsonl \
    $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M320.npz \
    $RAW/I343-win2/states/lowD343_D3.0436_M320.npz $T \
    --predict 3.04315 --plan own --tol_step 1e-32 --refine 4 --levels 2 --threads 10
log "diagnostic and step 1 done"
