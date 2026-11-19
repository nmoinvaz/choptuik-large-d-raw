#!/usr/bin/env bash
# #1033 run 3: the 3 h cap by exact pid (coordinator's order). run1033_run3.sh recorded run3.winpid = 33892, which is its own forked bash stub, not the python (a mistake of that glue: its cap check, which wants "tau_map_gain.py ... solve" in the
# command line, would not match and would kill nothing). The job itself is not touched. This gate takes over the cap: at 18:37:05 UTC (the solve's start in exits_1033.txt) + 10800 s = 21:37:05 UTC it kills the tree of pid 32080
# (the venv-i600 launcher stub of the solve; its child 30900 is the main python), after checking that its command line holds tau_map_gain.py and solve. It ends when pid 32080 is gone. Glue, it computes nothing. usage: bash gate1033r3.sh
X=/d/choptuik-large-d-raw/I1033-win2
wpid=32080
t0=$(date -u -d '2026-11-19 18:37:05' +%s)
cap=10800
log() { echo "1033 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1033.txt; }
alive() { powershell -NoProfile -Command "if (Get-Process -Id $wpid -ErrorAction SilentlyContinue) { 'yes' } else { 'no' }" | tr -d '\r'; }
log "gate1033r3.sh took over the run 3 cap: ${cap} s from 18:37:05 UTC (kill at 21:37:05 UTC) on pid $wpid"
while [ "$(alive)" = "yes" ]; do
  if [ $(( $(date +%s) - t0 )) -ge $cap ]; then
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
    case "$cl" in
      *tau_map_gain.py*solve*) log "run3 cap of ${cap} s reached, killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1;;
      *) log "pid $wpid is not the run 3 solve (command line: ${cl:0:80}), nothing killed";;
    esac
    break
  fi
  sleep 15
done
log "gate1033r3 ends (pid $wpid gone or capped)"
