#!/bin/bash
# #826 arm B (the coordinator): as arm A, plus --full_drop 1e-3, which accepts a full step whose max|F| falls to 1e-3 of
# the start's; arm A's acceptance tests refused such steps because the Newton correction is noise at ~3e-8 (#827). Newton from s0_D252's planted truth itself (--rel 0) at the default projection switch
# (1e-15; the truth's residual 3.58e-20 lies below it, so the start is not projected), #777's rerun flags otherwise,
# --it_max 12, 4 threads. Bar: pinned max|F| below 1e-40 within 12 steps. The first step must reproduce #823's
# dDelta +3.311085e-8 to 1e-12 relative. Worktree choptuik-large-d-817 (main 390d1db9), the main checkout's .venv.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I826-dh610
B=/home/nathan/scratch817
WT=/home/nathan/Source/choptuik-large-d-817
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
S252=I603-win2/chain/anm_pin3_D252.6135.npz
mkdir -p $R
log() { echo "826 $1 $(date -u '+%F %T') UTC" >> $R/exits_826.txt; }
cd $WT/hp || exit 9
[ -s $B/$S252 ] || { log "missing $B/$S252"; exit 9; }
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
log "truth_drop start, hp $(git rev-parse --short=8 HEAD)"
nice -n 10 $PY -u octo_corrector.py planted $B $S252 --threads 4 --reseed_o 3 --reseed_start pred --qd 0 \
  --rel 0 --it_max 12 --full_drop 1e-3 --out $R/truth_drop > $R/truth_drop.log 2>&1
log "truth_drop exit $?"
