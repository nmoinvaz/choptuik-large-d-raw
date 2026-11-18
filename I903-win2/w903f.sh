#!/usr/bin/env bash
# #903 restarted-chain watcher (w903e.sh with the pattern ^903[ef], for run903f.sh) (glue, never kills): notifies on a new 903e line of exits_903.txt, a new ks_chain2 leg record, a Traceback in ks_chain2.log or its
# leg logs, or a 3 h heartbeat.
R=/d/choptuik-large-d-raw/I903-win2
cnt() { local n; n=$(grep -cE "$1" "$2" 2>/dev/null); echo ${n:-0}; }
jl() { if [ -f $R/ks_chain2/ks_chain.jsonl ]; then wc -l < $R/ks_chain2/ks_chain.jsonl; else echo 0; fi; }
n0=$(cnt '^903[ef] ' $R/exits_903.txt); j0=$(jl); t0=$(date +%s); why=none
while true; do
  [ "$(cnt '^903[ef] ' $R/exits_903.txt)" -gt "$n0" ] && { why="NEW 903e LINE"; break; }
  [ "$(jl)" -gt "$j0" ] && { why="NEW ks_chain2 LEG RECORD"; break; }
  grep -qs Traceback $R/ks_chain2.log $R/ks_chain2/leg*/anm_run.log && { why="TRACEBACK"; break; }
  [ $(( $(date +%s) - t0 )) -ge 10800 ] && { why="3 H HEARTBEAT"; break; }
  sleep 10
done
echo "$why at $(date -u '+%Y-%m-%d %H:%M:%S UTC')"; grep '^903[ef] ' $R/exits_903.txt | tail -4 | cut -c1-300
