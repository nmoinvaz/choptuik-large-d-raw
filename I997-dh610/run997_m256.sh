#!/bin/bash
# #997 step 1 on dh610: D 3.15 at M 256 from I927-mac's M 160 state with lowD_dd.py, the state's own nodes, kt 36, kc 100 and ks 250 (read from its meta),
# --jac f64 --tol 1e-29, 12 threads, nice 10. $1 = the --Ms list (256; 192,256 steps through M 192 first), $2 = the output name (m256).
. "$(dirname "$0")/common997.sh"
MS=${1:-256}; NAME=${2:-m256}
cd "$WT/hp" || exit 1; . $WTV/.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
[ -s $R/$ST ] || { echo "missing $ST"; exit 9; }
echo "# $(stamp) UTC start, hp $(git rev-parse --short=8 HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)'), Ms $MS, load $(cut -d' ' -f1-3 /proc/loadavg)" >> $OUT/exits_997.txt
s=$(date +%s)
nice -n 10 python -u lowD_dd.py $OUT/$NAME.jsonl --start $R/$ST --Ms $MS --nodes $NODES --kt 36 --kcs 100 --ks 250 --jac f64 --tol 1e-29 --threads 12 --tag lowD997 > $OUT/$NAME.log 2>&1
rc=$?
echo "# $(stamp) UTC lowD_dd Ms $MS exit $rc wall $(( $(date +%s) - s )) s" >> $OUT/exits_997.txt
ls hp/data/lowD_states/lowD997* data/lowD_states/lowD997* 2>/dev/null >> $OUT/exits_997.txt
exit $rc
