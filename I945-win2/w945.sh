#!/usr/bin/env bash
# #945 watcher (glue, never kills): returns on the _fail state's six records, an exit, a Traceback, or after 2 h.
R=/d/choptuik-large-d-raw/I945-win2
cnt() { if [ -f "$1" ]; then wc -l < "$1"; else echo 0; fi; }
t0=$(date +%s); why=none
while true; do
  [ "$(cnt $R/plan_floor.jsonl)" -ge 6 ] && { why="THE _fail STATE'S SIX RECORDS ARE WRITTEN"; break; }
  grep -q 'plan_floor exit' $R/exits_945.txt 2>/dev/null && { why="PLAN_FLOOR EXITED"; break; }
  grep -q Traceback $R/plan_floor.log 2>/dev/null && { why="TRACEBACK"; break; }
  [ $(( $(date +%s) - t0 )) -ge 7200 ] && { why="2 H HEARTBEAT"; break; }
  sleep 5
done
echo "$why at $(date -u '+%Y-%m-%d %H:%M:%S UTC')"; cat $R/exits_945.txt 2>/dev/null | cut -c1-200; cat $R/plan_floor.log 2>/dev/null | tail -12 | cut -c1-200
