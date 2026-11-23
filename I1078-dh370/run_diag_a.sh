#!/bin/bash
# #1078, t5's diagnostic (comment of 18:55 UTC), run (a): equilibrated mode_det (HP_MODE_EQUIL=1, feat/mode-equil a2607acb) at lambda 5.140600 on the D 3.044375 M' 96 state with
# hmax 0.0015 (plan of 1537 steps; the state is unpolished: its |F| on that plan was 1.77e-29 in the earlier run), pivot range only. Starts after unit i1078o (the checks, ending with
# the selftest 1c) ends, and only if (1c) passed. Unit i1078p, 6 threads, nice 10. Log: steps_diag.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WTN=/home/nathan/Source/choptuik-large-d-1078m
PYN=$WTN/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_diag.txt; }
cd $OUT || exit 9
step "waiting for unit i1078o (the checks) to end"
while [ "$(systemctl --user is-active i1078o)" = active ]; do sleep 30; done
grep -q 'EQUAL' MEQUIL_STEP1_DONE.txt && grep -q 'rc 0' MEQUIL_STEP1_DONE.txt || { step "STOP: (1c) did not pass ($(cat MEQUIL_STEP1_DONE.txt 2>/dev/null)); diagnostic not run"; echo "DIAG A NOT RUN $(stamp) UTC" > DIAG_A_DONE.txt; exit 1; }
[ "$(git -C $WTN rev-parse --short=8 HEAD)" = a2607acb ] && [ "$(git hash-object --no-filters $S96 | cut -c1-8)" = 6a0f83d2 ] || { step "STOP: worktree or state not pinned"; echo "DIAG A NOT RUN $(stamp) UTC" > DIAG_A_DONE.txt; exit 1; }
step "(a) starts: HP_MODE_EQUIL=1 mequil_probe.py D 3.044375 M' 96, lambda 5.140600, --hmax=0.0015; load $(cut -d' ' -f1-3 /proc/loadavg)"
t0=$(date +%s)
HP_MODE_EQUIL=1 nice -n 10 $PYN -u mequil_probe.py $WTN/hp diag_a_hmax0015.jsonl $S96 5.140600 --threads=6 --hmax=0.0015 > diag_a_hmax0015.log 2>&1; rc=$?
step "(a) exit $rc, $(( $(date +%s) - t0 )) s wall; $(cat diag_a_hmax0015.log | cut -c1-300 | tail -1)"
echo "DIAG A DONE exit $rc $(stamp) UTC" > DIAG_A_DONE.txt
exit 0
}
