#!/usr/bin/env bash
# #945 watcher (glue, never kills): returns when the third launch exits, on a Traceback, on each newton step line, or after 2 h.
R=/d/choptuik-large-d-raw/I945-win2
t0=$(date +%s); why=none
while true; do
  grep -q '945c plan_floor exit' $R/exits_945.txt 2>/dev/null && { why="PLAN_FLOOR EXITED"; break; }
  grep -q Traceback $R/plan_floor_newton.log 2>/dev/null && { why="TRACEBACK"; break; }
  [ $(( $(date +%s) - t0 )) -ge 7200 ] && { why="2 H HEARTBEAT"; break; }
  sleep 5
done
echo "$why at $(date -u '+%Y-%m-%d %H:%M:%S UTC')"; tail -3 $R/exits_945.txt | cut -c1-200; tail -40 $R/plan_floor_newton.log | cut -c1-220
