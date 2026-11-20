#!/usr/bin/env bash
# #1025 signtest batch (coordinator's hc ~08:25 UTC 20 Nov, list from xfkappa): after D 16.25's record and its signtest, the 11 records of the delta table at D 15-17 that have no signtest (rows in st/rows.txt: tag K D DDDD),
# one at a time, from solver/matter of D:/choptuik-i1025b, venv-i962, 4 BLAS threads, BelowNormal (set by the launching PowerShell). Inputs were taken by git show from choptuik-large-d-raw origin/main (hashes in st/hashes.txt).
# Each signtest is capped at 7200 s by the exact pid of its python (found by rootpidpat.ps1, command line checked, taskkill /T /F), not retried. Output appended to signtest_list.log, one exits_1025.txt line per row.
# Step 0 waits (at most until 11:30 UTC) for D 16.25's restart to exit, then runs its signtest (signtest1025.sh u, into signtest.log) if its record exists. usage: bash signtest_batch1025.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
WX=D:/choptuik-large-d-raw/I1025-win2b
PS1=$WX/rootpidpat.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
n0=$(grep -ac "D16.25 restart exit" $X/exits_1025.txt)
end=$(date -u -d '2026-11-20 11:30:00' +%s)
while [ "$(grep -ac 'D16.25 restart exit' $X/exits_1025.txt)" = "$n0" ] && [ $(date +%s) -lt $end ]; do sleep 20; done
if [ "$(grep -ac 'D16.25 restart exit' $X/exits_1025.txt)" = "$n0" ]; then log "batch: D 16.25 restart still running at 11:30 UTC, starting the batch anyway"; fi
cd $W || exit 9
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
if [ -s data/l1kc55Fu1025.jsonl ] && grep -q '"D": 16.25' data/l1kc55Fu1025.jsonl && ! grep -aq "signtest u (D 16.25) exit" $X/exits_1025.txt; then
  bash $X/signtest1025.sh u
else
  log "batch: no D 16.25 record to signtest (or already done)"
fi
runcap() { # name cap logfile signtest-args...
  local name=$1 cap=$2 lg=$3; shift 3
  local pat=$1                                              # the state file, unique per row
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
  log "signtest row $name exit $rc wall $(( $(date +%s) - t ))s capped $capped"
}
while read -u 3 T K D DDDD; do
  runcap "$T D$D" 7200 $X/signtest_list.log $WX/st/sol_${T}_D${DDDD}.npy $D $K around=$WX/st/${T}.jsonl:$D:0.02 < /dev/null
done 3< $X/st/rows.txt
log "signtest batch done (11 rows)"
