#!/bin/bash
# #834 pilot on dh370 (the coordinator): does a re-planned polish converge near the fold with the residual-drop rule?
# Two of #603's chain_nsr states, D 259.4928 and 259.7436, polished at their own D (--steps 0) on a plan made at the
# state (--keep_plan 0), #603's own held values (held_fit.json), #603's flags, plus --od_full_drop 1e-2 (#836). Side by
# side at 6 threads each. Bar for #834 to go ahead: both converge to max|F| <= 1e-60. Worktree 808b (main bd4ada6c or
# later), venv-i800. #808's plandrop (with 1e-6) converged 1 of 5 such polishes at D 240-253.5.
SELF=$(realpath "$0")
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I834-dh370
B=/home/nathan/scratch834
WT=/home/nathan/Source/choptuik-large-d-808b
PY=/home/nathan/Source/venv-i800/bin/python
mkdir -p $R $B/I603-win2/chain_nsr
log() { echo "834 $1 $(date -u '+%F %T') UTC" >> $R/exits_834.txt; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 38744bb3 HEAD || { log "worktree older than 38744bb3"; exit 9; }
for D in 259.4928 259.7436; do
  f=I603-win2/chain_nsr/anm_pin3_D$D.npz
  [ -s $B/$f ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$f > $B/$f; } || { log "missing $f"; exit 9; }
done
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
pol() {  # D
  log "s$1 start, hp $(git rev-parse --short=8 HEAD)"
  nice -n 10 $PY -u anm_run.py $RAW $R/s$1 --state $B/I603-win2/chain_nsr/anm_pin3_D$1.npz --kfreeze 3 \
    --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 6 --corrector od --tol_od 1e-60 \
    --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 \
    --reseed_o 3 --save_base 1 --keep_plan 0 --od_full_drop 1e-2 > $R/s$1.log 2>&1
  log "s$1 exit $?"
}
pol 259.4928 &
pol 259.7436 &
wait
log "pilot done"
