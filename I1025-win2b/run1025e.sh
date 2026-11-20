#!/usr/bin/env bash
# #1025, the coordinator's hc ~15:27 UTC 20 Nov (winb's laptop offline since ~11:45): two jobs, one after the other, from solver/matter of D:/choptuik-i1025b (wip/ell1-highD 5c9d001c), venv-i962,
# 4 BLAS threads, BelowNormal (set by the launching PowerShell). Inputs by git show of raw origin/main 86792f25 into st2/ (blob ids in st2/hashes.txt), states copied into data/.
#  (1) signtest of winb's k_c 63 record at D 16.75 (lam 2.0834870, from winb's 11:42 UTC message; its record jsonl never reached raw): xfkappa's newest signtest.py (I1025-mac, blob a0769780, as st2/signtest_mac.py)
#        signtest_mac.py data/sol_l1kc63Fv1025_D16.7500.npy 16.75 63 2.0634870,2.1034870        -> signtest_kc63_D16.75.log, capped 7200 s by exact pid
#  (2) winb's check (2) of the k_c 71 record at D 16.5, under the rule logged in raw I1025-win README at 2c1a63d4:
#        ell_refine.py l1kc71Fw1025 71 l1kc71Fw1025c 71 1 16.5 2.1408016 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60     -> kc71c_D16.5.log, 12 h cap (43200 s) by exact pid
#      then the record check (winb's check_1025.py, edge rule, --ref 2.1454677, and bracket1025.py) -> check_kc71c.log, then the signtest at lam -/+ 0.02 on its own state
#        signtest_mac.py data/sol_l1kc71Fw1025c_D16.5000.npy 16.5 71 around=data/l1kc71Fw1025c.jsonl:16.5:0.02   -> signtest_kc71c.log, capped 7200 s by exact pid
# Caps are taskkill /T /F of the exact root pid after a command-line check, not retried. One exits_1025.txt line per event. usage: bash run1025e.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
WX=D:/choptuik-large-d-raw/I1025-win2b
PS2=$WX/rootpidpat.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
cd $W || exit 9
[ "$(git rev-parse --short=8 HEAD)" = 5c9d001c ] || { log "e-jobs not started: worktree is not at 5c9d001c"; exit 9; }
for f in sol_l1kc63Fv1025_D16.7500.npy sol_l1kc71Fw1025_D16.5000.npy; do
  cmp -s data/$f $X/st2/$f || { log "e-jobs not started: data/$f differs from the st2/ copy (or is missing)"; exit 9; }
done
for f in l1kc71Fw1025c.jsonl sol_l1kc71Fw1025c_D16.5000.npy; do [ -e data/$f ] && { log "e-jobs not started: data/$f exists"; exit 9; }; done
[ "$(git hash-object $X/st2/signtest_mac.py)" = a0769780be7384436299672a88dd3ebc7f123b7d ] || { log "e-jobs not started: st2/signtest_mac.py is not blob a0769780"; exit 9; }
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
RC=0
runcap() { # name cap logfile script pat -- command...   (sets RC)
  local name=$1 cap=$2 lg=$3 script=$4 pat=$5; shift 6
  echo "== $name: $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
  local t=$(date +%s) capped=0 wpid="" pid i cl
  "$@" >> $lg 2>&1 < /dev/null &
  pid=$!
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 3
    wpid=$(powershell -NoProfile -File "$PS2" -Script "$script" -Pat "$pat" | tr -d '\r')
    [ -n "$wpid" ] && break
    kill -0 $pid 2>/dev/null || break
  done
  if [ -n "$wpid" ]; then log "$name root pid $wpid, cap ${cap} s"
  elif kill -0 $pid 2>/dev/null; then log "UNEXPECTED: root pid of $name not found while it runs, no cap possible (left running)"
  else log "$name ended within seconds, no root pid taken"; fi
  while kill -0 $pid 2>/dev/null; do
    if [ -n "$wpid" ] && [ $(( $(date +%s) - t )) -ge $cap ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *"$script"*"$pat"*) log "$name CAP of ${cap} s reached, last log line: $(tail -n 1 $lg | cut -c1-160); killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
        *) log "pid $wpid is not the $name command (command line: ${cl:0:80}), nothing killed";;
      esac
      break
    fi
    sleep 15
  done
  wait $pid; RC=$?
  log "$name exit $RC wall $(( $(date +%s) - t ))s capped $capped"
  return 0
}
# (1)
runcap "signtest kc63_D16.75" 7200 $X/signtest_kc63_D16.75.log signtest_mac.py sol_l1kc63Fv1025_D16.7500 -- \
  "$PY" -u $WX/st2/signtest_mac.py data/sol_l1kc63Fv1025_D16.7500.npy 16.75 63 2.0634870,2.1034870
# (2)
runcap "kc71c_D16.5" 43200 $X/kc71c_D16.5.log ell_refine.py l1kc71Fw1025c -- \
  "$PY" -u ell_refine.py l1kc71Fw1025 71 l1kc71Fw1025c 71 1 16.5 2.1408016 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60
if [ -s data/l1kc71Fw1025c.jsonl ] && grep -q '"lam": [0-9]' data/l1kc71Fw1025c.jsonl; then
  {
    echo "== check_1025.py (winb's, blob 6840ce89) edge rule, --ref 2.1454677 $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    "$PY" -I $WX/st2/check_1025_win.py data/l1kc71Fw1025c.jsonl 16.5 --rule edge --ref 2.1454677; echo "== exit $?"
    echo "== bracket1025.py"
    "$PY" -I $WX/bracket1025.py data/l1kc71Fw1025c.jsonl 16.5; echo "== exit $?"
  } >> $X/check_kc71c.log 2>&1
  log "kc71c_D16.5 record check written to check_kc71c.log"
  runcap "signtest kc71c_D16.5" 7200 $X/signtest_kc71c.log signtest_mac.py sol_l1kc71Fw1025c_D16.5000 -- \
    "$PY" -u $WX/st2/signtest_mac.py data/sol_l1kc71Fw1025c_D16.5000.npy 16.5 71 around=data/l1kc71Fw1025c.jsonl:16.5:0.02
else
  log "kc71c_D16.5: no record with a lambda, no record check and no signtest"
fi
log "e-jobs done"
