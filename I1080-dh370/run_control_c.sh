#!/bin/bash
# #1080 control, third start (t5's hc 2026-11-24: the first walk, feat/inner-mp a0441d8b, was stopped after 7 h 0x min in iteration 0 with no row: its step halving wastes calls at every solve's floor, fixed in 73dcf243):
# the new code from the ORIGINAL start: python3 zero_mp.py 2.726475885672135 1.0156030949093042 - control_walk_c.jsonl --M=5 --v0=0.1444194785,0.0110874259,0,0 --procs=5 --iters=8 on feat/inner-mp 73dcf243
# (worktree ~/Source/choptuik-large-d-1080b; zero_mp.py 1077ea0e, value_mp.py 56bb4856, inner_mp.py 563bc062). Same pass rule (control_check.py). Unit i1080c, 5 processes, nice 10. Log: steps_control_c.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1080-dh370
WT=/home/nathan/Source/choptuik-large-d-1080b
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_control_c.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/solver/inner_stokes || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 73dcf243 ] && [ "$(blob zero_mp.py)" = 1077ea0e ] && [ "$(blob value_mp.py)" = 56bb4856 ] && [ "$(blob inner_mp.py)" = 563bc062 ] || { step "STOP: worktree or code not pinned (73dcf243, 1077ea0e, 56bb4856, 563bc062)"; echo "CONTROL C NOT RUN $(stamp) UTC" > $OUT/CONTROL_C_DONE.txt; exit 1; }
[ ! -s $OUT/control_walk_c.jsonl ] || { step "STOP: control_walk_c.jsonl exists and is not empty"; echo "CONTROL C NOT RUN $(stamp) UTC" > $OUT/CONTROL_C_DONE.txt; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
$PY zero_mp.py selftest > $OUT/selftest_zero_mp_c.txt 2>&1; s0=$?
$PY zero_mp.py selftest --mutate=sign > $OUT/selftest_zero_mp_c_mutsign.txt 2>&1; s1=$?
python3 $OUT/control_check.py selftest > $OUT/selftest_control_check_c.txt 2>&1; s2=$?
step "start: $($PY -V 2>&1), mpmath $($PY -c 'import mpmath; print(mpmath.__version__, mpmath.libmp.BACKEND)'); zero_mp.py selftest exit $s0 (0 wanted), with --mutate=sign exit $s1 (1 wanted); control_check selftest exit $s2 (0 wanted); load $(cut -d' ' -f1-3 /proc/loadavg)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 0 ] || { step "STOP: a selftest or its mutation did not read as written"; echo "CONTROL C NOT RUN $(stamp) UTC" > $OUT/CONTROL_C_DONE.txt; exit 1; }
t0=$(date +%s)
nice -n 10 $PY -u zero_mp.py 2.726475885672135 1.0156030949093042 - $OUT/control_walk_c.jsonl --M=5 --v0=0.1444194785,0.0110874259,0,0 --procs=5 --iters=8 > $OUT/control_walk_c.log 2>&1; rc=$?
step "walk exit $rc, $(( $(date +%s) - t0 )) s"
python3 $OUT/control_check.py $OUT/control_walk_c.log $OUT/control_walk_c.jsonl > $OUT/control_check_c.txt 2>&1; rc2=$?
step "control_check exit $rc2 (0 = PASS): $(head -1 $OUT/control_check_c.txt | cut -c1-500)"
echo "CONTROL C DONE walk exit $rc check exit $rc2 $(stamp) UTC" > $OUT/CONTROL_C_DONE.txt
exit 0
}
