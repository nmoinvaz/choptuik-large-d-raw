#!/bin/bash
# T101: one jump from T85's layout-A frontier (77.8806) to D = 100, the cubic predictor through T85's waypoints 74..77.
cd ~/Source/choptuik-mac-qd2/hp || exit 1
R=/Users/nathan/Source/choptuik-large-d-raw/T101-mac
T=/Users/nathan/Source/choptuik-large-d-raw/T85-mac
PY=~/venv-qd/bin/python
H=$T/pin7_x80_D74.0000.npz,$T/pin7_x80_D75.0000.npz,$T/pin7_x80_D76.0000.npz,$T/pin7_x80_D77.0000.npz
OPENBLAS_NUM_THREADS=1 nice -n 10 $PY -u scan_hp.py $R/jump100.jsonl $T/pin7_x80_D77.8806.npz 100 \
  --kt 36 --kc 232 --ks 130 --kfreeze 13 --qdh 1 --corrector dnp --accept_stall 1e-19,1e-16 --tol 1e-19 \
  --tol_growth 1.45 --tol_step 1e-32 --hmax 0.05 --dD 22.1194 --dD0 22.1194 --maxdD 22.1194 --min_dD 1e-4 \
  --max_fail_row 1 --it_max 30 --lm 15 --predictor lagrange_dd --pin_from seed --pin_hist full1 --threads 4 \
  --history $H --pin 7 --nodes 0.3,0.4,0.5,0.6,0.7,0.8 --tag jump100_x80 --verbose \
  --attempts $R/jump100_attempts.jsonl --allow_unraw > $R/jump100.log 2>&1
echo "exit $?" >> $R/jump100.log
