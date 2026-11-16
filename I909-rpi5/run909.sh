#!/bin/bash
# #909 on rpi5: the issue's three commands as written (sigdss_band.py profile at D 10.5, eta 0.3, kc 15), the two sweeps at
# once with OPENBLAS_NUM_THREADS=2 each, then the dfree control; the exit status of each against the required one is
# appended to exits_909.txt. Only $PY, nice -n 10 and the redirections of stderr are added to the issue's text.
# Usage: bash run909.sh PY WT RAW  (the venv's python, a worktree at main 42a3e4b0 or later, the raw clone)
PY=$1; WT=$2; RAW=$3
R=$RAW/I909-rpi5
cd $WT/solver/matter || exit 9
git merge-base --is-ancestor 42a3e4b0 HEAD || { echo "STOP: the worktree is older than 42a3e4b0"; exit 9; }
log() { echo "909 $* $(date -u '+%F %T') UTC" >> $R/exits_909.txt; }
{ echo "commit $(git rev-parse --short=8 HEAD)"; $PY -c "import numpy, scipy, sys, platform; print('numpy', numpy.__version__, 'scipy', scipy.__version__, platform.platform(), 'python', sys.version.split()[0])"; } > $R/env.txt 2>&1
export OPENBLAS_NUM_THREADS=2
G="--D 10.5 --eps 3.33333333333 --kc 15 --maxjac 30 --settle 3"
t=$(date +%s)
log "sweepA and sweepB start"
nice -n 10 $PY -u sigdss_band.py profile $RAW/I907-winb/walk3_up_10.5.npy $G --deltas 1.120,1.122,1.124,1.126,1.128,1.130,1.132,1.134,1.136,1.138,1.140,1.142 --json $R/profile.jsonl > $R/sweepA.log 2>&1 &
pA=$!
nice -n 10 $PY -u sigdss_band.py profile $RAW/I897-winb/walk2_hi_10.5.npy $G --deltas 1.142,1.140,1.138,1.136,1.134,1.132,1.130,1.128,1.126,1.124,1.122,1.120 --json $R/profileB.jsonl > $R/sweepB.log 2>&1 &
pB=$!
wait $pA; rcA=$?
log "sweepA exit $rcA (required 0) wall $(( $(date +%s) - t )) s"
wait $pB; rcB=$?
log "sweepB exit $rcB (required 0) wall $(( $(date +%s) - t )) s"
t=$(date +%s)
nice -n 10 $PY -u sigdss_band.py profile $RAW/I907-winb/walk3_up_10.5.npy $G --maxjac 2 --deltas 1.128 --mutate dfree > $R/control_dfree.log 2>&1
rc=$?
log "control_dfree exit $rc (required 1) wall $(( $(date +%s) - t )) s"
log done
