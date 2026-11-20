#!/usr/bin/env bash
# #1025: signtests of the two redo records (coordinator's hc ~09:07 UTC 20 Nov), at lambda -/+ 0.02 of each record's lambda, one at a time, each as soon as its own redo job has exited and left a record:
#   redo55_D16.5 : signtest.py data/sol_l1kc55Fw1025_D16.5000.npy 16.5 55 around=data/l1kc55Fw1025.jsonl:16.5:0.02
#   redo47_D17   : signtest.py data/sol_l1kc47Fw1025_D17.0000.npy 17 47 around=data/l1kc47Fw1025.jsonl:17.0:0.02
# From solver/matter of D:/choptuik-i1025b, venv-i962, 4 BLAS threads, BelowNormal, each capped at 7200 s by the exact pid of its python. Output appended to signtest_redo.log, one exits_1025.txt line per signtest.
# A job that ends without a record (refused, failed, capped) gets a line saying so and no signtest. The planted control (agree, agree, DISAGREE) was printed at 08:15:50 UTC with this signtest.py. usage: bash signtest_redo1025.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
WX=D:/choptuik-large-d-raw/I1025-win2b
PS1=$WX/rootpidpat.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
cd $W || exit 9
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
runcap() { # name cap logfile signtest-args...
  local name=$1 cap=$2 lg=$3; shift 3
  local pat=$1
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
  local t=$(date +%s) capped=0 wpid="" i
  "$PY" -u $WX/signtest.py "$@" >> $lg 2>&1 < /dev/null &
  local pid=$!
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 3
    wpid=$(powershell -NoProfile -File "$PS1" -Script signtest.py -Pat "$(basename $pat)" | tr -d '\r')
    [ -n "$wpid" ] && break
    kill -0 $pid 2>/dev/null || break
  done
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t )) -ge $cap ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *signtest.py*$(basename $pat)*) log "$name CAP of ${cap} s reached, killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
        *) log "pid $wpid is not the $name command, nothing killed";;
      esac
      break
    fi
    sleep 10
  done
  wait $pid; local rc=$?
  log "signtest redo $name exit $rc wall $(( $(date +%s) - t ))s capped $capped"
}
pending="redo55_D16.5 redo47_D17"
end=$(date -u -d '2026-11-21 00:00:00' +%s)
while [ -n "$pending" ] && [ $(date +%s) -lt $end ]; do
  for n in $pending; do
    if grep -aq "$n exit" $X/exits_1025.txt; then
      pending=$(echo " $pending " | sed "s/ $n / /" | xargs)
      case $n in
        redo55_D16.5) rec=data/l1kc55Fw1025.jsonl; st=sol_l1kc55Fw1025_D16.5000.npy; D=16.5; K=55;;
        redo47_D17)   rec=data/l1kc47Fw1025.jsonl; st=sol_l1kc47Fw1025_D17.0000.npy; D=17.0; K=47;;
      esac
      if [ -s $rec ] && grep -q '"lam": [0-9]' $rec; then
        runcap "$n" 7200 $X/signtest_redo.log data/$st $D $K around=$rec:$D:0.02
      else
        log "signtest redo $n: no record with a lambda (the job ended without one), no signtest"
      fi
    fi
  done
  sleep 20
done
log "signtest redo chain done"
