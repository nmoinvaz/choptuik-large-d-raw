#!/bin/bash
# T85: two pinned scans to D = 200 side by side, 2 threads each, 6 h, below normal priority, under caffeinate.
cd ~/Source/choptuik-mac-qd2/hp || exit 1
T=~/Source/raw-T75
R=../../raw-T85
PY=~/venv-qd/bin/python
H=$(cat $R/history.txt)
COMMON="200 --kt 36 --kc 146 --ks 130 --kfreeze 13 --qdh 1 --corrector dnp --accept_stall 1e-19,1e-16 --tol 1e-19 \
  --tol_step 1e-32 --hmax 0.05 --dD 1.0 --dD0 1.0 --maxdD 1.0 --min_dD 1e-2 --max_fail_row 4 --it_max 30 --lm 15 \
  --predictor lagrange_dd --pin_from seed --pin_hist full1 --Dlist @$R/dlist.txt --max_hours 6 --threads 2 \
  --history $H --pin 7"
run() {   # tag nodes
  OPENBLAS_NUM_THREADS=1 caffeinate -is nice -n 10 $PY -u scan_hp.py $R/$1.jsonl $T/pin7_D73.2657.npz $COMMON \
    --nodes "$2" --tag pin7_$1 --attempts $R/$1_attempts.jsonl > $R/$1.log 2>&1
  echo "exit $?" >> $R/$1.log
}
run x80 0.3,0.4,0.5,0.6,0.7,0.8 &
run x85 0.3,0.4,0.5,0.6,0.7,0.85 &
wait
