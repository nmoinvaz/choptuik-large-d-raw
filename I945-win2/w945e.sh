#!/usr/bin/env bash
# #945 watcher (glue, never kills): returns when the third launch exits, on a Traceback, on a second "newton" line, or after 3 h.
R=/d/choptuik-large-d-raw/I945-win2
t0=$(date +%s); why=none
while true; do
  grep -q '945c plan_floor exit' $R/exits_945.txt 2>/dev/null && { why="PLAN_FLOOR EXITED"; break; }
  grep -q Traceback $R/plan_floor_newton.log 2>/dev/null && { why="TRACEBACK"; break; }
  [ $(grep -c '^  newton ' $R/plan_floor_newton.log 2>/dev/null) -ge 2 ] && { why="NEW NEWTON LINE"; break; }
  [ $(( $(date +%s) - t0 )) -ge 10800 ] && { why="3 H HEARTBEAT"; break; }
  sleep 5
done
echo "$why at $(date -u '+%Y-%m-%d %H:%M:%S UTC')"; tail -3 $R/exits_945.txt | cut -c1-200; grep '^  newton ' $R/plan_floor_newton.log | cut -c1-250; tail -5 $R/plan_floor_newton.log | cut -c1-220
