#!/bin/bash
# watch_i1088a_recount.sh: the coordinator's order (hc, 25 Nov): "put the recount i1076d under the fixed yield watcher: renice its 12 processes to 19 while any i1088a unit is active (nothing stopped)".
# While the recount's argcount python runs, whenever a systemd user unit i1088a-* is active this watcher raises the nice value of every thread (nice is per thread on Linux; renice_threads.sh) of that python and of all its descendants
# (the 12 spawn workers) to 19 by exact pid and tid, whenever a thread is below 19; it writes a line per pid to i1088a_yield.txt and tells the coordinator once. It stops and kills nothing. Nice can be raised but not lowered by this user, so a process
# stays at 19 after the unit ends. It exits when the recount's python is gone.
F=/home/nathan/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_m3mp; T5="nathans-macbook-air-m5-3/t5"; told=0
root() { ps -eo pid,cmd | awk '($2 ~ /python/) && /argcount.py --M=3 --recount=.*M3_fu022mp_m3mp_r0.17/ {print $1}' | head -1; }
kids() { ps -eo pid=,ppid= | awk -v r=$1 '{pp[$1]=$2; ids[n++]=$1} END {s[r]=1; ch=1; while (ch) {ch=0; for (i=0;i<n;i++) {p=ids[i]; if (!(p in s) && (pp[p] in s)) {s[p]=1; ch=1}}} for (p in s) print p}'; }
R=$(root); [ -n "$R" ] || { echo "$(date -u '+%F %T') UTC watch_i1088a_recount: no recount python found"; exit 1; }
echo "$(date -u '+%F %T') UTC watch_i1088a_recount: root pid $R, nothing is stopped"
while [ -d /proc/$R ]; do
  if [ -n "$(systemctl --user list-units 'i1088a-*' --state=active --no-legend 2>/dev/null)" ]; then
    for p in $(kids $R); do
      [ -d /proc/$p ] || continue
      case $(ps -o stat= -p $p 2>/dev/null) in Z*|'') continue;; esac
      if [ -n "$(ps -L -o ni= -p $p 2>/dev/null | awk '$1 < 19')" ]; then
        l=$(bash $F/renice_threads.sh $p) && echo "$(date -u '+%F %T') UTC an i1088a unit is active: $l ($(ps -o args= -p $p | cut -c1-50))" >> $F/i1088a_yield.txt
      fi
    done
    if [ $told = 0 ] && [ -s $F/i1088a_yield.txt ]; then told=1; hc send "$T5" "dh610 recount i1076d (auto): an i1088a unit is active: the recount's processes were reniced to 19 by exact pid and tid ($(wc -l < $F/i1088a_yield.txt) so far, i1088a_yield.txt); nothing stopped." > /dev/null 2>&1; fi
  fi
  sleep 30
done
echo "$(date -u '+%F %T') UTC watch_i1088a_recount: recount python $R gone, watcher ends"
