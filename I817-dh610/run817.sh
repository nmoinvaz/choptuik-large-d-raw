#!/bin/bash
# #817 on dh610 (the coordinator): the strong-row chord at #713's planted start s0_D252 (I603-win2's state at D 252.6135,
# #713's two-seed test, seed 1), octo_corrector.py planted with #777's rerun flags plus --strong 4, without and with
# --full_drop 1e-6, side by side at 2 threads each (dh610's 4 threads beside #608's chains). Judged against #816's root
# (mac752) when it ends: pinned max|F| below 1e-40 within 12 steps, Delta within 1e-30 of that root.
# Worktree choptuik-large-d-817 at main (165b1da3 or later), the main checkout's .venv (#606's build, after #523).
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I817-dh610
B=/home/nathan/scratch817
WT=/home/nathan/Source/choptuik-large-d-817
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
S252=I603-win2/chain/anm_pin3_D252.6135.npz
mkdir -p $R $B/$(dirname $S252)
log() { echo "817 $1 $(date -u '+%F %T') UTC" >> $R/exits_817.txt; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 165b1da3 HEAD || { log "worktree older than 165b1da3"; exit 9; }
[ -s $B/$S252 ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$S252 > $B/$S252; } || { log "missing $S252"; exit 9; }
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
arm() {  # name extra...
  local name=$1; shift
  log "$name start, hp $(git rev-parse --short=8 HEAD)"
  nice -n 10 $PY -u octo_corrector.py planted $B $S252 --threads 2 --switch 0 --reseed_o 3 --reseed_start pred --qd 0 \
    --strong 4 "$@" --out $R/$name > $R/$name.log 2>&1
  log "$name exit $?"
}
arm strong4 &
arm strong4_drop --full_drop 1e-6 &
wait
log "all done"
