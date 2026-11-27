#!/bin/bash
# #1105 step 1 (t5's order, comment 7212742507): i1105_u0.py on win2's k_c 135 state at D 23.0, the u0 and N sweep, then the control --mutate=steps (must exit 1).
# 1 process, 1 thread (OMP, OPENBLAS, MKL = 1), nice 10, a systemd user unit. Stops at the first failure (STOP.txt).
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170
WTM=/home/nathan/Source/choptuik-large-d-1105/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
ST=$OUT/in/sol_l1kc135win2d23_D23.0000.npy
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP.txt; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $WTM || exit 9
[ "$(git rev-parse --short=8 HEAD)" = 5b1e38e8 ] && [ "$(blob i1105_u0.py)" = e522a5e7 ] || stop "the worktree is not 5b1e38e8 or i1105_u0.py is not e522a5e7"
[ "$(blob $ST)" = cd134e2c ] && [ "$(blob $OUT/in/l1kc135win2d23.jsonl)" = bc295fbc ] || stop "the state or the record is not the pinned blob"
step "pins ok: worktree 5b1e38e8, i1105_u0.py e522a5e7, dss_ell.py $(blob dss_ell.py), state cd134e2c, record bc295fbc"
step "sweep starts: i1105_u0.py STATE 23.0 135 u0_kc135_d23.json --u0=0.01,0.015,0.02,0.03,0.04,0.05,0.06 --N=408,544,816,1088"
t0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -I -u i1105_u0.py $ST 23.0 135 $OUT/u0_kc135_d23.json --u0=0.01,0.015,0.02,0.03,0.04,0.05,0.06 --N=408,544,816,1088 > $OUT/u0_kc135_d23.log 2>&1; e0=$?
step "sweep exit $e0 (0 wanted), $(( $(date +%s) - t0 )) s; $(grep -E 'Maximum resident' $OUT/u0_kc135_d23.log | tr -d '\t')"
[ $e0 = 0 ] || stop "the sweep's sanity check did not pass (exit $e0)"
t1=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -I -u i1105_u0.py $ST 23.0 135 $OUT/u0_kc135_d23_mut.json --u0=0.04 --N=408 --mutate=steps > $OUT/u0_kc135_d23_mut.log 2>&1; e1=$?
step "control --mutate=steps exit $e1 (1 wanted), $(( $(date +%s) - t1 )) s"
[ $e1 = 1 ] || stop "the control did not fail (exit $e1)"
echo "1105 step 1 DONE $(stamp) UTC, sweep exit $e0, control exit $e1" > $OUT/DONE.txt
step "done"
exit 0
}
