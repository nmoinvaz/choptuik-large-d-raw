#!/bin/bash
# watch_i1088a.sh: the coordinator's order (hc, 25 Nov): "If an i1088a unit starts, let it have its threads first". While this lane runs (until its "point done" or STOP line), when a systemd user unit i1088a-* is active this watcher raises the
# nice value of every thread (nice is per thread on Linux; renice_threads.sh) of this lane's own compute processes (the regrid's python, the scan's python) to 19 by exact pid, whenever a thread is below 19, writes a line to i1088a_yield.txt and tells the coordinator once. It stops and kills nothing.
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc111_d22875; T5="nathans-macbook-air-m5-3/t5"; told=0
while ! grep -q -E "kc111_d22875: (.*kc111 D 22.875 point done|STOP: )" $F/exits_kc111.txt 2>/dev/null; do
  if [ -n "$(systemctl --user list-units 'i1088a-*' --state=active --no-legend 2>/dev/null)" ]; then
    for p in $(ps -eo pid,cmd | awk '($2 ~ /python/) && (/ell_refine.py.*l1kc111dh610d22875/ || /d18_hybsign.py.*kc111dh610d22875/ || /d18_secant.py.*l1kc111dh610d22875/) {print $1}'); do
      if [ -n "$(ps -L -o ni= -p $p | awk '$1 < 19')" ]; then
        l=$(bash $F/renice_threads.sh $p) && echo "$(date -u '+%F %T') UTC an i1088a unit is active: $l ($(ps -o cmd= -p $p | cut -c1-60))" >> $F/i1088a_yield.txt
      fi
    done
    if [ $told = 0 ] && [ -s $F/i1088a_yield.txt ]; then told=1; hc send "$T5" "dh610 kc111_d22875 (auto): an i1088a unit is active: this lane's compute processes were reniced to 19 by exact pid ($(wc -l < $F/i1088a_yield.txt) so far, i1088a_yield.txt); nothing stopped." > /dev/null 2>&1; fi
  fi
  sleep 30
done
