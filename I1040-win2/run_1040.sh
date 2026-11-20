#!/bin/bash
# I1040 on win2: the coordinator's check of PR #1047 (#1040's timing fix), from hp/ of D:\choptuik-i1034 (main 9980cd93) with venv-i1034's hpkernel (the #1034 build), BelowNormal inherited.
# The coordinator's hc (2026-11-20 ~14:20 UTC): run it FIRST when the build ends, while win2 is quiet (win2b holds off), then #1034's steps 5 and 2; post both exits on #1040 with the machine's load during the run.
# Quiet gate (fixed before the run, the coordinator's "load under 2" read as under 2 busy threads of 20, i.e. total CPU under 10%): before the first command the total CPU % is averaged over 3 samples 2 s apart,
# every 30 s, and the check starts when two consecutive averages are under 10%. If that has not happened within 2700 s the check is NOT run (logged, summary line "NOT RUN"), step 5 goes on, and I tell the coordinator
# and run the pair later when the machine is quiet; it is never run on a busy machine as its "once". load_watch1040.ps1 logs the machine's load every 5 s into load.log from the start of the gate to the end.
# Commands, once each: step_timing_check.py --reps=3 --threads=4 (want exit 0), then --reps=2 --threads=4 --mutate=drop (want exit 1, check 1 FAIL; the coordinator's prediction for a quiet machine: only check 1 fails).
# Caps by the exact root pid, command line checked for step_timing_check.py: 900 s and 600 s (the estimate is "a few minutes in all", three times).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1040-win2
. $OUT/lib1040.sh
V=/c/Users/nathan/Source/venv-i1034
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1034
export PATH="$V/Scripts:$PATH"
PY=C:/Users/nathan/Source/venv-i1034/Scripts/python.exe
cd /d/choptuik-i1034/hp || exit 1
stamp() { date -u '+%F %T'; }
load() { powershell -NoProfile -Command "\$c=(Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 3).CounterSamples.CookedValue; 'total cpu % (3 samples, 2 s apart): ' + (\$c | % { [math]::Round(\$_,1) }) -join ' '; 'available GB: ' + [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1); 'python processes: ' + ((Get-Process python -ErrorAction SilentlyContinue | Measure-Object).Count)" | tr -d '\r'; }
avgcpu() { powershell -NoProfile -Command "(1..3 | % { (Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter \"Name='_Total'\").PercentProcessorTime; Start-Sleep -Seconds 2 } | Measure-Object -Average).Average" | tr -d '\r'; }
echo "# run_1040 start $(stamp) UTC, hp $(git rev-parse HEAD)" >> $SUM
powershell -NoProfile -ExecutionPolicy Bypass -File "D:/choptuik-i935-raw/I1040-win2/load_watch1040.ps1" -Out "D:/choptuik-i935-raw/I1040-win2" -DoneFile "D:/choptuik-i935-raw/I1040-win2/step_timing.done" &
SAMPLER=$!
# the quiet gate
t0=$(date +%s); ok=0; prev=999
while [ $(( $(date +%s) - t0 )) -lt 2700 ]; do
  v=$(avgcpu); v=${v:-999}
  log "gate: total cpu average $v % (need two in a row under 10)"
  if awk "BEGIN{exit !($v<10)}"; then if awk "BEGIN{exit !($prev<10)}"; then ok=1; break; fi; fi
  prev=$v; sleep 30
done
if [ $ok = 0 ]; then
  echo "step_timing, step_timing_drop: NOT RUN, the machine was not quiet (total CPU under 10% twice in a row) within 2700 s; last average $v %" >> $SUM
  log "NOT RUN: machine not quiet within 2700 s (last total cpu average $v %)"
  echo "# run_1040 done (not run) $(stamp) UTC" >> $SUM
  touch $OUT/step_timing.done; exit 0
fi
log "gate passed after $(( $(date +%s) - t0 )) s (total cpu averages $prev and $v %)"
run() {
  local name=$1 want=$2 cap=$3; shift 3
  { echo "# $(stamp) UTC hp worktree $(git rev-parse --short HEAD), python $PY"
    echo "# load before:"; load | sed 's/^/#   /'
    echo "# cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s)
  crun "$name" $want $cap step_timing_check.py "$PY" -u "$@" >> $OUT/$name.log 2>&1
  echo "exit $RC" >> $OUT/$name.log
  { echo "# load after:"; load | sed 's/^/#   /'; } >> $OUT/$name.log
  echo "$name: expected exit $want, got $RC, $(( $(date +%s) - s )) s capped $CAPPED $([ $RC = $want ] && echo OK || echo MISMATCH), window $(date -u -d @$s '+%F %T') to $(stamp) UTC" >> $SUM
}
run step_timing 0 900 step_timing_check.py --reps=3 --threads=4
run step_timing_drop 1 600 step_timing_check.py --reps=2 --threads=4 --mutate=drop
echo "# run_1040 done $(stamp) UTC" >> $SUM
touch $OUT/step_timing.done
