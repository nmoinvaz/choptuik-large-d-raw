#!/bin/bash
# T101 ladders: the scan's own halving toward D = 100 (see README, amendment of 2026-11-02 22:52 UTC).
cd ~/Source/choptuik-mac-qd2/hp || exit 1
R=/Users/nathan/Source/choptuik-large-d-raw/T101-mac
T75=/Users/nathan/Source/choptuik-large-d-raw/T75
T85=/Users/nathan/Source/choptuik-large-d-raw/T85-mac
PY=~/venv-qd/bin/python
COMMON="100 --kt 36 --kfreeze 13 --qdh 1 --corrector dnp --accept_stall 1e-19,1e-16 --tol_growth 1.45 --tol_step 1e-32 \
  --hmax 0.05 --fail_factor 0.5 --grow 2 --min_dD 0.25 --max_fail_row 12 --max_hours 0.13 --it_max 30 --lm 15 \
  --predictor lagrange_dd --pin_from seed --pin_hist full1 --threads 4 --pin 7 --verbose --allow_unraw"
H85=$T75/pin7_D70.6500.npz,$T75/pin7_D71.5000.npz,$T75/pin7_D72.4000.npz
H80=$T85/pin7_x80_D74.0000.npz,$T85/pin7_x80_D75.0000.npz,$T85/pin7_x80_D76.0000.npz,$T85/pin7_x80_D77.0000.npz
OPENBLAS_NUM_THREADS=1 nice -n 10 $PY -u scan_hp.py $R/ladder_x85.jsonl $T75/pin7_D73.2657.npz $COMMON --kc 146 --ks 130 \
  --tol 1.093e-20 --dD 26.734278 --dD0 26.734278 --maxdD 26.734278 --history $H85 --nodes 0.3,0.4,0.5,0.6,0.7,0.85 \
  --tag ladder_x85 --attempts $R/ladder_x85_attempts.jsonl > $R/ladder_x85.log 2>&1 &
OPENBLAS_NUM_THREADS=1 nice -n 10 $PY -u scan_hp.py $R/ladder_x80.jsonl $T85/pin7_x80_D77.8806.npz $COMMON --kc 232 --ks 130 \
  --tol 1e-19 --dD 22.1194 --dD0 22.1194 --maxdD 22.1194 --history $H80 --nodes 0.3,0.4,0.5,0.6,0.7,0.8 \
  --tag ladder_x80 --attempts $R/ladder_x80_attempts.jsonl > $R/ladder_x80.log 2>&1 &
wait
