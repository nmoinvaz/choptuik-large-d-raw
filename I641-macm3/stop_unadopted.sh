#!/bin/bash
# #641, the coordinator's go (message 1794561510140-0, 2026-11-13 09:18 UTC): stop the chain step of any run whose octo-double base polish is not adopted
# ("base polish not adopted" in its log), keeping the polish record. Checks every 20 s for 6 h; writes stops.txt (which run, when).
R=/Users/nathan/Source/choptuik-large-d-raw-641/I641-macm3
for i in $(seq 1 1080); do
  for lg in $R/K*_D*.log; do
    case $lg in *first*|*attempt*) continue ;; esac
    tag=$(basename $lg .log)
    grep -q "base polish not adopted" $lg 2>/dev/null || continue
    grep -q "^$tag " $R/stops.txt 2>/dev/null && continue
    pid=$(ps -axo pid,command | grep "anm_run.py" | grep "/I641-macm3/$tag " | grep -v grep | grep -v caffeinate | grep -v "bash -c" | awk '{print $1}' | head -1)
    if [ -n "$pid" ]; then
      kill -TERM $pid
      echo "$tag stopped at $(date -u +%FT%TZ): base polish not adopted ($(grep -m1 'base polish not adopted' $lg | cut -c1-90)); pid $pid killed" >> $R/stops.txt
    fi
  done
  sleep 20
done
