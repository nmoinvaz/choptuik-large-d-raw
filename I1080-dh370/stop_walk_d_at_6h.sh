#!/bin/bash
# #1080 walk d (t5's hc 2026-11-24): "if control_walk_d.jsonl has no row by 16:18 UTC (6 h), stop the unit and report its CPU time". The unit i1080d started 2026-11-24 10:18:02 UTC.
# At 16:18:02 UTC this checks control_walk_d.jsonl; with no row it records the CPU time of the unit and of its main process, stops unit i1080d (my own unit, by name), and writes WALK_D_STOPPED_6H.txt;
# with a row it writes WALK_D_ROW_BEFORE_6H.txt and does nothing. Unit i1080t. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1080-dh370
target=$(date -u -d '2026-11-24 16:18:02' +%s)
while [ $(date +%s) -lt $target ]; do sleep 30; done
if [ -s $OUT/control_walk_d.jsonl ]; then echo "a row exists at $(date -u '+%F %T') UTC; nothing stopped" > $OUT/WALK_D_ROW_BEFORE_6H.txt; exit 0; fi
{
  echo "no row in control_walk_d.jsonl at $(date -u '+%F %T') UTC (6 h after the start 10:18:02): stopping unit i1080d"
  echo "unit CPUUsageNSec $(systemctl --user show i1080d -p CPUUsageNSec --value) ns, ActiveEnterTimestamp $(systemctl --user show i1080d -p ActiveEnterTimestamp --value)"
  ps -eo pid,etime,cputime,pcpu,rss,args | grep -E 'zero_mp.py 2.72|multiprocessing.spawn' | grep -v grep | cut -c1-140
  echo "log: $(tail -2 $OUT/control_walk_d.log | cut -c1-200 | tr '\n' '|')"
} > $OUT/WALK_D_STOPPED_6H.txt 2>&1
systemctl --user stop i1080d
echo "stopped $(date -u '+%F %T') UTC: $(systemctl --user is-active i1080d)" >> $OUT/WALK_D_STOPPED_6H.txt
exit 0
}
