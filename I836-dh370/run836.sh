#!/bin/bash
# #836 on dh370 (the coordinator): #608's d6 attempt from D 252.6966 at a = 0.08881784197001252 (side A refused it at
# iteration 3, #608's log), rerun with #608's restart flags plus --od_full_drop 1e-2, --steps 1, 12 threads. Worktree
# choptuik-large-d-808b (main bd4ada6c), venv-i800. Bar: a = 0.0888 accepted, max|F| <= 1e-60 within 20 steps.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I836-dh370
B=/home/nathan/scratch836
WT=/home/nathan/Source/choptuik-large-d-808b
PY=/home/nathan/Source/venv-i800/bin/python
S=I608-dh610/restart2_d6/anm_pin3_D252.6966.npz
mkdir -p $R $B/$(dirname $S)
log() { echo "836 $1 $(date -u '+%F %T') UTC" >> $R/exits_836.txt; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 38744bb3 HEAD || { log "worktree older than 38744bb3"; exit 9; }
[ -s $B/$S ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$S > $B/$S; } || { log "missing $S"; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
log "drop start, hp $(git rev-parse --short=8 HEAD)"
nice -n 10 $PY -u anm_run.py $B $R/drop --state $S --kfreeze 3 --held_fit data/held_fit_d6.json --N 24 \
  --eps 1e-14 --h_max 1.0 --steps 1 --D_max 254 --threads 12 --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 \
  --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 \
  --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred \
  --a0 0.08881784197001252 --od_full_drop 1e-2 > $R/drop.log 2>&1
log "drop exit $?"
