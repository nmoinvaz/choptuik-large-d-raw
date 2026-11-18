#!/bin/bash
# #967 item 2 on dh610: jet_by_order_check.py at N 12, Np 6 on ST (ks 240) and S291 (ks 291), at 2 threads (saved), then 6 and
# 16 threads with --compare against the 2-thread series. One run at a time, so each by-order time is measured alone. BLAS threads
# are 1, so --threads is the run's thread count. Exit 0 is a pass with every control firing; exit 1 is a failed check and the
# script goes on (a failure is a result); any other exit stops it.
. "$(dirname "$0")/common967.sh"
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
SUM=$OUT/summary_item2.txt
hdr() { echo "# $(stamp) UTC build $(git -C $WT rev-parse --short HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)"; }
run() { local name=$1; shift; { hdr; echo "# cmd: $*"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: exit $rc, $(( $(date +%s) - s )) s, load at start $(sed -n 1p $OUT/$name.log | grep -oE 'load .*')" >> $SUM
  [ $rc = 0 ] || [ $rc = 1 ] || { echo "stopped: $name exit $rc" >> $SUM; exit $rc; }; }
echo "# checks967 start $(stamp) UTC; $(lscpu | grep -E 'Model name' | sed 's/  */ /g')" > $SUM
for tag in ks240 ks291; do
  if [ $tag = ks240 ]; then ST=$ST; else ST=$S291; fi
  run jbo_${tag}_t2 python jet_by_order_check.py $R $ST --N 12 --threads 2 --Np 6 --out $OUT/jbo_${tag}_t2 --save $OUT/jbo_${tag}_t2.npz
  run jbo_${tag}_t6 python jet_by_order_check.py $R $ST --N 12 --threads 6 --Np 6 --out $OUT/jbo_${tag}_t6 --compare $OUT/jbo_${tag}_t2.npz
  run jbo_${tag}_t16 python jet_by_order_check.py $R $ST --N 12 --threads 16 --Np 6 --out $OUT/jbo_${tag}_t16 --compare $OUT/jbo_${tag}_t2.npz
done
echo "# checks967 done $(stamp) UTC" >> $SUM
