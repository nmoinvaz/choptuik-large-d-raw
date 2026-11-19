#!/bin/bash
# #997 step 2 on dh610: anm_lowd.py --save_series at M 256 from step 1's converged state (I997-dh610/lowD997_D3.1500_M256.npz), N 20, --checks "", --target 3.14, 12 threads, nice 10
# (win2b's command at M 160, I997-win2/run997a.sh, with the state and the thread count changed). RAWDIR is the live clone, which holds I997-dh610/.
. "$(dirname "$0")/common997.sh"
cd "$WT/hp" || exit 1; . $WTV/.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
mkdir -p $OUT/series
echo "# $(stamp) UTC series start, hp $(git rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" >> $OUT/exits_997.txt
s=$(date +%s)
nice -n 10 python -u anm_lowd.py $RAW $OUT/series --state I997-dh610/lowD997_D3.1500_M256.npz --N 20 --checks "" --target 3.14 --threads 12 \
  --save_series $OUT/series_D3.15_M256_N20.npz > $OUT/series/run.log 2>&1
rc=$?
echo "# $(stamp) UTC anm_lowd exit $rc wall $(( $(date +%s) - s )) s" >> $OUT/exits_997.txt
exit $rc
