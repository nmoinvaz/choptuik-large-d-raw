#!/usr/bin/env bash
# #1025 P4 (amendment 7), win2b: fallback caps by exact pid for the driver's p4_hybrid.py rows. The driver (blob e004c9ec) caps its rows with `timeout`; the standing rule is caps by exact pid
# (taskkill /T /F after a command-line check). Every 30 s: each root python of a running p4_hybrid.py older than its cap + 120 s (cross-check row 14400 s, k_c 71 row 43200 s, any other 43200 s) is killed by its exact pid
# after its command line is read again. Nothing is stopped for memory. Ends when the driver log says "p4_driver_rows.sh done" or at 17 h. One exits_1025.txt line per kill. usage: bash p4cap1025.sh
X=/d/choptuik-large-d-raw/I1025-win2b
WX=D:/choptuik-large-d-raw/I1025-win2b
LOG=$X/p4/p4_w.log
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
t0=$(date +%s)
log "P4 fallback cap watcher started (cross 14400+120 s, kc71 43200+120 s, by exact pid; no memory stop)"
while [ $(( $(date +%s) - t0 )) -lt 61200 ]; do
  grep -aq "p4_driver_rows.sh done" $LOG 2>/dev/null && { log "P4 fallback cap watcher ends: the driver is done"; exit 0; }
  powershell -NoProfile -File "$WX/p4prio1025.ps1" | tr -d '\r' | while read -r pid what; do log "P4 priority: pid $pid $what (the driver's nice -n 10 gives Idle, ordered BelowNormal)"; done
  powershell -NoProfile -File "$WX/p4roots1025.ps1" | tr -d '\r' | while read -r pid age kind; do
    [ -z "$pid" ] && continue
    case $kind in cross) cap=${P4CAP_CROSS:-14520};; *) cap=${P4CAP_OTHER:-43320};; esac
    if [ "$age" -ge "$cap" ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$pid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *p4_hybrid.py*) log "P4 CAP fallback: root pid $pid ($kind row) is $age s old, cap $cap s, killing its tree"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1;;
        *) log "P4 cap watcher: pid $pid is not a p4_hybrid.py command (${cl:0:80}), nothing killed";;
      esac
    fi
  done
  sleep ${P4POLL:-30}
done
log "P4 fallback cap watcher ends: 17 h reached"
