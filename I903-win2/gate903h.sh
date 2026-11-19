#!/usr/bin/env bash
# #903 stop gate (glue, coordinator's hc of 2026-11-19 ~01:27 UTC: "stop ks_chain2 when its current attempt ends, by exact pids, logs kept"): it waits for the next attempt line (" -> D ") of leg 3's
# anm_run.log beyond the count at its start, gives an accepted attempt up to 90 s to write its saved-state line, then kills the process tree of ks_chain.py pid 13236 (exact pid, checked against its
# command line before the kill) and logs the stop in exits_903.txt. It starts and kills nothing else. usage: bash gate903h.sh
R=/d/choptuik-large-d-raw/I903-win2
L=$R/ks_chain2/leg03_D242.0000_ks299/anm_run.log
PID=13236
n0=$(grep -c ' -> D ' $L)
while [ "$(grep -c ' -> D ' $L)" -le "$n0" ]; do sleep 5; done
last=$(grep ' -> D ' $L | tail -1 | cut -c1-120)
if echo "$last" | grep -q 'stall accepted'; then
  for i in $(seq 1 18); do tail -n 3 $L | grep -q 'Delta of the saved state' && break; sleep 5; done
else sleep 10; fi
cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$PID\").CommandLine")
case "$cl" in *ks_chain.py*I903-win2/ks_chain2*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $PID > /dev/null 2>&1; st="killed the tree of pid $PID";; *) st="pid $PID is not my ks_chain.py (command line: ${cl:0:80}), nothing killed";; esac
echo "903h ks_chain2 stopped by win2b at the end of its attempt (coordinator's order): $st; last attempt line: $last $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_903.txt
echo "$st at $(date -u +%H:%M:%S)"; tail -2 $R/exits_903.txt | cut -c1-300
