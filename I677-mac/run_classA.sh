#!/bin/bash
# I677-mac: #603's class A attempt (D 248.6298 -> 249.39, a 0.762939453125) made again with --save_dz0 1, on #603's
# flags (I603-win2/run_603.sh, I644-win2/run_644.sh) but 2 threads. Run from the checkout's hp/ as
#   bash run_classA.sh RAW
# with PYTHONPATH at main 3c35f0c's hpkernel build. It is stopped by hand after the attempt's first Newton step line.
RAW=$1
PY=${PY:-/Users/nathan/venv-314/bin/python3}
R=$RAW/I677-mac
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
echo "classA start $(date -u '+%Y-%m-%dT%H:%M:%SZ') $(git rev-parse --short=8 HEAD)" >> $R/exits.txt
nice -n 10 "$PY" -u anm_run.py $RAW $R/classA --state I603-win2/chain/anm_pin3_D248.6298.npz --kfreeze 3 \
  --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 2 --corrector od \
  --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
  --held_o 1 --reseed_o 3 --save_pred 1 --save_dz0 1 --a0 0.762939453125 --od_accept own > $R/classA.log 2>&1
echo "classA exit $? $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> $R/exits.txt
