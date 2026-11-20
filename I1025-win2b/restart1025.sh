#!/usr/bin/env bash
# #1025: waits for win2-build's rustc to pass its peak, then restarts the D 16.25 solve (coordinator's hc ~06:46 UTC: "restart D 16.25 after win2-build's build has passed its peak (its rustc falls below 10 GiB) or ended").
# Trigger: the largest rustc working set was at least 25 GiB at some check (the peak seen) and is below 10 GiB at two checks 30 s apart, and commit is under 92 GiB (or no rustc and no cargo process is left after the peak).
# It does not restart if the D 16.75 solve is gone (stopped or ended): it logs that and exits so that I report it. On the restart it runs run1025b.sh and appends a line to README.md. usage: bash restart1025.sh
X=/d/choptuik-large-d-raw/I1025-win2b
P=D:/choptuik-large-d-raw/I1025-win2b
peak=0; low=0
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
while true; do
  ra=$(powershell -NoProfile -File "$P/rootpid1025.ps1" -Pat l1kc55Fv1025 | tr -d '\r')
  if [ -z "$ra" ]; then log "restart watcher: the D 16.75 solve is gone, D 16.25 not restarted (stop, end or cap of D 16.75: see exits_1025.txt)"; exit 0; fi
  r=$(powershell -NoProfile -File "$P/mem1025b.ps1" -Root $ra | tr -d '\r'); set -- $r
  free=$1; com=$2; rs=$6
  nc=$(powershell -NoProfile -Command "@(Get-Process -Name rustc,cargo -ErrorAction SilentlyContinue).Count" | tr -d '\r')
  [ "$(awk "BEGIN{print ($rs>=25)}")" = "1" ] && peak=1
  if [ "$peak" = 1 ] && { [ "$(awk "BEGIN{print ($rs<10)}")" = "1" ] || [ "${nc:-1}" = 0 ]; }; then low=$((low+1)); else low=0; fi
  if [ "$low" -ge 2 ] && [ "$(awk "BEGIN{print ($com<92)}")" = "1" ]; then
    log "restart watcher: rustc peak seen and now $rs GiB (cargo/rustc processes $nc), free $free GiB, commit $com GiB: restarting D 16.25"
    echo "- $(date -u '+%Y-%m-%d %H:%M UTC'): D 16.25 restarted by restart1025.sh (win2-build's rustc fell to $rs GiB after its peak; free $free GiB, commit $com GiB); new root pid in D16.25.winpid, 43200 s cap from the restart." >> $X/README.md
    exec bash $X/run1025b.sh
  fi
  sleep 30
done
