#!/bin/bash
# #1025 D 17.75 scan on dh170 (watch1060.sh with the file names of this run; the renice logs the nice read back, since a user cannot lower nice): sampler and priority rule for the anm_run of lane_d1775_dh170.sh (alert-only: it logs, stops nothing).
# Every 30 s one line into memlog_scan.log: MemAvailable, swap used, the python child's RSS, its CPU time and nice; ALERT lines (alert_scan.log) at MemAvailable under 3, 2 and 1 GiB, one per new level.
# Priority rule (coordinator, 21 Nov: "when leg 13's next state lands, #1057's read goes first"): while the #1057 lane's last record in exits_1057.txt is a start without its exit, every thread of the python child is
# reniced to 19 (a state read runs at nice 10); otherwise to 10 (the order's nice). Changes are logged in prio_scan.log. No pattern kills or pgrep: the python child is the child of the time pid in time_pid_scan.txt.
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/d1775
L1057=/home/nathan/Source/choptuik-large-d-raw/I1057-dh170/exits_1057.txt
while [ ! -s $OUT/time_pid_scan.txt ]; do sleep 5; done
tp=$(cat $OUT/time_pid_scan.txt); lvl=0; cur=10; n=0
echo "# $(date -u '+%F %T') UTC watch1060 start, time pid $tp" >> $OUT/memlog_scan.log
while kill -0 $tp 2>/dev/null; do
  py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' ')
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); sw=$(awk '/SwapTotal/ {t=$2} /SwapFree/ {f=$2} END {print int((t-f)/1024)}' /proc/meminfo)
  if [ -n "$py" ] && [ -d /proc/$py ]; then
    rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status); ni=$(ps -o ni= -p $py | tr -d ' '); cpu=$(ps -o cputime= -p $py | tr -d ' ')
    last=$(grep -E '^1057 c3b_.* (start|exit) ' $L1057 | tail -n 1); want=10; case "$last" in *" start "*) want=19;; esac
    if [ "$want" != "$cur" ] && [ "$want" -gt "$cur" ]; then
      for t in /proc/$py/task/*; do renice -n $want -p ${t##*/} > /dev/null 2>&1; done
      now=$(ps -o ni= -p $py | tr -d ' ')
      echo "$(date -u '+%F %T') UTC python pid $py: asked nice $want, nice read back $now (it was $cur; #1057 last record: $(echo "$last" | cut -c1-60))" >> $OUT/prio_scan.log; cur=$now
    fi
  else rss=0; ni=-; cpu=-; fi
  echo "$(date -u '+%T') MemAvailable $av MiB, swap used $sw MiB, python pid ${py:-none} RSS $rss MiB, cputime $cpu, nice $ni" >> $OUT/memlog_scan.log
  new=0; [ "$av" -lt 3072 ] && new=1; [ "$av" -lt 2048 ] && new=2; [ "$av" -lt 1024 ] && new=3
  if [ "$new" -gt "$lvl" ]; then echo "ALERT $(date -u '+%F %T') UTC #1025 scan: MemAvailable $av MiB (level $new of 3: under 3, 2, 1 GiB), swap used $sw MiB; nothing stopped" >> $OUT/alert_scan.log; lvl=$new; fi
  n=$((n+1)); sleep 30
done
echo "# $(date -u '+%F %T') UTC watch1060 end: the time pid $tp is gone" >> $OUT/memlog_scan.log
