#!/bin/bash
# #1080 control walk (t5's order, comment of 19:30 UTC; unit i1080a): zero_mp.py from the fundamental's M = 3 zero in extended precision, M = 5, 5 processes, nice 10.
# Pins: worktree ~/Source/choptuik-large-d-1080 at feat/inner-mp a0441d8b; zero_mp.py 0d94efcd, value_mp.py fbb1b1fa, inner_mp.py 563bc062. Python: main's venv.
# Output: control_walk.jsonl (one row per iteration), control_walk.log; verdict by control_check.py. Log: steps_control.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1080-dh370
WT=/home/nathan/Source/choptuik-large-d-1080
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_control.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/solver/inner_stokes || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = a0441d8b ] && [ "$(blob zero_mp.py)" = 0d94efcd ] && [ "$(blob value_mp.py)" = fbb1b1fa ] && [ "$(blob inner_mp.py)" = 563bc062 ] || { step "STOP: worktree or code not pinned"; echo "CONTROL NOT RUN $(stamp) UTC" > $OUT/CONTROL_DONE.txt; exit 1; }
[ ! -s $OUT/control_walk.jsonl ] || { step "STOP: control_walk.jsonl exists and is not empty"; echo "CONTROL NOT RUN $(stamp) UTC" > $OUT/CONTROL_DONE.txt; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
step "start: $($PY -V 2>&1), mpmath $($PY -c 'import mpmath; print(mpmath.__version__, mpmath.libmp.BACKEND)'); load $(cut -d' ' -f1-3 /proc/loadavg)"
$PY zero_mp.py selftest > $OUT/selftest_zero_mp.txt 2>&1; s0=$?
$PY zero_mp.py selftest --mutate=sign > $OUT/selftest_zero_mp_mutsign.txt 2>&1; s1=$?
step "zero_mp.py selftest exit $s0 (0 wanted), with --mutate=sign exit $s1 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] || { step "STOP: the walk's own selftest or its mutation did not read as written"; echo "CONTROL NOT RUN $(stamp) UTC" > $OUT/CONTROL_DONE.txt; exit 1; }
t0=$(date +%s)
nice -n 10 $PY -u zero_mp.py 2.726475885672135 1.0156030949093042 - $OUT/control_walk.jsonl --M=5 --v0=0.1444194785,0.0110874259,0,0 --procs=5 --iters=8 > $OUT/control_walk.log 2>&1; rc=$?
step "walk exit $rc, $(( $(date +%s) - t0 )) s"
python3 $OUT/control_check.py $OUT/control_walk.log $OUT/control_walk.jsonl > $OUT/control_check.txt 2>&1; rc2=$?
step "control_check exit $rc2 (0 = PASS): $(head -1 $OUT/control_check.txt | cut -c1-500)"
echo "CONTROL DONE walk exit $rc check exit $rc2 $(stamp) UTC" > $OUT/CONTROL_DONE.txt
exit 0
}
