#!/usr/bin/env bash
# #945 rerun-of-step-2 watcher with the file's stop rules (I926-mac/runner_task_M320.md), as w932b.sh: after the leg's start line, kill the leg's python tree
# on a failed pass ("failed at M", the code's halving after 8 Newton calls or a give-up) or after 30 h; notify on a pair record, STOP, Traceback, exit or a 3 h heartbeat.
X=/d/choptuik-large-d-raw/I945-win2
R=$X/leg
cnt() { if [ -f "$1" ]; then wc -l < "$1"; else echo 0; fi; }
until grep -q '945f rerun of step 2 (--accept 1e-20) start' $X/exits_945.txt 2>/dev/null; do sleep 10; done
n0=$(cnt $R/leg.jsonl); f0=$(grep -c 'failed at M' $R/leg.log); e0=$(cnt $X/exits_945.txt); t0=$(date +%s); dl=${DL:-$(( t0 + 30*3600 ))}; why=none; kill=0
while true; do
  [ "$(cnt $R/leg.jsonl)" -gt "$n0" ] && { why="NEW leg.jsonl RECORD (a pair or a stop record)"; break; }
  [ "$(grep -c 'failed at M' $R/leg.log)" -gt "$f0" ] && { why="A PASS FAILED (failed at M, the code halves): stopping the leg as the file says"; kill=1; break; }
  grep -q -E '^[0-9:]+ STOP:' $R/leg.log && { why="STOP LINE"; break; }
  grep -q Traceback $R/leg.log && { why="TRACEBACK"; break; }
  tail -n +$((e0+1)) $X/exits_945.txt | grep -q 'rerun of step 2 exit' && { why="RERUN EXITED"; break; }
  [ "$(date +%s)" -ge "$dl" ] && { why="30 H CAP"; kill=1; break; }
  [ $(( $(date +%s) - t0 )) -ge 10800 ] && { why="3 H HEARTBEAT"; break; }
  sleep 5
done
if [ $kill -eq 1 ]; then
  pid=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*I945-win2/leg/states*' } | Sort-Object ProcessId | Select-Object -First 1).ProcessId")
  [ -n "$pid" ] && MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1
  echo "945f rerun of step 2 leg stopped by win2b at the file's stop rule: $why (python tree of pid ${pid:-none}) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_945.txt
fi
echo "$why at $(date -u '+%Y-%m-%d %H:%M:%S UTC')"; tail -3 $X/exits_945.txt | cut -c1-250; tail -6 $R/leg.log | cut -c1-250
