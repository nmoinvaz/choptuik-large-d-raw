#!/bin/bash
# watch_i1088a_r25.sh: the coordinator's order (hc, 25 Nov): "Run at nice 19 under the i1088a yield watcher; the quest comes first." While the r1 0.25 recount's argcount python runs (it appears after the lane's selftests), whenever a
# systemd user unit i1088a-* is active this watcher sets nice 19 on every thread (nice is per thread on Linux; renice_threads.sh) of that python and of all its descendants, by exact pid and tid, whenever a thread is below 19, and
# writes a line per pid to i1088a_yield.txt. It stops and kills nothing; it ends when the lane's exits.txt has the lane's "r25 done" or "STOP:" line after its start, or when the unit i1076r25 is no longer active after it saw a python (the lane runs two recounts one after the other, so a python that is gone does not end it).
F=/home/nathan/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_corner_r25; told=0; seen=0; R=""
root() { ps -eo pid,cmd | awk '($2 ~ /python/) && /argcount.py .*--tag=M3_fu022mp_r25_/ {print $1}' | head -1; }
kids() { ps -eo pid=,ppid= | awk -v r=$1 '{pp[$1]=$2; ids[n++]=$1} END {s[r]=1; ch=1; while (ch) {ch=0; for (i=0;i<n;i++) {p=ids[i]; if (!(p in s) && (pp[p] in s)) {s[p]=1; ch=1}}} for (p in s) print p}'; }
n0=$(grep -c -E "fu022mp_corner_r25: (.*r25 done|STOP: )" $F/exits.txt 2>/dev/null || true)
echo "$(date -u '+%F %T') UTC watch_i1088a_r25: started, nothing is stopped"
while :; do
  [ "$(grep -c -E "fu022mp_corner_r25: (.*r25 done|STOP: )" $F/exits.txt 2>/dev/null || true)" -gt "${n0:-0}" ] && break
  r=$(root)
  if [ -n "$r" ]; then R=$r; seen=1; elif [ $seen = 1 ] && [ "$(systemctl --user is-active i1076r25)" != active ]; then break; fi
  if [ -n "$R" ] && [ -d /proc/$R ] && [ -n "$(systemctl --user list-units 'i1088a-*' --state=active --no-legend 2>/dev/null)" ]; then
    for p in $(kids $R); do
      [ -d /proc/$p ] || continue
      case $(ps -o stat= -p $p 2>/dev/null) in Z*|'') continue;; esac
      if [ -n "$(ps -L -o ni= -p $p 2>/dev/null | awk '$1 < 19')" ]; then
        l=$(bash $F/renice_threads.sh $p) && echo "$(date -u '+%F %T') UTC an i1088a unit is active: $l ($(ps -o args= -p $p | cut -c1-50))" >> $F/i1088a_yield.txt
      fi
    done
  fi
  sleep 30
done
echo "$(date -u '+%F %T') UTC watch_i1088a_r25: the lane has ended, watcher ends"
