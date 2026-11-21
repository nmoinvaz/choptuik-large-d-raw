#!/bin/bash
# #1025 D 17.5, k_c 63: dd M determinant signs at 1.9072222575778963 and 1.9472222575778963 (the coordinator's hc 2026-11-21 ~06:25 UTC), two processes in parallel, same call as the D 18 points, caps 10800 s each by exact pid, BelowNormal.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/d17p5
. $OUT/lib_d17p5.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md510 OPENBLAS_NUM_THREADS=20 OMP_NUM_THREADS=20 MKL_NUM_THREADS=20
export PATH="/c/Users/nathan/Source/venv-md510/Scripts:$PATH"
W=/d/choptuik-i1025d
WOUT=D:/choptuik-i935-raw/I1025-win2/d17p5
STATE=data/sol_l1kc63Fw1025_D17.5000.npy
stamp() { date -u '+%F %T'; }
cd $W/solver/matter || exit 1
[ "$(git hash-object $STATE | cut -c1-12)" = d85f7b71c2c1 ] || { log "state blob hash differs from d85f7b71c2c1: stop"; exit 1; }
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/mem_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/commit_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
echo "# $(stamp) UTC d17p5 start (two processes in parallel), ell_ddm.py $(git hash-object ell_ddm.py | cut -c1-8)" >> $SUM; log "start"
runpt() {
  local lam=$1 tag=$2 name=det_$1
  local s0=$(date +%s)
  crun $name 0 10800 ell_ddm.py "$PY" -u ell_ddm.py det $STATE 17.5 63 $lam --noise 1e-24,1e-20,1e-16 --out $WOUT/ell_ddm_d17p5_win2_$tag.jsonl > $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  echo "$name: ell_ddm.py det exit $RC (want 0), $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED" >> $SUM
}
runpt 1.9072222575778963 lo &
p1=$!
runpt 1.9472222575778963 hi &
p2=$!
wait $p1; wait $p2
cd $OUT && "$PY" read_d17p5_win2.py > d17p5_win2_read.md 2>&1; echo "read_d17p5_win2.py written d17p5_win2_read.md" >> $SUM
log "done"; touch $OUT/d17p5.done; touch $OUT/all.done
