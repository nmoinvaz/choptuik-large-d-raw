#!/bin/bash
# #1102 (mm5): wait for part A of the D 4628/D 6666 ladder job (a "job rc" line in D4628m/tail/run.log), then run ell_fastm.py jaccheck
# on R0 at k_c 127 from the worktree at 693a4d79: 4 threads, nice 10, timeout 7200. Output: jac127.log, jac127.json.
{
R=$HOME/Source/choptuik-large-d-raw
H=$R/I1102-mm5
RUN=$R/I1098-mm5/ladder/D4628m/tail/run.log
W=$HOME/Source/choptuik-jac127/solver/matter
PY=$HOME/venv-314/bin/python
IN=$R/I1109-mm5/c/in
L=$H/jac127_run.log
echo "waiting $(date -u '+%Y-%m-%d %H:%M:%S UTC') for a job rc line in $RUN" >> $L
until grep -q "^job rc" $RUN 2>/dev/null; do sleep 60; done
echo "part A ended: $(grep '^job rc' $RUN | tail -1)" >> $L
[ "$(git -C $R hash-object --no-filters $IN/sol_l1kc127k070w2_D23.0000.npy | cut -c1-8)" = 90d3e655 ] && [ "$(git -C $R hash-object --no-filters $IN/l1kc127k070w2.jsonl | cut -c1-8)" = d1a3a641 ] || { echo "input blob differs" >> $L; exit 1; }
[ "$(git -C $HOME/Source/choptuik-jac127 rev-parse --short=8 HEAD)" = 693a4d79 ] || { echo "worktree is not 693a4d79" >> $L; exit 1; }
cd $W || exit 1
export OPENBLAS_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4
t0=$(date +%s); echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
nice -n 10 timeout 7200 $PY -u ell_fastm.py jaccheck $IN/l1kc127k070w2.jsonl $IN/sol_l1kc127k070w2_D23.0000.npy 23.0 --out=$H/jac127.json > $H/jac127.log 2>&1
rc=$?
echo "jaccheck exit $rc $(( $(date +%s) - t0 )) s $(date -u +%H:%M:%S)" >> $L
exit $rc
}
