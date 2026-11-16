#!/bin/bash
# #903 on dh610, restart at 15:57 UTC on main 423bd22d (the coordinator's order; the run on 1f3cda09 was stopped after 735 s, its log chain_stopped_1f3cda09.log): a chain at the fixed horizon order 140
# from the ladder's rung state (I903-mac/ladder/k140_from130/base_pin3_D225.1312.npz) toward the fold. Python and hp/data
# from a worktree of origin/main (423bd22d); hpkernel from #911's build (0cf9b94a, venv choptuik-large-d-911), by the
# coordinator's option (1): that build's existing paths reproduce main's bits (#911's checks), and the order-by-order
# functions it adds are not called by anm_run (--jet_by_order stays at its default 0). 10 threads, nice 10.
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-903
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I903-dh610
B=/home/nathan/scratch903
PY=/home/nathan/Source/choptuik-large-d-911/.venv/bin/python
S=I903-mac/ladder/k140_from130/base_pin3_D225.1312.npz
log() { echo "903 $1 $(date -u '+%F %T') UTC" >> $OUT/exits_903.txt; }
mkdir -p $B/$(dirname $S) $OUT
git -C "$SRC" fetch -q origin
if [ ! -d "$WT" ]; then
  { git -C "$SRC" fetch -q origin && git -C "$SRC" worktree add -q --detach "$WT" 423bd22d; } || { log "worktree failed"; exit 9; }
fi
git -C "$WT" checkout -q --detach 423bd22d || { log "checkout failed"; exit 9; }
[ -s $B/$S ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$S > $B/$S; } || { log "missing $S"; exit 9; }
$PY -I -c "import sys, numpy as np; z = np.load(sys.argv[1], allow_pickle=False); [z[k] for k in z.files]" $B/$S || { log "unreadable $S"; exit 9; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 423bd22d HEAD || { log "worktree older than 423bd22d"; exit 9; }
log "start, hp $(git rev-parse --short=8 HEAD), hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)"
t=$(date +%s)
PYTHONFAULTHANDLER=1 nice -n 10 $PY -u anm_run.py $B $OUT/chain_k140 --state $S --ks 140 --keep_plan 1 --kfreeze 3 \
  --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 400 --D_max 262 --threads 10 --corrector od \
  --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
  --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred \
  >> $OUT/chain.log 2>&1
rc=$?
log "anm_run exit $rc wall $(( $(date +%s) - t )) s"
exit $rc
