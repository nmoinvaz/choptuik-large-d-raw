#!/bin/bash
# #954 (the coordinator's addition), build C (PR #955, perf/series-par-at): 1. jet_by_order_check at N 12 with 1 thread (saved) and with 8 threads (--compare: 0 words differ),
# and at N 24 with 8 threads (passes, its controls failing); 2. highm_check jets at Ms 32,48,64 (exit 0) and with --mutate=kappa (exit 1); 3. the timing of A and C alternated twice at
# 8 threads on ST (truth_system, newton_o, coefficients_o by_order at 24), the series compared word for word, with the load average beside each; 4. perf, if installed.
. "$(dirname "$0")/common954.sh"
WTA=/home/nathan/Source/choptuik-large-d-954a; WTC=/home/nathan/Source/choptuik-large-d-954c
SUM=$OUT/summary_C.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WTC/hp" || exit 1; . ../.venv/bin/activate
so=$(python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
hdr() { echo "# $(stamp) UTC build C, hp $(git -C $WTC rev-parse --short HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)')"; echo "# multidouble in the .so: $(strings -n 8 $so 2>/dev/null | grep -oE 'multidouble[-/][^/ ]+' | sort -u | head -3 | tr '\n' ' ')"; }
run() { local name=$1 want=$2; shift 2; { hdr; echo "# cmd: $*"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
: > $SUM
run C_jbo_t1 0 python jet_by_order_check.py $R $ST --N 12 --threads 1 --Np 6 --out $OUT/jbo_t1 --save $OUT/jbo_t1.npz
run C_jbo_t8_compare 0 python jet_by_order_check.py $R $ST --N 12 --threads 8 --Np 6 --out $OUT/jbo_t8 --compare $OUT/jbo_t1.npz
run C_jbo_N24 0 python jet_by_order_check.py $R $ST --N 24 --threads 8 --Np 6 --out $OUT/jbo_N24
run C_jets 0 python highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json --Ms=32,48,64
run C_jets_kappa 1 python highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json --Ms=32,48,64 --mutate=kappa
# the timing: A, C, A, C
for i in 1 2; do
  for b in A C; do
    if [ $b = A ]; then W=$WTA; else W=$WTC; fi
    ( cd "$W/hp" && . ../.venv/bin/activate && nice -n 10 python timing954.py $R $ST $OUT/timing_${b}$i --N 24 --threads $T ) > $OUT/timing_${b}$i.json 2> $OUT/timing_${b}$i.err
    echo "timing $b run $i: $(cat $OUT/timing_${b}$i.json | cut -c1-400) $(tail -1 $OUT/timing_${b}$i.err | cut -c1-100)" >> $SUM
  done
done
python3 -I $OUT/compare954.py $OUT/timing_A1.npz $OUT/timing_A2.npz $OUT/timing_C1.npz $OUT/timing_C2.npz > $OUT/timing_compare.txt 2>&1; echo "timing series compare: $(cat $OUT/timing_compare.txt | tr '\n' '|')" >> $SUM
echo "perf: $(which perf 2>&1 | head -1)" >> $SUM
echo "# checksC done $(stamp) UTC" >> $SUM
