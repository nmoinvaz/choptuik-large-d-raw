#!/bin/bash
# T84 pilot: two layouts side by side, 2 threads each, 1 h, below normal priority, under caffeinate.
cd ~/Source/choptuik-mac-qd2/hp || exit 1
T=~/Source/raw-T75
R=../../raw-T84
PY=~/venv-qd/bin/python
COMMON="200 --kt 36 --kc 146 --ks 130 --kfreeze 13 --qdh 1 --corrector dnp --accept_stall 1e-19,1e-16 \
  --tol_growth 1.45 --tol_step 1e-32 --hmax 0.05 --dD 0.005 --min_dD 1e-4 --max_fail_row 4 --it_max 30 \
  --predictor lagrange_dd --pin_from seed --pin_hist full1 --Dlist @$R/dlist.txt --max_hours 1 --threads 2 \
  --tol 1.093e-20 --history $T/pin7_D73.2608.npz,$T/pin7_D73.2622.npz,$T/pin7_D73.2640.npz --pin 7"
run() {   # tag nodes
  OPENBLAS_NUM_THREADS=1 caffeinate -is nice -n 10 $PY -u scan_hp.py $R/$1.jsonl $T/pin7_D73.2657.npz $COMMON \
    --nodes "$2" --tag pin7_$1 --attempts $R/$1_attempts.jsonl > $R/$1.log 2>&1
  echo "exit $?" >> $R/$1.log
}
run x85 0.3,0.4,0.5,0.6,0.7,0.85 &
run x80 0.3,0.4,0.5,0.6,0.7,0.8 &
wait
