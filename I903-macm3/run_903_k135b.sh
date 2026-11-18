#!/bin/bash
# #903 (the coordinator's hc, 2026-11-18 10:5x UTC): restart of the order-135 chain with --qd_it 40 instead of 20, every other flag
# unchanged, from the last accepted base (D 258.24808321, chain_k135/anm_pin3_D258.2481.npz, step 48 of chain_k135) into chain_k135b.
# --a0 0.14901161193847656 is 1.25 x 0.11920928955078125, the a the chain would have tried next (step 48 was accepted at its first attempt
# at a 0.1192, --a_grow 1.25 with --a_hold 1); without it a restart starts at h_max 1.0. Code and venv as run_903_k135.sh (main 5897ee28,
# the 1f3cda09 hpkernel), nice 10 under caffeinate, 6 threads.
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I903-macm3
PY=$HOME/Source/venv-macm3-main/bin/python
export PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 6 --corrector od --tol_od 1e-60 --qd_it 40 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd $HOME/Source/choptuik-large-d-903m/hp || exit 9
log() { echo "903m $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_k135.txt; }
t=$(date +%s); log "chain_k135b start (qd_it 40, from chain_k135 base D 258.2481, a0 0.14901161193847656)"
caffeinate -is nice -n 10 $PY -u anm_run.py $RAW $O/chain_k135b --state I903-macm3/chain_k135/anm_pin3_D258.2481.npz $F --a0 0.14901161193847656 --ks 135 --keep_plan 1 --steps 400 --D_max 262 > $O/chain_k135b.log 2>&1
log "chain_k135b exit $? wall $(( $(date +%s) - t ))s"
