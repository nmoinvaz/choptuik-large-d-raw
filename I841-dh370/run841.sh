#!/bin/bash
# #841 on dh370 (the coordinator): a chain on a new plan, from #808's converged re-planned state at D 251.8859 (its own
# stored plan, kept), #603's flags plus the residual-drop acceptance (#836) and the iteration-1..2 refusal (#784), the
# series saved (--save_jet 1) for #829's approximants near the fold. 12 threads. Worktree 808b updated to main.
#   bash run841.sh pilot   two steps, then stop: each must converge to max|F| <= 1e-60
#   bash run841.sh chain   from the pilot's last state on to --D_max 259.95
SELF=$(realpath "$0")
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I841-dh370
B=/home/nathan/scratch841
WT=/home/nathan/Source/choptuik-large-d-841
PY=/home/nathan/Source/venv-i800/bin/python
S0=I808-dh370/s251.8859_plandrop/base_pin3_D251.8859.npz
mkdir -p $R $B/$(dirname $S0)
log() { echo "841 $1 $(date -u '+%F %T') UTC" >> $R/exits_841.txt; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 2e315411 HEAD || { log "worktree older than 2e315411"; exit 9; }
[ -s $B/$S0 ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$S0 > $B/$S0; } || { log "missing $S0"; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --D_max 259.95 --threads 12 --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred --save_jet 1 --od_full_drop 1e-2 --od_abort_theta 1e8 --od_abort_it 2"
case $1 in
  pilot)
    log "pilot start, hp $(git rev-parse --short=8 HEAD)"
    nice -n 10 $PY -u anm_run.py $B $R/chain --state $S0 $FLAGS --steps 2 >> $R/chain.log 2>&1
    log "pilot exit $?" ;;
  chain)
    last=$(ls $R/chain/anm_pin3_D*.npz 2>/dev/null | sort -t D -k2 -g | tail -1)
    [ -n "$last" ] || { log "no pilot state"; exit 9; }
    log "chain start from $last, hp $(git rev-parse --short=8 HEAD)"
    nice -n 10 $PY -u anm_run.py / $R/chain --state $last $FLAGS --steps 400 >> $R/chain.log 2>&1
    log "chain exit $?" ;;
  *) echo "usage: run841.sh pilot|chain"; exit 2 ;;
esac
