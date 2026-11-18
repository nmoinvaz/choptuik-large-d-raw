#!/bin/bash
# #954 ad hoc: jet_by_order_check's own sequence at ST on build A with the detail of the differing words (jbo_nan954.py), 8 threads, nice 10.
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954a
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH="$WT/hp"
nice -n 10 python $OUT/jbo_nan954.py $R $ST --threads $T --N 6 --Np 6 > $OUT/A_jbo_nan_ST.log 2>&1; echo "exit $?" >> $OUT/A_jbo_nan_ST.log
echo "done $(stamp)" > $OUT/A_jbo_nan_done.txt
