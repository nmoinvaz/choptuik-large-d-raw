#!/usr/bin/env bash
# #933, the sonic valley's closing at M 384 (coordinator's hc, 2026-11-17 ~03:45 UTC). It only chains the coordinator's four commands
# and logs each exit; the two controls are expected to exit 1, and a non-zero exit of the first or third command stops the chain.
# Worktree D:/choptuik-i932 at origin/main 65ec482f, venv-i600, 1 thread. usage: bash run933.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I933-win2
S82=$RAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0450_M384.npz
S105=$RAW/T105-win2/states/lowDhm_x0.000157-0.975_D3.0438_M384.npz
S36=$RAW/I343-win2/states/lowD343_D3.0436_M384.npz
S335=$RAW/I343-win2/states/lowD343_D3.043350_M384.npz
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "933 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_933.txt; }
run() { n=$1; shift; t=$(date +%s); log "$n start"; "$PY" -u sonic_valley.py "$@" > $R/$n.log 2>&1; rc=$?; log "$n exit $rc wall $(( $(date +%s) - t ))s"; return $rc; }
for f in $S82 $S105 $S36 $S335; do [ -f $f ] || { log "missing $f"; exit 9; }; done
log "start, worktree $(git rev-parse --short=8 HEAD)"
run gap gap $R/gap_M384.jsonl $S82 $S105 $S36 $S335 --plan stored --threads 1 || { log "gap failed, chain stopped"; exit 1; }
run gap_dshift gap $R/gap_dshift.jsonl $S335 --plan stored --threads 1 --mutate dshift
run tangency tangency $R/gap_M384.jsonl --M 384 --last 3 || { log "tangency failed, control not run"; exit 1; }
run tangency_slope tangency $R/gap_M384.jsonl --M 384 --last 3 --mutate slope
log "done"
