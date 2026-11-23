#!/bin/bash
# #1078, t5's order (coordinator comment 14:15 UTC): map the roots of det M(lambda) on the M' 96 state before reading gamma: lowD_gamma.py --scan=5.14060,5.14100,41 (sign, ln|det| and
# pivots per lambda into OUT, no root search), worktree 1078 at main 552a32d9 (lowD_gamma.py blob e040c8a2; Python only, no rebuild), HP_DENSE_M_MAX unset, 6 threads, nice 10.
# usage: run_scan_roots.sh a                              plan a: the hmax 0.05 plan, state unpolished (unit i1078g)
#        run_scan_roots.sh b --hmax=0.0015 --polish=4     plan b: the 1537-step plan, state polished on it (unit i1078h)
# Log: steps_scan_<label>.txt. No hc from here.
{
LABEL=$1; shift
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
J=$OUT/scan_roots_$LABEL.jsonl
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
unset HP_DENSE_M_MAX
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_scan_$LABEL.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 552a32d9 ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob lowD_gamma.py)" = e040c8a2 ] || { step "STOP: worktree, state or lowD_gamma.py not pinned (552a32d9, 6a0f83d2, e040c8a2)"; exit 1; }
step "start plan $LABEL: lowD_gamma.py $J <the M' 96 state> --threads=6 --scan=5.14060,5.14100,41 $*; load $(cut -d' ' -f1-3 /proc/loadavg)"
t0=$(date +%s)
nice -n 10 timeout 172800 $PY -u lowD_gamma.py $J $S96 --threads=6 --scan=5.14060,5.14100,41 "$@" > $OUT/scan_roots_$LABEL.log 2>&1; rc=$?
step "scan $LABEL: exit $rc, $(( $(date +%s) - t0 )) s, $(grep -c '"scan": true' $J 2>/dev/null) points"
echo "SCAN $LABEL DONE exit $rc $(stamp) UTC" > $OUT/SCAN_${LABEL}_DONE.txt
exit 0
}
