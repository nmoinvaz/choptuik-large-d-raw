#!/bin/bash
# #948 (coordinator, 2026-11-17): a down rung is capped at 2 h wall and an up rung at 3 h. This watcher kills the rung's anm_run.py when its
# age passes the cap, writes the cap line (the rung's last max|F| and lam, caprep948.py) to exits_948.txt and touches RUNG.capped. The
# ladder scripts then see a rung that failed: up stops (a capped +20 rung falls back to +10), down falls back (run948_down2.sh).
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I948-dh370
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
while true; do
  ps -eo pid=,etimes=,args= | grep -E "^ *[0-9]+ +[0-9]+ +[^ ]*python[^ ]* -u anm_run.py" | grep "/I948-dh370/" | grep -v grep | while read pid age rest; do
    dir=$(echo "$rest" | sed -nE 's#.*/I948-dh370/((up|down)_K[0-9]+_from[0-9]+) .*#\1#p'); [ -z "$dir" ] && continue
    case $dir in down_*) cap=7200 ;; *) cap=10800 ;; esac
    if [ "$age" -gt $cap ]; then
      rep=$("$PY" "$OUT/caprep948.py" "$OUT/$dir.log" 2>&1 | cut -c1-600)
      touch "$OUT/$dir.capped"
      echo "948 $dir capped at $cap s wall, killed (pid $pid): $rep $(date -u '+%F %T')" >> "$OUT/exits_948.txt"
      kill "$pid"
    fi
  done
  sleep 30
done
