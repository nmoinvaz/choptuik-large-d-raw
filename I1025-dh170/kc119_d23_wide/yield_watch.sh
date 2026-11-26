#!/bin/bash
# #1025 kc119_d23_wide, t5's yield rule: renice this lane's scan processes (cmdline matches $PATTERN) to 19 while an i1088a* unit is active on this machine (user or system scope; #1088 comes first).
# A user cannot lower a nice value again without privilege, so a process once reniced stays at 19 (harmless without contention). Logs transitions to yield.log. usage: yield_watch.sh [once]; env PATTERN, UNITGLOB, LOG for the test.
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
PATTERN=${PATTERN:-"^(/usr/bin/time -v )?$PY -u .*d18_hybsign\.py .*l1kc119macm3d23"}
UNITGLOB=${UNITGLOB:-'i1088a*'}
LOG=${LOG:-/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc119_d23_wide/yield.log}
active() { { systemctl --user list-units --state=active,activating --no-legend "$UNITGLOB" 2>/dev/null; systemctl list-units --state=active,activating --no-legend "$UNITGLOB" 2>/dev/null; } | awk 'NF {print $1}' | tr '\n' ' '; }
prev=""
while true; do
  u=$(active)
  if [ -n "$u" ]; then
    for pid in $(pgrep -f "$PATTERN"); do
      [ "$(ps -o ni= -p $pid | tr -d ' ')" = 19 ] || { renice -n 19 -p $pid > /dev/null 2>&1 && echo "$(date -u '+%F %T') UTC unit(s) active: $u: reniced pid $pid to 19" >> $LOG; }
    done
  fi
  [ "$u" != "$prev" ] && echo "$(date -u '+%F %T') UTC i1088a units active: [${u:-none}]" >> $LOG
  prev=$u
  [ "${1:-}" = once ] && exit 0
  sleep 20
done
