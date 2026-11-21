#!/bin/bash
# #1025 D 18, the two outer grid points (coordinator's hc 2026-11-21 ~05:47 UTC): after run_d18.sh (all.done), ell_ddm.py det at 1.752930001950494 and 1.824478165295412 (xfkappa's D 18 root record, bf5b9d7f) with the same call,
# --noise 1e-24,1e-20,1e-16; one invocation per point, 20 BLAS threads, BelowNormal, caps 10800 s each by exact pid. The watches are restarted for it.
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
t=$(date +%s)
while [ ! -f $OUT/all.done ]; do
  [ $(( $(date +%s) - t )) -gt 21600 ] && { log "outer: all.done not seen in 6 h, stop"; exit 1; }
  sleep 20
done
mv $OUT/all.done $OUT/all.done_1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/mem_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/commit_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
cd $W/solver/matter || exit 1
[ "$(git hash-object $STATE | cut -c1-8)" = 45e72c6a ] || { log "outer: state blob hash differs: stop"; exit 1; }
echo "# $(stamp) UTC outer grid points start" >> $SUM; log "outer start"
for lam in 1.752930001950494 1.824478165295412; do
  name=det_$lam
  s0=$(date +%s)
  crun $name 0 10800 ell_ddm.py "$PY" -u ell_ddm.py det $STATE 18 63 $lam --noise 1e-24,1e-20,1e-16 --out $WOUT/ell_ddm_d18_win2.jsonl > $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  echo "$name: ell_ddm.py det exit $RC (want 0), $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED" >> $SUM
done
cd $OUT && "$PY" read_d18_win2.py > d18_win2_read.md 2>&1; echo "read_d18_win2.py rewritten for four points" >> $SUM
log "outer done"; touch $OUT/outer.done; touch $OUT/all.done
