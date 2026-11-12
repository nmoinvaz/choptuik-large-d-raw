#!/usr/bin/env bash
# #562 control arm (3), forced: crawlJ's anm_run.py options with --steps 0 --save_base 1 and --tol 1e-30 (so that the start's double-double |F| 3.5e-29 exceeds --tol and the base polish runs), 8 threads, timeout 2 h.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I562-win2
OUT=I562-win2/renode_0975_D242.3642.npz
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i562/hp || exit 9
echo "polish_forced start $(date -u '+%Y-%m-%d %H:%M:%S UTC') (--tol 1e-30)" >> $R/exits.txt
timeout 7200 "$PY" -u anm_run.py $RAW $R/polish_forced --state $OUT --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --tol 1e-30 \
   --h_max 1.0 --steps 0 --D_max 400 --threads 8 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 --save_base 1 > $R/polish_forced.log 2>&1
echo "polish_forced exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
