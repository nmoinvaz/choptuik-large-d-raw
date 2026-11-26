#!/bin/bash
# stage_scan.sh (kc111_d22875, dh610): the coordinator's order of 26 Nov (hc): the scan uses `d18_secant.py scan` (branch wip/ell1-speed at 92b9bf53, blob eb1396ad), not d18_hybsign.py. 6 evaluations (lambda 0.06 to 0.14 by 0.02 and a repeat of 0.12)
# on 4 processes of 1 thread (nice 10, raised to 19 by watch_i1088a.sh while an i1088a unit is active), cap 43200 s each, then the merged file and the reading (read_lower.py, repeat_check.py, leg_read.py against PRED 0.12, bar 0.02).
# Read when the stage starts. Exit 0 when the scan and the reading are done (no robust change is a reading, not a failure), 1 on a failed process.
source /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc111_d22875/common_kc111.sh
export D18_DIR=$IN
if [ -n "$(systemctl --user list-units 'i1088a-*' --state=active --no-legend 2>/dev/null)" ]; then say "an i1088a unit is active: the scan processes are reniced to 19 by watch_i1088a.sh"; fi
tw=$(date +%s)
while :; do
  av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
  [ "$av" -ge $(( NP * RSS_GUESS + 4000000 )) ] && break
  [ -e $F/scan_mem_wait.txt ] || say "waiting for memory: MemAvailable $av kB is below $NP x $RSS_GUESS kB + 4 GB (nothing is stopped)"
  echo "$(stamp) UTC MemAvailable $av kB" > $F/scan_mem_wait.txt
  [ $(( $(date +%s) - tw )) -lt 21600 ] || halt "the memory wait before the scan ended after 6 h"
  sleep 60
done
say "scan memory gate passed (MemAvailable $av kB, waited $(( $(date +%s) - tw )) s, load $(cut -d' ' -f1-3 /proc/loadavg))"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1; unset P4_WT_MATTER
SST=$IN/sol_${TAG}_D${DS}.npy; SREC=$IN/$TAG.jsonl; SB=$(blob $SST); RB=$(blob $SREC)
LISTS=("0.12,0.08" "0.10,0.06" "0.14" "0.12")
say "scan (d18_secant.py scan, blob $(blob $SWM/d18_secant.py | cut -c1-8), the fast float64 matrix, ell_ddm's block 12, pins ${SB:0:8},${RB:0:8}): lambda 0.06 to 0.14 by 0.02 and a repeat of 0.12 (6 evaluations), lists ${LISTS[*]}, $NP processes of 1 thread, nice 10, cap 43200 s each"
pids=()
for ((j = 0; j < NP; j++)); do
  ( cd $SWM && nice -n 10 /usr/bin/time -v timeout -s TERM 43200 $PY -u d18_secant.py scan $SREC $SST $D ${LISTS[$j]} $S/scan_D${D}_p$j.jsonl --pin=$SB,$RB < /dev/null > $S/scan_p$j.raw 2>&1
    echo "$(stamp) UTC scan p$j (${LISTS[$j]}) exit $?" >> $L ) &
  pids+=($!)
done
( sleep 10; while pgrep -f "d18_secant.py scan.*sol_${TAG}_D${DS}" > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(stamp) UTC alive $(pgrep -f "d18_secant.py scan.*sol_${TAG}_D${DS}" | wc -l), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/scan_D${D}_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(stamp) UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_scan.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for ((j = 0; j < NP; j++)); do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_p$j.raw > $S/scan_p$j.log; say "p$j: $(grep -E 'record system|pin|Maximum resident' $S/scan_p$j.raw | head -2 | cut -c1-150 | tr '\n' ' ')"; done
[ "$(cat $S/scan_D${D}_p*.jsonl 2>/dev/null | wc -l)" = 6 ] || halt "the scan wrote $(cat $S/scan_D${D}_p*.jsonl 2>/dev/null | wc -l) records, 6 wanted (see scan_p*.raw and the exits above)"
cat $S/scan_D${D}_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D${D}_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
( cd $IN; { echo "=== read_lower.py $S 0.06 0.14"; $PY -W ignore read_lower.py $S 0.06 0.14; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $S/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
  $PY -I leg_read.py read $F/read_lower.txt $PRED $BAR > $F/leg_read.txt 2>&1 )
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|against the prediction' $F/leg_read.txt | tr '\n' ' ' | cut -c1-500)"
[ "$(grep -c '   change (' $F/leg_read.txt)" = 0 ] && say "no robust change in the window (the order: report, do not widen): reported as read"
bash $PUSH I1025-dh610/kc111_d22875 "I1025-dh610/kc111_d22875: D 22.875 scan rows and reading" > $F/push_scan.txt 2>&1
exit 0
