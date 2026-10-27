#!/bin/bash
# T84 jump ladder: one step of J from T75's pin 7 frontier (73.2657) in the x85 layout, the cubic predictor through
# T75's waypoints near 70.65, 71.5 and 72.4 and the frontier (spacing about 0.87), the pinned Newton as T75/T80.
# One attempt per J (--max_fail_row 1), 4 threads, sequential, below normal priority.
cd ~/Source/choptuik-mac-qd2/hp || exit 1
T=~/Source/raw-T75
R=../../raw-T84
PY=~/venv-qd/bin/python
H=$(cat $R/history.txt)
for J in 0.5 1.0 2.0 5.0; do
  E=$($PY -c "print(round(73.265722 + $J, 6))")
  OPENBLAS_NUM_THREADS=1 caffeinate -is nice -n 10 $PY -u scan_hp.py $R/jump$J.jsonl $T/pin7_D73.2657.npz $E \
    --kt 36 --kc 146 --ks 130 --kfreeze 13 --qdh 1 --corrector dnp --accept_stall 1e-19,1e-16 --tol_growth 1.45 \
    --tol_step 1e-32 --hmax 0.05 --dD $J --dD0 $J --maxdD $J --min_dD 1e-4 --max_fail_row 1 --it_max 30 --lm 15 \
    --predictor lagrange_dd --pin_from seed --pin_hist full1 --threads 4 --tol 1.093e-20 --history $H --pin 7 \
    --nodes 0.3,0.4,0.5,0.6,0.7,0.85 --tag jump$J --verbose --attempts $R/jump${J}_attempts.jsonl > $R/jump$J.log 2>&1
  echo "exit $?" >> $R/jump$J.log
done
