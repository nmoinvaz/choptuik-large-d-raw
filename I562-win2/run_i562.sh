#!/usr/bin/env bash
# #562 control arm: (1) renode crawlJ's D 242.3642 state to last node 0.975 (4 threads) and its sign control, then (2) near_null.py --keep_plan=1 (4 threads) and (3) the plain base polish (anm_run.py, crawlJ's options, --steps 0 --save_base 1,
# 8 threads, capped at 2 h) at the same time.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I562-win2
J=I461-win2/crawlJ/anm_pin3_D242.3642.npz
OUT=I562-win2/renode_0975_D242.3642.npz
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i562/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "80b5056" ] || { echo "D:/choptuik-i562 is not at 80b5056" >&2; exit 9; }
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt; }
log "renode_0975 start"
"$PY" -u renode_o.py $RAW $J $OUT --nodes 0.3,0.4,0.5,0.6,0.975 --threads 4 > $R/renode_0975.log 2>&1; rc=$?
log "renode_0975 exit $rc (check must pass)"
[ $rc -eq 0 ] || exit 8
log "renode_0975 mutate sign start"
"$PY" -u renode_o.py $RAW $J I562-win2/renode_0975_mut.npz --nodes 0.3,0.4,0.5,0.6,0.975 --threads 4 --mutate sign > $R/renode_0975_mut.log 2>&1; rc=$?
log "renode_0975 mutate sign exit $rc (must be nonzero)"
# (3) the plain polish in the background, (2) near_null in the foreground
log "polish start (anm_run.py --steps 0 --save_base 1, 8 threads, timeout 2 h)"
( timeout 7200 "$PY" -u anm_run.py $RAW $R/polish_0975 --state $OUT --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 0 --D_max 400 --threads 8 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 --save_base 1 > $R/polish_0975.log 2>&1; echo "polish exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt ) &
PPID2=$!
log "near_null start"
"$PY" -u near_null.py $RAW $OUT --keep_plan=1 --threads=4 --json=$R/nn_0975.json > $R/nn_0975.log 2>&1; rc=$?
log "near_null exit $rc"
wait $PPID2
log "run_i562 done"
