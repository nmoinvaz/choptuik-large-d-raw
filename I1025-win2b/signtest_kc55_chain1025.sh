#!/usr/bin/env bash
# #1025 signtests, second chain (coordinator's hc ~08:35 UTC 20 Nov: the 4 k_c 55 rows (l1kc55Fb1025 at D 15, 15.5, 16, 16.5) come back to win2b, to run beside the k_c 47 chain, 4 BLAS threads, same extraction by git show (st/, hashes in
# st/hashes.txt), same pass rule; dh170 posts any row it finished and win2b skips those). Rows in st/rows_kc55.txt in REVERSE order (D 16.5 first), because dh170 (comment 7034479811 on #1025) runs them forward from D 15, so the two meet
# in the middle. Before each row: git fetch of the raw clone (no checkout) and a look at dh170's raw I1025-dh170/signtest.log (both JSON lines of that state present = skip), and the file st/skip_kc55.txt (one "tag D" per line, which I fill
# from dh170's #1025 posts). From solver/matter of D:/choptuik-i1025b, venv-i962, 4 BLAS threads, BelowNormal (set by the launching PowerShell), one at a time, each signtest capped at 7200 s by the exact pid of its python.
# Output appended to signtest_list_kc55.log, one exits_1025.txt line per row. usage: bash signtest_kc55_chain1025.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
WX=D:/choptuik-large-d-raw/I1025-win2b
RAW=/d/choptuik-large-d-raw-743p
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
  log "signtest row $name exit $rc wall $(( $(date +%s) - t ))s capped $capped"
}
while read -u 3 T K D DDDD; do
  git -C $RAW fetch -q origin 2>/dev/null
  have=$(git -C $RAW show origin/main:I1025-dh170/signtest.log 2>/dev/null | grep -ac "\"state\": \"sol_${T}_D${DDDD}.npy\"")
  if [ "${have:-0}" -ge 2 ]; then log "kc55 chain: row $T D$D skipped, dh170's raw signtest.log already has both lines"; continue; fi
  if grep -aqx "$T $D" $X/st/skip_kc55.txt 2>/dev/null; then log "kc55 chain: row $T D$D skipped (listed in st/skip_kc55.txt after dh170's post)"; continue; fi
  runcap "$T D$D" 7200 $X/signtest_list_kc55.log $WX/st/sol_${T}_D${DDDD}.npy $D $K around=$WX/st/${T}.jsonl:$D:0.02 < /dev/null
done 3< $X/st/rows_kc55.txt
log "signtest kc55 chain done"
