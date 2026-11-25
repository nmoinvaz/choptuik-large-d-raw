#!/bin/bash
# watch_i1088a.sh: the coordinator's order (hc, 25 Nov): "If an i1088a unit starts, let it have its threads first". While this lane runs (until its "point done" or STOP line), when a systemd user unit i1088a-* is active this watcher raises the
# nice value of this lane's own compute processes (the regrid's python, the scan's python) to 19 by exact pid, once per process, writes a line to i1088a_yield.txt and tells the coordinator once. It stops and kills nothing.
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc95_d22375; T5="nathans-macbook-air-m5-3/t5"; told=0
while ! grep -q -E "kc95_d22375: (.*kc95 D 22.375 point done|STOP: )" $F/exits_kc95.txt 2>/dev/null; do
  if [ -n "$(systemctl --user list-units 'i1088a-*' --state=active --no-legend 2>/dev/null)" ]; then
    for p in $(ps -eo pid,ni,cmd | awk '($3 ~ /python/) && (/ell_refine.py.*l1kc95dh610d22375/ || /d18_hybsign.py.*kc95dh610d22375/) && $2 < 19 {print $1}'); do
      renice -n 19 -p $p > /dev/null 2>&1 && echo "$(date -u '+%F %T') UTC an i1088a unit is active: pid $p reniced to 19 ($(ps -o cmd= -p $p | cut -c1-60))" >> $F/i1088a_yield.txt
    done
    if [ $told = 0 ] && [ -s $F/i1088a_yield.txt ]; then told=1; hc send "$T5" "dh610 kc95_d22375 (auto): an i1088a unit is active: this lane's compute processes were reniced to 19 by exact pid ($(wc -l < $F/i1088a_yield.txt) so far, i1088a_yield.txt); nothing stopped." > /dev/null 2>&1; fi
  fi
  sleep 30
done
