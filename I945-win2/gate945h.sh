#!/usr/bin/env bash
# #945 decision gate (coordinator's hc, 2026-11-18 ~13:45 UTC): on M 384 pass 1's next Newton line (step 3, due near 14:04 UTC), if its start |F| is below 1e-6 leave the leg
# running, if not stop the leg cleanly (the leg's python tree only, logs kept). It acts only on that line; with no line by 16:00 UTC or after the leg's exit it does nothing.
X=/d/choptuik-large-d-raw/I945-win2
R=$X/leg
log() { echo "945h $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_945.txt; }
n0=$(grep -c '^  newton ' $R/leg.log)
dl=$(date -u -d '2026-11-18 16:00:00' +%s)
while true; do
  [ "$(grep -c '^  newton ' $R/leg.log)" -gt "$n0" ] && break
  grep -q '945g resume of step 2 exit' $X/exits_945.txt && { echo "leg exited before the line"; exit 0; }
  [ "$(date +%s)" -ge "$dl" ] && { echo "NO LINE BY 16:00 UTC, no action"; log "gate: no step 3 line by 16:00 UTC, no action"; exit 0; }
  sleep 5
done
line=$(grep '^  newton ' $R/leg.log | sed -n "$((n0+1))p")
f=$(echo "$line" | sed -n 's/.*|F| \([0-9.e+-]*\) .*/\1/p')
echo "step 3 line: $line"
if awk -v f="$f" 'BEGIN { exit !(f + 0 < 1e-6) }'; then
  log "gate: step 3 line start |F| $f is below 1e-6, the leg is left running"
  echo "LET IT RUN: start |F| $f below 1e-6"
else
  pid=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*I945-win2/leg/states*' } | Sort-Object ProcessId | Select-Object -First 1).ProcessId")
  [ -n "$pid" ] && MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1
  log "gate: step 3 line start |F| $f is not below 1e-6, the leg's python tree (pid ${pid:-none}) stopped by win2b as the coordinator ordered"
  echo "STOPPED: start |F| $f not below 1e-6, pid ${pid:-none}"
fi
