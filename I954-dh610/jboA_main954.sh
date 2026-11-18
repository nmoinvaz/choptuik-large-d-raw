#!/bin/bash
# #954 (hc, 2026-11-17): one rerun of A's jet_by_order line with main's script (9bff3a1e: finite words bit for bit, non-finite ones by place), 8 threads, nice 10.
# The pipeline's scope is frozen while this runs and thawed at the end.
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954a
SC=run-p550370-i581817.scope
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH="$WT/hp"
systemctl --user freeze $SC && echo "pipeline scope frozen $(stamp) for A_jet_by_order_main" >> $OUT/pipeline.txt
trap 'systemctl --user thaw $SC; echo "pipeline THAWED $(stamp)" >> $OUT/pipeline.txt' EXIT
{ echo "# $(stamp) UTC build A, hp $(git -C $WT rev-parse --short HEAD), script jet_by_order_check_main.py = origin/main 9bff3a1e"
  echo "# cmd: python jet_by_order_check_main.py $R $ST --threads $T --N 6 --out $OUT/A_jbo_main"; } > $OUT/A_jbo_main.log
s=$(date +%s)
nice -n 10 python $OUT/jet_by_order_check_main.py $R $ST --threads $T --N 6 --out $OUT/A_jbo_main >> $OUT/A_jbo_main.log 2>&1; rc=$?
echo "exit $rc, $(( $(date +%s) - s )) s" >> $OUT/A_jbo_main.log
echo "A_jbo_main exit $rc $(stamp)" > $OUT/A_jbo_main_done.txt
