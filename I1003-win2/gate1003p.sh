#!/usr/bin/env bash
# #1003 pilot, cap raised to 2.5 h (coordinator's hc of 2026-11-19 ~06:33 UTC: "raise your pilot's cap to 2.5 h now, don't restart it"). run1003p.sh's loop had a fixed cap of 3600 s, so I stopped that script's bash
# (pid 16736, by exact pid, the python was not touched) and this gate takes over its two jobs: it logs the pilot's end in exits_1003.txt and kills the python tree at 06:31:02 UTC + 9000 s (09:01:02 UTC),
# by the exact Windows pid in pilot.winpid (24596, the venv launcher stub whose child tree is the main python and the 8 spawn workers), after checking its command line. Glue, it computes nothing.
# usage: bash gate1003p.sh
X=/d/choptuik-large-d-raw-743/I1003-win2
log() { echo "1003p $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1003.txt; }
wpid=$(cat $X/pilot.winpid)
t0=$(date -u -d '2026-11-19 06:31:02' +%s)
cap=9000
alive() { powershell -NoProfile -Command "if (Get-Process -Id $wpid -ErrorAction SilentlyContinue) { 'yes' } else { 'no' }" | tr -d '\r'; }
log "gate1003p.sh took over the pilot's cap: 9000 s from 06:31:02 UTC (kill at 09:01:02 UTC) on pid $wpid"
capped=0
while [ "$(alive)" = "yes" ]; do
  if [ $(( $(date +%s) - t0 )) -ge $cap ]; then
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
    case "$cl" in
      *amp_flint_par.py*I1003-win2/pilot_K25_J1500.json*) log "pilot cap of ${cap} s reached, killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
      *) log "pid $wpid is not the pilot (command line: ${cl:0:80}), nothing killed";;
    esac
    break
  fi
  sleep 15
done
j=no; [ -f $X/pilot_K25_J1500.json ] && j=yes
log "pilot exit (python gone; its exit code is not seen by this gate) wall $(( $(date +%s) - t0 ))s capped $capped json $j"
