#!/bin/bash
# #1025 D 18, the two outer grid points in parallel now (coordinator's hc 2026-11-21 ~05:52 UTC): ell_ddm.py det at 1.752930001950494 and 1.824478165295412, same call and noise levels, two processes beside run_d18.sh's running point,
# 20 BLAS threads each, BelowNormal, caps 10800 s each by exact pid, each with its own --out file. If run_d18.sh ends (all.done) while they run, all.done is moved aside and the alert-only watches are restarted for them.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/d18
. $OUT/lib_d18.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md510 OPENBLAS_NUM_THREADS=20 OMP_NUM_THREADS=20 MKL_NUM_THREADS=20
export PATH="/c/Users/nathan/Source/venv-md510/Scripts:$PATH"
W=/d/choptuik-i1025d
WOUT=D:/choptuik-i935-raw/I1025-win2/d18
STATE=data/sol_l1kc63W1025_D18.000000.npy
stamp() { date -u '+%F %T'; }
cd $W/solver/matter || exit 1
[ "$(git hash-object $STATE | cut -c1-8)" = 45e72c6a ] || { log "outer: state blob hash differs: stop"; exit 1; }
echo "# $(stamp) UTC outer grid points start (two processes in parallel)" >> $SUM; log "outer start"
runpt() {
  local lam=$1 tag=$2 name=det_$1
  local s0=$(date +%s)
  crun $name 0 10800 ell_ddm.py "$PY" -u ell_ddm.py det $STATE 18 63 $lam --noise 1e-24,1e-20,1e-16 --out $WOUT/ell_ddm_d18_win2_$tag.jsonl > $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  echo "$name: ell_ddm.py det exit $RC (want 0), $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED (outer point, in parallel)" >> $SUM
}
runpt 1.752930001950494 outer1 &
p1=$!
runpt 1.824478165295412 outer2 &
p2=$!
while kill -0 $p1 2>/dev/null || kill -0 $p2 2>/dev/null; do
  if [ -f $OUT/all.done ]; then
    mv $OUT/all.done $OUT/all.done_1
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/mem_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/commit_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
    log "outer: run_d18.sh ended, watches restarted"
  fi
  sleep 20
done
wait $p1; wait $p2
cd $OUT && "$PY" read_d18_win2.py > d18_win2_read.md 2>&1; echo "read_d18_win2.py rewritten (outer points done)" >> $SUM
log "outer done"; touch $OUT/outer.done; touch $OUT/all.done
