#!/bin/bash
# #1025 kc95_d1975 (dh610), step 2 of the coordinator's order of 23 Nov: d18_hybsign.py at D 19.75, k_c 95, on the regridded state and record that regrid/VERDICT.txt accepted (their blobs are in in_blobs_regrid.txt),
# lambda 1.30 to 1.36 at 0.01 (7 values) plus a repeat of 1.33 (8 evaluations) over 4 processes of 1 thread, nice 10; value i goes to process i mod 4 (I1025-dh370/scan_hyb.sh's splitting; this is the order's split: p0 1.30,
# 1.34; p1 1.31,1.35; p2 1.32,1.36; p3 1.33 and its repeat, the repeat placed last on the same process as the original). The lane starts only after regrid/VERDICT.txt reads ACCEPTED and the D 19.5 scan (unit
# i1025u) has ended; it waits for both (6 h cap) and stops if the regrid is REFUSED. The reading is dh170's read_lower.py. d18_hybsign.py is xfkappa's, blob e089207a, unmodified. Free memory: the lane refuses to
# start with less than 4 x 4 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes scan/MEMALERT.txt, which the runner session posts to
# the coordinator. usage: bash lane_kc95_scan.sh [dry]   (dry waits for the same two conditions)
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc95_d1975; IN=$F/in
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
NP=4; CAP_SCAN=28800; RSS_GUESS=4000000; MEMSTOP=4194304
L=$F/exits_kc95_scan.txt
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc95_d1975 scan: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
# the order's two conditions: the regrid is ACCEPTED (regrid/VERDICT.txt) and the D 19.5 scan (unit i1025u) has ended
say "waiting for regrid/VERDICT.txt ACCEPTED and the end of unit i1025u (the D 19.5 scan); the wait is capped at 6 h"
tw=$(date +%s)
while true; do
  v=$(head -1 $F/regrid/VERDICT.txt 2>/dev/null)
  case "$v" in REFUSED*) say "stop: the regrid was refused ($v); the scan is not started"; exit 2;; esac
  case "$v" in ACCEPTED*) [ "$(systemctl --user is-active i1025u)" = active ] || break;; esac
  [ $(( $(date +%s) - tw )) -lt 21600 ] || { say "stop: the wait of 6 h ended without the two conditions"; exit 2; }
  sleep 60
done
say "conditions met: $(head -1 $F/regrid/VERDICT.txt), unit i1025u $(systemctl --user is-active i1025u); the D 19.5 scan's last line: $(tail -1 $RAW/I1025-dh610/kc95_d195/exits_kc95_scan.txt | cut -c1-80)"
bad=0
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" \
          "$IN/read_lower.py 89309d3c8e4f758bb5f936f7d24796b594e4cbdb" "$IN/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" \
          "$IN/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$IN/repeat_check.py aaf598a98c05d8d67f740b5a3b0675b422daad6a"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
# the regridded state and record: the blobs written into in_blobs_regrid.txt when the regrid was accepted
[ -f $F/in_blobs_regrid.txt ] || { say "refuse: in_blobs_regrid.txt is missing"; bad=1; }
while read b f; do [ -f $IN/$f ] && [ "$(hb $IN/$f)" = "$b" ] || { say "refuse: $IN/$f missing or not blob $b"; bad=1; }; done < $F/in_blobs_regrid.txt
[ "$(wc -l < $F/in_blobs_regrid.txt)" = 2 ] || { say "refuse: in_blobs_regrid.txt does not list the state and the record"; bad=1; }
head -1 $F/regrid/VERDICT.txt | grep -q '^ACCEPTED' || { say "refuse: regrid/VERDICT.txt is not ACCEPTED"; bad=1; }
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $F/scan/scan_D19.75_p0.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
LAMS=$($PY -c 'v = [f"{round(1.30 + 0.01 * i, 2):.2f}" for i in range(7)]; print(",".join(v + ["1.33"]))'); NEV=8
# the pre-run checks of the controls: the reader's selftest and its two mutations, the repeat check's selftest
export D18_DIR=$IN
( cd $IN && $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  echo "$r0 $r1 $r2 $r3" > $F/selftest_exits.txt )
read r0 r1 r2 r3 < $F/selftest_exits.txt
[ $r0 = 0 ] && [ $r1 = 1 ] && [ $r2 = 1 ] && [ $r3 = 0 ] || { say "refuse: the selftests did not behave (read_lower $r0, mutate shift $r1, mutate round2 $r2, repeat_check $r3; wanted 0 1 1 0)"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
if [ "$av" -lt $(( NP * RSS_GUESS + 4000000 )) ]; then say "refuse: MemAvailable $av kB is below $NP x $RSS_GUESS kB (a guess above k_c 87's 2.9 GB peak) + 4 GB"; bad=1; fi
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs.txt, in_blobs_regrid.txt, d18_hybsign e089207a, worktree 505d8399 clean, $PY, regrid/VERDICT.txt: $(head -1 $F/regrid/VERDICT.txt | cut -c1-40)), selftests as wanted (exits $r0 $r1 $r2 $r3); MemAvailable $av kB; lambda list $LAMS ($NEV evaluations over $NP processes of 1 thread, nice 10)"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
cd $W
say "scan: D 19.75, k_c 95, lambda $LAMS ($NEV evaluations), $NP processes of 1 thread, nice 10, cap ${CAP_SCAN} s each by exact pid"
mapfile -t LA < <(echo $LAMS | tr ',' '\n')
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LA[@]}; i += NP)); do mine="$mine,${LA[$i]}"; done
  mine=${mine#,}
  say "process $p: lambda $mine"
  ( nice -n 10 /usr/bin/time -v timeout -s TERM $CAP_SCAN $PY -u $IN/d18_hybsign.py $IN/l1kc95dh610d1975.jsonl $IN/sol_l1kc95dh610d1975_D19.7500.npy 19.75 $mine $F/scan/scan_D19.75_p$p.jsonl < /dev/null > $F/scan/scan_p$p.raw 2>&1
    echo "$(date -u '+%F %T') UTC process $p exit $?" >> $L ) &
  pids+=($!)
done
( while kill -0 ${pids[0]} 2>/dev/null || kill -0 ${pids[1]} 2>/dev/null || kill -0 ${pids[2]} 2>/dev/null || kill -0 ${pids[3]} 2>/dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*kc95_d1975' | wc -l) python, RSS_kB $(ps -eo rss,cmd | awk '/d18_hybsign.py.*kc95_d1975/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $F/scan/scan_D19.75_p*.jsonl 2>/dev/null | wc -l)" >> $F/scan/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/scan/MEMALERT.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for p in 0 1 2 3; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $F/scan/scan_p$p.raw > $F/scan/scan_p$p.log; head -1 $F/scan/scan_p$p.log | tee -a $L | cut -c1-200; done
cat $F/scan/scan_D19.75_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$F/scan/scan_D19.75_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# the reading: read_lower.py (dh170's, blob 89309d3c) on the four files, the repeat check on the merged file
cd $IN
{ echo "=== read_lower.py $F/scan 1.30 1.36"; $PY -W ignore read_lower.py $F/scan 1.30 1.36; echo "read_lower exit $?"
  echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $F/scan/scan_D19.75_1025.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
say "scan done; reading in read_lower.txt"
exit 0
}
