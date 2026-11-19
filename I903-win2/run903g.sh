#!/usr/bin/env bash
# #903 second restart of ks_chain2 (coordinator's hc, 2026-11-19 ~00:15 UTC): run903f.sh unchanged except --reseed_qd_bar 1e-15 (the polish |R| of the accepted re-seeds rose to 5.7e-22 at D 241.68, so 1e-21 fails near D 242). Was: #903 restart of ks_chain2 (hc of 2026-11-18 ~22:15 UTC): run903e.sh's command on #962's build (venv-i962, D:/choptuik-i962/hp at main 290e9d04, which has anm_run.py --reseed_qd_bar),
# the same OUT I903-win2/ks_chain2 (ks_chain.py resumes from the highest-D state of its legs, D 238.1789 at ks 291), the same --mult 4.4 --pad -249, the same flags F (the old flags, 9 threads),
# plus --reseed_qd_bar 1e-15. Glue: it chains this one command and logs the exit in exits_903.txt.
# ks_chain.py's resume starts a new leg of length --leg (default 10) from the last state, which would be D 238.1789 -> 248.1789 at ks 305 (+14); the optional environment variable LEGARG
# (for example LEGARG="--leg 3.8211", which makes the leg end at D 242.0000 at ks 291) adds ks_chain.py's own --leg option and nothing else. usage: [LEGARG="--leg 3.8211"] bash run903f.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I903-win2
cd /d/choptuik-i962/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
log() { echo "903g $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_903.txt; }
log "ks_chain2 restart on venv-i962 (main $(git rev-parse --short=8 HEAD)), --mult 4.4 --pad -249 ${LEGARG:-(default --leg 10)} --reseed_qd_bar 1e-15, OUT I903-win2/ks_chain2, from the highest-D state of its legs"
t=$(date +%s)
"$PY" -u ks_chain.py D:/choptuik-large-d-raw D:/choptuik-large-d-raw/I903-win2/ks_chain2 --state I903-win2/start948/base_pin3_D232.0000.npz --D_stop 400 --mult 4.4 --pad -249 $LEGARG \
    -- $F --steps 400 --reseed_qd_bar 1e-15 >> $R/ks_chain2.log 2>&1
log "ks_chain2 (restart) exit $? wall $(( $(date +%s) - t ))s"
