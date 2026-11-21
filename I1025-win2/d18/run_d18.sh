#!/bin/bash
# #1025 D 18 on win2 (the coordinator's hc 2026-11-21 ~05:28 UTC; xfkappa's criteria I1025-mac/d18/d18_dd_criteria.log): the full dd M as a second machine, from solver/matter of D:\choptuik-i1025d (wip/ell1-highD 48c36355),
# venv-md510's python, 20 BLAS threads, BelowNormal. (1) ell_ddm.py selftest (PASS), (2) selftest --mutate=slices (FAIL), (3) det at 1.788704083622953, (4) det at 1.8, each with --noise 1e-24,1e-20,1e-16.
# Caps by the exact root pid (command line checked for ell_ddm.py): 1800 s per selftest, 10800 s per det point.
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
[ "$(git -C $W rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "worktree not at 48c36355: stop"; exit 1; }
[ "$(git hash-object $STATE | cut -c1-8)" = 45e72c6a ] || { log "state blob hash differs from 45e72c6a: stop"; exit 1; }
echo "# $(stamp) UTC d18 start, ell_ddm.py $(git hash-object ell_ddm.py | cut -c1-8), python $PY, BLAS threads 20" >> $SUM; log "start"
# ---- selftests
crun selftest 0 1800 ell_ddm.py "$PY" -u ell_ddm.py selftest > $OUT/selftest.log 2>&1
r1=$RC; echo "exit $r1" >> $OUT/selftest.log
echo "selftest: expected exit 0 (PASS), got $r1; last line: $(grep -a . $OUT/selftest.log | tail -n 2 | head -n 1 | cut -c1-120)" >> $SUM
crun selftest_slices 1 1800 ell_ddm.py "$PY" -u ell_ddm.py selftest --mutate=slices > $OUT/selftest_slices.log 2>&1
r2=$RC; echo "exit $r2" >> $OUT/selftest_slices.log
echo "selftest --mutate=slices: expected exit 1 (FAIL), got $r2; last line: $(grep -a . $OUT/selftest_slices.log | tail -n 2 | head -n 1 | cut -c1-120)" >> $SUM
if [ "$r1" != 0 ] || [ "$r2" != 1 ]; then echo "# selftests not as required: stop (reading 1)" >> $SUM; log "selftests wrong: stop"; touch $OUT/all.done; exit 1; fi
# ---- det points
for lam in 1.788704083622953 1.8; do
  name=det_$lam
  s0=$(date +%s)
  crun $name 0 10800 ell_ddm.py "$PY" -u ell_ddm.py det $STATE 18 63 $lam --noise 1e-24,1e-20,1e-16 --out $WOUT/ell_ddm_d18_win2.jsonl > $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  echo "$name: ell_ddm.py det exit $RC (want 0), $(( $(date +%s) - s0 )) s wall (cap 10800 s) capped $CAPPED" >> $SUM
done
cd $OUT && "$PY" read_d18_win2.py > d18_win2_read.md 2>&1; echo "read_d18_win2.py written d18_win2_read.md" >> $SUM
log "done"; touch $OUT/all.done
