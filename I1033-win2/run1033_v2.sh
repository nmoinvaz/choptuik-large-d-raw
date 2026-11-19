#!/usr/bin/env bash
# #1033, the rerun at perf/tau-map-lowd 32e5825d (coordinator's comment 7022166701 on #1033 and hc: after #1031's build ends, start at 32e5825d, not f53fb5bf; the bot reviews' fixes rename the checkpoints (they carry the map centre s0),
# bind them to their configuration and tighten the report). Order: (1) run 0: selftest exit 0 and each of its eight controls (lo parity dps40 inverse gp phase_gp lenient unbound) exit 1; (2) run 3: solve A_M384 --pairs 1:384,0.4:192,0.5:192, 3 h cap;
# (3) the cost steps: step 1 `cost A_M320 A_M384 --threads 8 --reps 2` (cap 1.5 h), step 2 its control `--mutate plan_m` (exit 1, no record, cap 10 min), step 3 `cost S37_M128/160/192/256 A_M256` (cap 45 min), all into cost2.jsonl;
# (4) run 3's report with --cost cost2.jsonl. Then it stops (no run 1 again, no run 4). From hp/ of D:/choptuik-i1033, venv-i600's python (its hpkernel read-only), 8 threads, BelowNormal set by the launching PowerShell and inherited, no nice.
# Caps by exact pid: each command's python is started directly, its root pid (the venv launcher stub) is found by rootpid1033.ps1, and at the cap its tree is killed by that pid after its command line is checked. A cap that fires is reported with the M it
# was on (last log line) and not retried; the script then stops. Run 0 must pass entirely before run 3 starts. Run 3's solve exit 0 or 1 (a map that did not converge is a result, not a crash) goes on to the cost steps; any other exit stops the script.
# Exit codes expected: steps 1 and 3 exit 0, step 2 exit 1 with no record written; the report is recorded whatever it exits (it exits 1 when a check fails). usage: bash run1033_v2.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
CODE=/d/choptuik-i1033
RAW=/d/choptuik-large-d-raw
X=$RAW/I1033-win2
WRAW=D:/choptuik-large-d-raw
OUT=$WRAW/I1033-win2
L=$X/run1033.log
PS1=D:/choptuik-large-d-raw/I1033-win2/rootpid1033.ps1
A=$WRAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475
S37=data/lowD_states/highm15_D3.7000
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "1033 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1033.txt; }
n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*tau_map_gain.py*' }).Count" | tr -d '\r')
[ "$n" = 0 ] || { log "v2 not started: $n tau_map_gain python processes are alive"; exit 9; }
for f in solve_D3.0475.jsonl cost2.jsonl cost2_control.jsonl report_D3.0475.json; do [ -e $X/$f ] && { log "v2 not started: $f exists"; exit 9; }; done
ls $X/states | grep -q 'D3.0475' && { log "v2 not started: D3.0475 checkpoints exist in states/"; exit 9; }
cd $CODE || exit 9
git checkout --detach 32e5825d >> $L 2>&1 || { log "v2: git checkout 32e5825d failed"; exit 9; }
[ "$(git rev-parse --short=8 HEAD)" = 32e5825d ] || { log "v2: worktree is not at 32e5825d"; exit 9; }
cd $CODE/hp || exit 9
cstage() { # name accepted-exits(space separated, or any) cap-seconds tau_map_gain-args...
  local name=$1 want=$2 cap=$3; shift 3
  echo "== $name: tau_map_gain.py $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
  local t=$(date +%s) capped=0 wpid="" i
  "$PY" -u tau_map_gain.py "$@" >> $L 2>&1 &
  local pid=$!
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 3
    wpid=$(powershell -NoProfile -File "$PS1" | tr -d '\r')
    [ -n "$wpid" ] && break
    kill -0 $pid 2>/dev/null || break
  done
  if [ -n "$wpid" ]; then echo "$wpid" > $X/v2.winpid; log "$name root pid $wpid, cap ${cap} s"
  elif kill -0 $pid 2>/dev/null; then log "UNEXPECTED: root pid of $name not found while it runs, no cap possible, stopping the script (python left running)"; exit 1
  else log "$name ended within seconds, no root pid taken"; fi
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t )) -ge $cap ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *tau_map_gain.py*) log "$name cap of ${cap} s reached, last log line: $(tail -n 1 $L | cut -c1-160); last M line: $(grep -a ' f64 Jacobian ' $L | tail -n 1 | cut -c1-120); killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
        *) log "pid $wpid is not the $name command (command line: ${cl:0:80}), nothing killed";;
      esac
      break
    fi
    sleep 15
  done
  wait $pid
  RC=$?
  log "$name exit $RC (accepted: $want) wall $(( $(date +%s) - t ))s capped $capped"
  [ "$capped" = 1 ] && { log "UNEXPECTED: cap fired at $name, stopping, no retry"; exit 1; }
  if [ "$want" != any ]; then case " $want " in *" $RC "*) ;; *) log "UNEXPECTED exit at $name, stopping"; exit 1;; esac; fi
}
log "v2 start, worktree $(git rev-parse --short=8 HEAD)"
# run 0
cstage "run0 selftest" 0 900 selftest
for m in lo parity dps40 inverse gp phase_gp lenient unbound; do cstage "run0 selftest control $m" 1 600 selftest --mutate $m; done
log "run0 passed: selftest exit 0, its eight controls exit 1"
# run 3
cstage "run3 solve 1:384,0.4:192,0.5:192" "0 1" 10800 solve ${A}_M384.npz --pairs 1:384,0.4:192,0.5:192 --threads 8 --states $OUT/states --out $OUT/solve_D3.0475.jsonl
R3=$RC
# cost steps
cstage "cost step1 M320 M384" 0 5400 cost ${A}_M320.npz ${A}_M384.npz --threads 8 --reps 2 --out $OUT/cost2.jsonl
cstage "cost step2 control plan_m" 1 600 cost ${A}_M320.npz ${A}_M384.npz --mutate plan_m --out $OUT/cost2_control.jsonl
if [ -s $X/cost2_control.jsonl ]; then log "UNEXPECTED: the plan_m control wrote a record, stopping"; exit 1; fi
log "cost step2 control wrote no record (as required)"
cstage "cost step3 D3.7 M128-256 and A M256" 0 2700 cost ${S37}_M128.npz ${S37}_M160.npz ${S37}_M192.npz ${S37}_M256.npz ${A}_M256.npz --threads 8 --reps 2 --out $OUT/cost2.jsonl
# report
cstage "run3 report with cost2" any 1800 report $OUT/solve_D3.0475.jsonl --ref ${A}_M384.npz --ref2 ${A}_M320.npz --cost $OUT/cost2.jsonl --json $OUT/report_D3.0475.json
log "v2 done (run 3 solve exit $R3, report exit $RC)"
