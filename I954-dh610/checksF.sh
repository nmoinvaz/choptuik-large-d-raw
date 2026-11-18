#!/bin/bash
# #954: series_split_check.py crashed on A ("no octo-double LU", after set_horizon_alpha); the coordinator fixed the script in origin/main (newton_o after each set_horizon_alpha, outside the timings), and the fixed script is run here (series_split_check_main.py, from origin/main), on A at D 253 and D 229 (exit 0 expected) and with --mutate 31 (exit 1 expected), 8 threads, nice 10, PYTHONPATH at A's hp.
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954a
SUM=$OUT/summary_F.txt
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH="$WT/hp"
run() { local name=$1 want=$2; shift 2; { echo "# $(stamp) UTC build A, modified check, hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)')"; echo "# cmd: $*"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
: > $SUM
run A_splitfix_D253 0 python $OUT/series_split_check_main.py $R $ST2 --N 24 --threads $T --Np 6 --out $OUT/splitfix_D253
run A_splitfix_D229 0 python $OUT/series_split_check_main.py $R $ST --N 24 --threads $T --Np 6 --out $OUT/splitfix_D229
run A_splitfix_mutate31 1 python $OUT/series_split_check_main.py $R $ST2 --N 6 --Np 3 --mutate 31 --threads $T --out $OUT/splitfix_mutate
echo "# checksF done $(stamp) UTC" >> $SUM
