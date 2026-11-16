#!/usr/bin/env bash
# #903, the chain (coordinator's comment, 2026-11-16 05:08 UTC): hp/ks_chain.py (main 54245002, cherry-picked as 3b60968f) from p160's
# s160 state at D 152, the horizon order tied to D, with the pilot's F unchanged. It only runs the coordinator's command and logs its exit.
# usage: bash run_ks_chain.sh D_STOP     (400, or 240 if p410 did not converge). Appends to ks_chain.log, so a start with the same
# OUT resumes from the highest-D state of its legs. Worktree D:/choptuik-i603r, venv-i600, 9 threads.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I903-win2
S=I903-win2/s160/anm_pin3_D152.0000.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
: "${1:?D_stop: 400, or 240 if p410 did not converge}"
cd /d/choptuik-i603r/hp || exit 9
export PYTHONFAULTHANDLER=1
log() { echo "903c $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_903.txt; }
[ -f $RAW/$S ] || { log "missing $S"; exit 9; }
log "ks_chain start, main $(git rev-parse --short HEAD), D_stop $1"
t=$(date +%s)
"$PY" -u ks_chain.py $RAW $R/ks_chain --state $S --D_stop $1 -- $F --steps 400 >> $R/ks_chain.log 2>&1
rc=$?
log "ks_chain exit $rc wall $(( $(date +%s) - t ))s"
