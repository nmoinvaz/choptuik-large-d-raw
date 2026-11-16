#!/bin/bash
# #910 on rpi5: the issue's two commands as written (sigdss_band.py profile at D 10.5, eta 0.3, kc 15, --maxjac 60 --settle 5,
# eleven Delta from 1.130 to 1.140), the sweeps at once with OPENBLAS_NUM_THREADS=2 each; the exit status of each against
# the required one (0) is appended to exits_910.txt. Only $PY, nice -n 10 and 2>&1 are added to the issue's text.
# Usage: bash run910.sh PY WT RAW  (the venv's python, a worktree at main 42a3e4b0 or later, the raw clone)
PY=$1; WT=$2; RAW=$3
R=$RAW/I910-rpi5
cd $WT/solver/matter || exit 9
git merge-base --is-ancestor 42a3e4b0 HEAD || { echo "STOP: the worktree is older than 42a3e4b0"; exit 9; }
log() { echo "910 $* $(date -u '+%F %T') UTC" >> $R/exits_910.txt; }
{ echo "commit $(git rev-parse --short=8 HEAD)"; $PY -c "import numpy, scipy, sys, platform; print('numpy', numpy.__version__, 'scipy', scipy.__version__, platform.platform(), 'python', sys.version.split()[0])"; } > $R/env.txt 2>&1
export OPENBLAS_NUM_THREADS=2
G="--D 10.5 --eps 3.33333333333 --kc 15 --maxjac 60 --settle 5"
t=$(date +%s)
log "fineA and fineB start"
nice -n 10 $PY -u sigdss_band.py profile $RAW/I907-winb/walk3_up_10.5.npy $G --deltas 1.130,1.131,1.132,1.133,1.134,1.135,1.136,1.137,1.138,1.139,1.140 --json $R/fineA.jsonl > $R/fineA.log 2>&1 &
pA=$!
nice -n 10 $PY -u sigdss_band.py profile $RAW/I897-winb/walk2_hi_10.5.npy $G --deltas 1.140,1.139,1.138,1.137,1.136,1.135,1.134,1.133,1.132,1.131,1.130 --json $R/fineB.jsonl > $R/fineB.log 2>&1 &
pB=$!
wait $pA; rcA=$?
log "fineA exit $rcA (required 0) wall $(( $(date +%s) - t )) s"
wait $pB; rcB=$?
log "fineB exit $rcB (required 0) wall $(( $(date +%s) - t )) s"
log done
