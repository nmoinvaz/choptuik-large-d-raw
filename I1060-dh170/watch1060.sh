#!/bin/bash
# #1060 on dh170: sampler and priority rule for the anm_run of run1060_dh170.sh (alert-only: it logs, stops nothing).
# Every 30 s one line into memlog_1060.log: MemAvailable, swap used, the python child's RSS, its CPU time and nice; ALERT lines (alert1060.log) at MemAvailable under 3, 2 and 1 GiB, one per new level.
# Priority rule (coordinator, 21 Nov: "when leg 13's next state lands, #1057's read goes first"): while the #1057 lane's last record in exits_1057.txt is a start without its exit, every thread of the python child is
# reniced to 19 (a state read runs at nice 10); otherwise to 10 (the order's nice). Changes are logged in prio1060.log. No pattern kills or pgrep: the python child is the child of the time pid in time_pid.txt.
OUT=/home/nathan/Source/choptuik-large-d-raw/I1060-dh170
L1057=/home/nathan/Source/choptuik-large-d-raw/I1057-dh170/exits_1057.txt
while [ ! -s $OUT/time_pid.txt ]; do sleep 5; done
tp=$(cat $OUT/time_pid.txt); lvl=0; cur=10; n=0
echo "# $(date -u '+%F %T') UTC watch1060 start, time pid $tp" >> $OUT/memlog_1060.log
while kill -0 $tp 2>/dev/null; do
  py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' ')
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); sw=$(awk '/SwapTotal/ {t=$2} /SwapFree/ {f=$2} END {print int((t-f)/1024)}' /proc/meminfo)
  if [ -n "$py" ] && [ -d /proc/$py ]; then
    rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status); ni=$(ps -o ni= -p $py | tr -d ' '); cpu=$(ps -o cputime= -p $py | tr -d ' ')
    last=$(grep -E '^1057 c3b_.* (start|exit) ' $L1057 | tail -n 1); want=10; case "$last" in *" start "*) want=19;; esac
    if [ "$want" != "$cur" ]; then
      for t in /proc/$py/task/*; do renice -n $want -p ${t##*/} > /dev/null 2>&1; done
      echo "$(date -u '+%F %T') UTC python pid $py nice $cur -> $want (#1057 last record: $(echo "$last" | cut -c1-60))" >> $OUT/prio1060.log; cur=$want
    fi
  else rss=0; ni=-; cpu=-; fi
  echo "$(date -u '+%T') MemAvailable $av MiB, swap used $sw MiB, python pid ${py:-none} RSS $rss MiB, cputime $cpu, nice $ni" >> $OUT/memlog_1060.log
  new=0; [ "$av" -lt 3072 ] && new=1; [ "$av" -lt 2048 ] && new=2; [ "$av" -lt 1024 ] && new=3
  if [ "$new" -gt "$lvl" ]; then echo "ALERT $(date -u '+%F %T') UTC #1060 run: MemAvailable $av MiB (level $new of 3: under 3, 2, 1 GiB), swap used $sw MiB; nothing stopped" >> $OUT/alert1060.log; lvl=$new; fi
  n=$((n+1)); sleep 30
done
echo "# $(date -u '+%F %T') UTC watch1060 end: the time pid $tp is gone" >> $OUT/memlog_1060.log
