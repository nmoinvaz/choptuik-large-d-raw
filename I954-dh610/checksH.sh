#!/bin/bash
# #954 build A against build C timing, A, C, A, C at 8 threads, nice 10 (checksC's timing lines failed: timing954.py is in this folder, not in the worktrees' hp; the path was mine).
# The pipeline's scope (checksD's planted run) is frozen meanwhile and thawed at the end.
. "$(dirname "$0")/common954.sh"
WTA=/home/nathan/Source/choptuik-large-d-954a; WTC=/home/nathan/Source/choptuik-large-d-954c
SUM=$OUT/summary_C.txt
SC=run-p550370-i581817.scope
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
systemctl --user freeze $SC && echo "pipeline scope frozen $(stamp) for checksH (A, C, A, C timing)" >> $OUT/pipeline.txt
trap 'systemctl --user thaw $SC; echo "pipeline THAWED $(stamp)" >> $OUT/pipeline.txt' EXIT
echo "# checksH start $(stamp) UTC: the four timing lines above this one failed (timing954.py not found), rerun here" >> $SUM
for i in 1 2; do
  for b in A C; do
    if [ $b = A ]; then W=$WTA; else W=$WTC; fi
    ( cd "$W/hp" && . ../.venv/bin/activate && nice -n 10 python $OUT/timing954.py $R $ST $OUT/timing_${b}$i --N 24 --threads $T ) > $OUT/timing_${b}$i.json 2> $OUT/timing_${b}$i.err
    echo "timing $b run $i: $(cat $OUT/timing_${b}$i.json | cut -c1-400) $(tail -1 $OUT/timing_${b}$i.err | cut -c1-100)" >> $SUM
  done
done
python3 -I $OUT/compare954.py $OUT/timing_A1.npz $OUT/timing_A2.npz $OUT/timing_C1.npz $OUT/timing_C2.npz > $OUT/timing_compare.txt 2>&1; echo "timing series compare: $(cat $OUT/timing_compare.txt | tr '\n' '|')" >> $SUM
echo "perf: $(which perf 2>&1 | head -1)" >> $SUM
echo "# checksH done $(stamp) UTC" >> $SUM
