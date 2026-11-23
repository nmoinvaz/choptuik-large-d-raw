#!/bin/bash
# #1078, t5's order (comment of 23:40 UTC; unit i1078w), on the D 3.044375 M' 96 state 6a0f83d2, 4 threads, nice 10, beside the #1080 control:
# (1) the background Jacobian: jac_diag.py (one dd Newton step with its LU's pivot range, then Solver.jacobian's dense matrix, equilibrated float64 LU, the 200 smallest pivots with their unknowns);
# (2) the equilibrated mode_det (HP_MODE_EQUIL=1, feat/mode-equil a2607acb kernel) at lambda 1, 3 and 8, pivot range only (mequil_probe.py);
# (3) the control of (1): the same jac_diag.py on the D 3.15 M' 96 state 9e683a14 (benign at D 3.15: the diagnostic must be able to read benign).
# Worktree ~/Source/choptuik-large-d-1078 at 3279c81f (c016b932 kernel) for (1), (3); ~/Source/choptuik-large-d-1078m (a2607acb) for (2). Log: steps_background.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
WTM=/home/nathan/Source/choptuik-large-d-1078m
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
S315=$RAWIN/I1072-dh370/states2/tmap_tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326_L0.7_M96_s1.8326.npz
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_background.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_BACKGROUND_$1.txt; step "STOP $1: $2"; echo "BACKGROUND STOPPED at $1 $(stamp) UTC" > $OUT/BACKGROUND_DONE.txt; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 3279c81f ] && [ "$(git -C $WTM rev-parse --short=8 HEAD)" = a2607acb ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob $S315)" = 9e683a14 ] && [ "$(blob mode_scale.py)" = 794be9b9 ] || stop 0 "a worktree, a state or mode_scale.py not pinned"
python3 $OUT/jac_count.py selftest > $OUT/selftest_jac_count.txt 2>&1 && ! python3 $OUT/jac_count.py selftest --mutate=delta > /dev/null 2>&1 || stop 0 "jac_count.py selftest or its mutation did not read as written"
step "start; load $(cut -d' ' -f1-3 /proc/loadavg)"
# (1)
t0=$(date +%s)
nice -n 10 $WT/.venv/bin/python -u $OUT/jac_diag.py $S96 $OUT/jac_diag_D3.0444_M96.jsonl --threads=4 > $OUT/jac_diag_D3.0444_M96.log 2>&1; rc=$?
step "(1) jac_diag on the D 3.044375 state: exit $rc, $(( $(date +%s) - t0 )) s; $(cut -c1-330 $OUT/jac_diag_D3.0444_M96.log | grep -v Warning | tr '\n' '|')"
echo "BACKGROUND STEP 1 rc $rc $(stamp) UTC" > $OUT/BACKGROUND_STEP1_DONE.txt
[ $rc = 0 ] || stop 1 "jac_diag exit $rc"
python3 $OUT/jac_count.py $OUT/jac_diag_D3.0444_M96.jsonl > $OUT/jac_count_D3.0444_M96.txt 2>&1
# (2)
cd $WTM/hp || exit 9
t0=$(date +%s)
HP_MODE_EQUIL=1 nice -n 10 $WTM/.venv/bin/python -u $OUT/mequil_probe.py $WTM/hp $OUT/probe_G_d3044_equil_lam138.jsonl $S96 1 3 8 --threads=4 > $OUT/probe_G_d3044_equil_lam138.log 2>&1; rc=$?
step "(2) equilibrated mode_det at lambda 1, 3, 8: exit $rc, $(( $(date +%s) - t0 )) s; $(cut -c1-200 $OUT/probe_G_d3044_equil_lam138.log | tr '\n' '|')"
echo "BACKGROUND STEP 2 rc $rc $(stamp) UTC" > $OUT/BACKGROUND_STEP2_DONE.txt
[ $rc = 0 ] || stop 2 "mequil_probe exit $rc"
# (3) the control of (1)
cd $WT/hp || exit 9
t0=$(date +%s)
nice -n 10 $WT/.venv/bin/python -u $OUT/jac_diag.py $S315 $OUT/jac_diag_D3.15_M96.jsonl --threads=4 > $OUT/jac_diag_D3.15_M96.log 2>&1; rc=$?
step "(3) jac_diag on the D 3.15 state (the control): exit $rc, $(( $(date +%s) - t0 )) s; $(cut -c1-330 $OUT/jac_diag_D3.15_M96.log | grep -v Warning | tr '\n' '|')"
python3 $OUT/jac_count.py $OUT/jac_diag_D3.15_M96.jsonl > $OUT/jac_count_D3.15_M96.txt 2>&1
echo "BACKGROUND DONE (1) rc, (2) rc, (3) rc $rc $(stamp) UTC" > $OUT/BACKGROUND_DONE.txt
exit 0
}
