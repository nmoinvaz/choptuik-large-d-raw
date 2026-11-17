#!/usr/bin/env bash
# #932, the field-shaped planted move (coordinator's hc, 2026-11-17 ~04:35 UTC, main 80b944ff's planplant --shape field): step 0's
# command with --shape field --threads 1, then its control (--mutate norefine, must exit 1). It only chains those two commands and logs
# each exit, on the one thread free beside the control or step 2 (10 threads) and the #903 chain (9). Worktree D:/choptuik-i932 at
# origin/main 80b944ff (pulled while the control was running; lowD_highM.py is unchanged by it and sonic_valley.py differs only in planplant).
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I932-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "932d $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_932.txt; }
run() { n=$1; shift; t=$(date +%s); log "$n start"; "$PY" -u sonic_valley.py "$@" > $R/$n.log 2>&1; rc=$?; echo "exit $rc" >> $R/$n.log; log "$n exit $rc wall $(( $(date +%s) - t ))s"; return $rc; }
T=$RAW/I343-win2/states/lowD343_D3.043350_M320.npz
C=$RAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M320.npz
log "field-shaped planplant start, worktree $(git rev-parse --short=8 HEAD)"
run planplant_field planplant $R/planplant_field.jsonl $T $C --refine 4 --levels 2 --delta 1e-8 --shape field --threads 1
run planplant_field_control planplant $R/planplant_field_control.jsonl $T $C --refine 4 --levels 2 --delta 1e-8 --shape field --threads 1 --mutate norefine
log "field-shaped planplant done"
