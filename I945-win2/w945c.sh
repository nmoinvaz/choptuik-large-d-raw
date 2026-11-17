#!/usr/bin/env bash
# #945 watcher (glue, never kills): returns when the second launch's plan_floor exits, on a Traceback, or after 1.5 h.
R=/d/choptuik-large-d-raw/I945-win2
t0=$(date +%s); why=none
while true; do
  grep -q '945b plan_floor exit' $R/exits_945.txt 2>/dev/null && { why="PLAN_FLOOR EXITED"; break; }
  grep -q Traceback $R/plan_floor.log 2>/dev/null && { why="TRACEBACK"; break; }
  [ $(( $(date +%s) - t0 )) -ge 5400 ] && { why="1.5 H HEARTBEAT"; break; }
  sleep 5
done
echo "$why at $(date -u '+%Y-%m-%d %H:%M:%S UTC')"; tail -3 $R/exits_945.txt | cut -c1-200; tail -9 $R/plan_floor.log | cut -c1-200
