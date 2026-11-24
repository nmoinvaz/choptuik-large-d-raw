#!/bin/bash
# #1080 control, restart on the faster walk (t5's hc 2026-11-23, after 4 h of iteration 0 of the first code): waits for the first row of control_walk.jsonl (unit i1080a, feat/inner-mp a0441d8b), stops that unit,
# and restarts from that row on feat/inner-mp 73dcf243 (worktree ~/Source/choptuik-large-d-1080b; the centre first at both precisions, the offsets from its harmonics and inner Jacobian at one precision):
#   python3 zero_mp.py <row 0's A + dA> <row 0's wf + dwf> - control_walk_b.jsonl --M=5 --v0=<row 0's F3, four strings> --procs=5 --iters=8
# The same pass rule (control_check.py: 'located' and the last (A, wf) within 1e-10 of (2.71857918921174, 0.999228403206568) in each coordinate). Unit i1080b, nice 10. Log: steps_control_b.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1080-dh370
WT=/home/nathan/Source/choptuik-large-d-1080b
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_control_b.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/solver/inner_stokes || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 73dcf243 ] && [ "$(blob zero_mp.py)" = 1077ea0e ] && [ "$(blob value_mp.py)" = 56bb4856 ] && [ "$(blob inner_mp.py)" = 563bc062 ] || { step "STOP: worktree or code not pinned (73dcf243, 1077ea0e, 56bb4856, 563bc062)"; echo "CONTROL B NOT RUN $(stamp) UTC" > $OUT/CONTROL_B_DONE.txt; exit 1; }
[ ! -s $OUT/control_walk_b.jsonl ] || { step "STOP: control_walk_b.jsonl exists and is not empty"; echo "CONTROL B NOT RUN $(stamp) UTC" > $OUT/CONTROL_B_DONE.txt; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
$PY zero_mp.py selftest > $OUT/selftest_zero_mp_b.txt 2>&1; s0=$?
$PY zero_mp.py selftest --mutate=sign > $OUT/selftest_zero_mp_b_mutsign.txt 2>&1; s1=$?
step "start: zero_mp.py (73dcf243) selftest exit $s0 (0 wanted), with --mutate=sign exit $s1 (1 wanted); waiting for the first row of control_walk.jsonl (unit i1080a)"
[ $s0 = 0 ] && [ $s1 = 1 ] || { step "STOP: the selftest or its mutation did not read as written"; echo "CONTROL B NOT RUN $(stamp) UTC" > $OUT/CONTROL_B_DONE.txt; exit 1; }
while [ "$(grep -c . $OUT/control_walk.jsonl 2>/dev/null || echo 0)" -lt 1 ]; do
  [ "$(systemctl --user is-active i1080a)" = active ] || { step "STOP: unit i1080a ended without a first row ($(cat $OUT/CONTROL_DONE.txt 2>/dev/null))"; echo "CONTROL B NOT RUN $(stamp) UTC" > $OUT/CONTROL_B_DONE.txt; exit 1; }
  sleep 10
done
systemctl --user stop i1080a
cp $OUT/control_walk.jsonl $OUT/control_walk_a_row0.jsonl
read A0 WF0 V0 < <(python3 - <<PY
import json
r = json.loads(open("$OUT/control_walk_a_row0.jsonl").readline())
print(repr(r["A"] + r["dA"]), repr(r["wf"] + r["dwf"]), ",".join(str(x) for x in r["F3"]))
PY
)
step "unit i1080a stopped after its first row (a0441d8b: row 0 of control_walk_a_row0.jsonl, $(python3 -c "import json; r=json.loads(open('$OUT/control_walk_a_row0.jsonl').readline()); print('A', r['A'], 'wf', r['wf'], '|R|/sigma', round(r['R_over_sig'], 3), 'dx', r['dA'], r['dwf'], 'sec', r['sec'])")); restart at ($A0, $WF0), v0 $V0"
t0=$(date +%s)
nice -n 10 $PY -u zero_mp.py $A0 $WF0 - $OUT/control_walk_b.jsonl --M=5 --v0=$V0 --procs=5 --iters=8 > $OUT/control_walk_b.log 2>&1; rc=$?
step "walk exit $rc, $(( $(date +%s) - t0 )) s"
python3 $OUT/control_check.py $OUT/control_walk_b.log $OUT/control_walk_b.jsonl > $OUT/control_check_b.txt 2>&1; rc2=$?
step "control_check exit $rc2 (0 = PASS): $(head -1 $OUT/control_check_b.txt | cut -c1-500)"
echo "CONTROL B DONE walk exit $rc check exit $rc2 $(stamp) UTC" > $OUT/CONTROL_B_DONE.txt
exit 0
}
