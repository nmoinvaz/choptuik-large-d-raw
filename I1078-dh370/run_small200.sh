#!/bin/bash
# #1078, t5's order (comment of 20:45 UTC, check 3; unit i1078r), beside the #1080 control (5 processes): hp/mode_scale.py (main 6a240733, blob 794be9b9) --small=200 at lambda 5.140600,
# D 3.044375 M' 96 state 6a0f83d2, hmax 0.05, 4 threads, nice 10: the ten smallest scaled float64 pivots with their unknown indices. HP_MODE_EQUIL unset, HP_DENSE_M_MAX unset.
# Kernel: the c016b932 build of ~/Source/choptuik-large-d-1078/.venv (mode_matrix, mode_det unchanged by a2607acb when unset). Log: steps_small200.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_small200.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 6a240733 ] && [ "$(blob mode_scale.py)" = 794be9b9 ] && [ "$(blob lowD_gamma.py)" = e040c8a2 ] && [ "$(blob $S96)" = 6a0f83d2 ] || { step "STOP: worktree, mode_scale.py, lowD_gamma.py or the state not pinned"; echo "SMALL NOT RUN $(stamp) UTC" > $OUT/SMALL200_DONE.txt; exit 1; }
$PY mode_scale.py selftest > $OUT/modescale_selftest_small200.txt 2>&1; s0=$?
$PY $OUT/small_check.py > $OUT/small_check200.txt 2>&1; s1=$?
$PY $OUT/small_check.py --mutate=shift > $OUT/small_check200_mut.txt 2>&1; s2=$?
step "start: mode_scale selftest exit $s0 (0 wanted); small_check exit $s1 (0 wanted), with --mutate=shift exit $s2 (1 wanted); load $(cut -d' ' -f1-3 /proc/loadavg)"
[ $s0 = 0 ] && [ $s1 = 0 ] && [ $s2 = 1 ] || { step "STOP: a selftest or its control did not read as written"; echo "SMALL NOT RUN $(stamp) UTC" > $OUT/SMALL200_DONE.txt; exit 1; }
t0=$(date +%s)
nice -n 10 $PY -u mode_scale.py $OUT/modescale_small200.jsonl $S96 5.140600 --hmax=0.05 --threads=4 --small=200 > $OUT/modescale_small200.log 2>&1; rc=$?
step "mode_scale --small=200 exit $rc, $(( $(date +%s) - t0 )) s"
echo "SMALL DONE exit $rc $(stamp) UTC" > $OUT/SMALL200_DONE.txt
exit 0
}
