#!/bin/bash
# #842 on dh610 (the coordinator's command of 2026-11-16, my launcher): the arclength chain around the fold from
# I603-win2/chain_nsr/anm_pin3_D259.8875.npz, worktree choptuik-large-d-842 at main 44275d99 (hp/arclength.py, anm_run.py
# --arclength), run with #855's venv (hpkernel from the 7e4cfd03 build), 9 threads, nice 10; it stops by itself after the
# mirror's turn (--turns_max 2). Log chain.log in this folder.
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-842
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I842-dh610
B=/home/nathan/scratch842
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
S=I603-win2/chain_nsr/anm_pin3_D259.8875.npz
log() { echo "842 $1 $(date -u '+%F %T') UTC" >> $OUT/exits_842.txt; }
mkdir -p $B/$(dirname $S) $OUT
if [ ! -d "$WT" ]; then
  { git -C "$SRC" fetch -q origin && git -C "$SRC" worktree add -q --detach "$WT" 44275d99; } || { log "worktree failed"; exit 9; }
fi
[ -s $B/$S ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$S > $B/$S; } || { log "missing $S"; exit 9; }
$PY -I -c "import sys, numpy as np; z = np.load(sys.argv[1], allow_pickle=False); [z[k] for k in z.files]" $B/$S || { log "unreadable $S"; exit 9; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 44275d99 HEAD || { log "worktree older than 44275d99"; exit 9; }
log "start, hp $(git rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
t=$(date +%s)
PYTHONFAULTHANDLER=1 nice -n 10 $PY -u anm_run.py $B $OUT/chain --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 \
  --eps 1e-14 --h_max 1.0 --steps 400 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 \
  --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 \
  --reseed_start pred --save_jet 1 --arclength 1 --a0 0.00097 --arc_dhold 1e-12 --turns_max 2 >> $OUT/chain.log 2>&1
rc=$?
log "anm_run exit $rc wall $(( $(date +%s) - t )) s"
exit $rc
