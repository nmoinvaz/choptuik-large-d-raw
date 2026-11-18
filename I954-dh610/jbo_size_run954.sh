#!/bin/bash
# #954 ad hoc: the size of the planted-change difference on build A, at ST (order 6 differs in jet_by_order_check) and at ST2 (the control, which passed in #914), 8 threads, nice 10.
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954a
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH="$WT/hp"
for p in "$ST" "$ST2"; do
  tag=$([ "$p" = "$ST" ] && echo ST || echo ST2)
  nice -n 10 python $OUT/jbo_size954.py $R $p --threads $T --Np 6 > $OUT/A_jbo_size_$tag.log 2>&1; echo "exit $?" >> $OUT/A_jbo_size_$tag.log
done
echo "done $(stamp)" > $OUT/A_jbo_size_done.txt
