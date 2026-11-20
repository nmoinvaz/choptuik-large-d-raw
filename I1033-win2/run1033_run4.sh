#!/usr/bin/env bash
# #1033 run 4 (coordinator's hc of 2026-11-19, after run 3 met the condition: "after the cost steps and run 3's report, run run 4 (the two ladder jobs of notes/LOW_D_SPEEDUP.md 'Runs' at 32e5825d, side by side), then its report with --cost.
# Caps three times each estimate. Post run 3's report table, then run 4's."). The note's run 4 commands, from hp/ of D:/choptuik-i1033 at 32e5825d, venv-i600, 8 threads each, BelowNormal set by the launching PowerShell:
#   job A: solve A_M384 --pairs 0.9:320,0.8:320,0.7:320,0.8:256,0.7:256 --out solve_D3.0475.jsonl    (estimate 3.2 h, cap 9.6 h = 34560 s; the file already holds run 3's three records, the solve appends, as the note's command does)
#   job B: solve A_M384 --pairs 1:320,0.6:256,0.5:256,0.6:192,0.5:160,0.4:160,0.3:160,0.3:128,0.2:160,0.2:128 --out solve_D3.0475b.jsonl    (estimate 2.7 h, cap 8.1 h = 29160 s)
#   then report solve_D3.0475*.jsonl --ref A_M384 --ref2 A_M320 --cost cost2.jsonl --json report_D3.0475_run4.json (run 3's report_D3.0475.json stays; report cap 1800 s)
# Each job has its own log (run1033_run4a.log, run1033_run4b.log). Caps by exact pid: each job's root python (venv launcher stub) is found by rootpid1033p.ps1 from the job's own --out file name, and at the cap its tree is killed by that pid after
# its command line is checked. A cap that fires is reported with the last log line (the M it was on) and not retried; then no report is made and the script stops after both jobs ended. Exit codes of the solves are recorded (0 all converged, 1 some did not:
# a result), anything else is flagged UNEXPECTED. usage: bash run1033_run4.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
CODE=/d/choptuik-i1033
RAW=/d/choptuik-large-d-raw
X=$RAW/I1033-win2
WRAW=D:/choptuik-large-d-raw
OUT=$WRAW/I1033-win2
PS1=D:/choptuik-large-d-raw/I1033-win2/rootpid1033p.ps1
A=$WRAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "1033 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1033.txt; }
n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*tau_map_gain.py*' }).Count" | tr -d '\r')
[ "$n" = 0 ] || { log "run4 not started: $n tau_map_gain python processes are alive"; exit 9; }
[ -e $X/solve_D3.0475b.jsonl ] && { log "run4 not started: solve_D3.0475b.jsonl exists"; exit 9; }
[ -e $X/report_D3.0475_run4.json ] && { log "run4 not started: report_D3.0475_run4.json exists"; exit 9; }
grep -aq "v2 done" $X/exits_1033.txt || { log "run4 not started: v2 done is not in exits_1033.txt"; exit 9; }
cd $CODE || exit 9
[ "$(git rev-parse --short=8 HEAD)" = 32e5825d ] || { log "run4 not started: worktree is not at 32e5825d"; exit 9; }
cd $CODE/hp || exit 9
runjob() { # name pattern cap-seconds logfile tau_map_gain-args...
  local name=$1 pat=$2 cap=$3 lg=$4; shift 4
  echo "== $name: tau_map_gain.py $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
  local t=$(date +%s) capped=0 wpid="" i
  "$PY" -u tau_map_gain.py "$@" >> $lg 2>&1 &
  local pid=$!
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 3
    wpid=$(powershell -NoProfile -File "$PS1" -Pat "$pat" | tr -d '\r')
    [ -n "$wpid" ] && break
    kill -0 $pid 2>/dev/null || break
  done
  if [ -n "$wpid" ]; then echo "$wpid" > $X/run4_$name.winpid; log "$name root pid $wpid, cap ${cap} s"
  elif kill -0 $pid 2>/dev/null; then log "UNEXPECTED: root pid of $name not found while it runs, no cap possible (python left running)"; wait $pid; exit 1
  else log "$name ended within seconds, no root pid taken"; fi
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t )) -ge $cap ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *tau_map_gain.py*$pat*) log "$name CAP of ${cap} s reached, last log line: $(tail -n 1 $lg | cut -c1-160); last result line: $(grep -a ': Delta ' $lg | tail -n 1 | cut -c1-160); killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
        *) log "pid $wpid is not the $name command (command line: ${cl:0:80}), nothing killed";;
      esac
      break
    fi
    sleep 15
  done
  wait $pid
  local rc=$?
  log "$name exit $rc wall $(( $(date +%s) - t ))s capped $capped"
  [ "$capped" = 1 ] && exit 99
  exit $rc
}
log "run4 start, worktree $(git rev-parse --short=8 HEAD)"
runjob jobA solve_D3.0475.jsonl 34560 $X/run1033_run4a.log solve ${A}_M384.npz --pairs 0.9:320,0.8:320,0.7:320,0.8:256,0.7:256 --threads 8 --states $OUT/states --out $OUT/solve_D3.0475.jsonl &
pa=$!
sleep 40
runjob jobB solve_D3.0475b.jsonl 29160 $X/run1033_run4b.log solve ${A}_M384.npz --pairs 1:320,0.6:256,0.5:256,0.6:192,0.5:160,0.4:160,0.3:160,0.3:128,0.2:160,0.2:128 --threads 8 --states $OUT/states --out $OUT/solve_D3.0475b.jsonl &
pb=$!
wait $pa; ra=$?
wait $pb; rb=$?
log "run4 jobs ended: job A exit $ra, job B exit $rb (0 converged, 1 not all converged, 99 cap)"
for r in $ra $rb; do
  case $r in 0|1) ;; 99) log "run4 cap fired, no report, stopping (the coordinator decides)"; exit 1;; *) log "UNEXPECTED run4 job exit $r, no report, stopping"; exit 1;; esac
done
echo "== run4 report: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/run1033_run4a.log
t=$(date +%s)
"$PY" -u tau_map_gain.py report $OUT/solve_D3.0475.jsonl $OUT/solve_D3.0475b.jsonl --ref ${A}_M384.npz --ref2 ${A}_M320.npz --cost $OUT/cost2.jsonl --json $OUT/report_D3.0475_run4.json >> $X/run1033_run4_report.log 2>&1
log "run4 report exit $? wall $(( $(date +%s) - t ))s (report_D3.0475_run4.json, run1033_run4_report.log)"
log "run4 done"
