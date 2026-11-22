#!/bin/bash
{
# #1025 kc71_d1925up (dh610): the coordinator's task of 22 Nov, widening ../kc71_d1925 upward: d18_hybsign.py at D 19.25, k_c 71, win2's state (raw 8e4797ff), lambda 1.59 to 1.80 at 0.01 (22 values) plus a
# repeat of 1.65 (23 evaluations) over 6 processes of 1 thread, nice 10; value i goes to process i mod 6 (I1025-dh370/scan_hyb.sh's splitting; the repeat, index 22, runs on process 4 and its original,
# index 6, on process 0). No control here: it passed in ../kc71_d19125/control (same build, record file's D 19.0 row, script; D 19.0 lambda 1.55). The reading is dh170's read_lower.py.
# d18_hybsign.py is xfkappa's, blob e089207a, unmodified. usage: bash lane_kc71_1925up.sh [dry]
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc71_d1925up; IN=$F/in; C=$RAW/I1025-dh610/kc71_d19125
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
NP=6; CAP_SCAN=28800
L=$F/exits_kc71_1925up.txt
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc71_d1925up: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" \
          "$IN/sol_l1kc71Lw1025_D19.250000.npy 36bc6b837f1016f23f50948a7b1fb2b1bd172ade" "$IN/l1kc71Lw1025.jsonl c5fc14a93fe0ba51af16eeaca3887955eef7153e" \
          "$IN/read_lower.py 89309d3c8e4f758bb5f936f7d24796b594e4cbdb" \
          "$IN/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$IN/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$IN/repeat_check.py aaf598a98c05d8d67f740b5a3b0675b422daad6a"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
grep -q 'PASS: record system True' $C/control/control_check.txt || { say "refuse: the control in $C/control did not pass"; bad=1; }
for f in $F/scan/scan_D19.25_p0.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
LAMS=$($PY -c 'print(",".join([f"{round(1.59 + 0.01 * i, 2):.2f}" for i in range(22)] + ["1.65"]))'); NEV=23
# the pre-run checks of the controls: the reader's selftest and its two mutations, the repeat check's selftest
export D18_DIR=$IN
( cd $IN && $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  echo "$r0 $r1 $r2 $r3" > $F/selftest_exits.txt )
read r0 r1 r2 r3 < $F/selftest_exits.txt
[ $r0 = 0 ] && [ $r1 = 1 ] && [ $r2 = 1 ] && [ $r3 = 0 ] || { say "refuse: the selftests did not behave (read_lower $r0, mutate shift $r1, mutate round2 $r2, repeat_check $r3; wanted 0 1 1 0)"; bad=1; }
MAXRSS=$(awk '/Maximum resident set size/ {print $NF}' $C/control/control.raw)
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
if [ -z "$MAXRSS" ] || [ "$av" -lt $(( NP * MAXRSS + 4000000 )) ]; then say "refuse: MemAvailable $av kB is below $NP x the control's max RSS (${MAXRSS:-?} kB) + 4 GB"; bad=1; fi
[ $bad = 0 ] || exit 2
say "pins checked (inputs in in_blobs.txt, d18_hybsign e089207a, worktree 505d8399 clean, $PY, control of ../kc71_d19125 passed), selftests as wanted (exits $r0 $r1 $r2 $r3); MemAvailable $av kB, control max RSS $MAXRSS kB; lambda list $LAMS ($NEV evaluations over $NP processes of 1 thread, nice 10)"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
cd $W
say "scan: D 19.25, k_c 71, lambda $LAMS ($NEV evaluations), $NP processes of 1 thread, nice 10, cap ${CAP_SCAN} s each by exact pid"
mapfile -t LA < <(echo $LAMS | tr ',' '\n')
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LA[@]}; i += NP)); do mine="$mine,${LA[$i]}"; done
  mine=${mine#,}
  say "process $p: lambda $mine"
  ( nice -n 10 /usr/bin/time -v timeout -s TERM $CAP_SCAN $PY -u $IN/d18_hybsign.py $IN/l1kc71Lw1025.jsonl $IN/sol_l1kc71Lw1025_D19.250000.npy 19.25 $mine $F/scan/scan_D19.25_p$p.jsonl < /dev/null > $F/scan/scan_p$p.raw 2>&1
    echo "$(date -u '+%F %T') UTC process $p exit $?" >> $L ) &
  pids+=($!)
done
( while kill -0 ${pids[0]} 2>/dev/null || kill -0 ${pids[1]} 2>/dev/null || kill -0 ${pids[2]} 2>/dev/null || kill -0 ${pids[3]} 2>/dev/null || kill -0 ${pids[4]} 2>/dev/null || kill -0 ${pids[5]} 2>/dev/null; do
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*kc71_d1925up' | wc -l) python, RSS_kB $(ps -eo rss,cmd | awk '/d18_hybsign.py.*kc71_d1925up/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $(awk '/MemAvailable/ {print $2}' /proc/meminfo), load $(cut -d' ' -f1 /proc/loadavg), points $(cat $F/scan/scan_D19.25_p*.jsonl 2>/dev/null | wc -l)" >> $F/scan/sampler.log; sleep 60
  done ) &
wait "${pids[@]}"
for p in 0 1 2 3 4 5; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $F/scan/scan_p$p.raw > $F/scan/scan_p$p.log; head -1 $F/scan/scan_p$p.log | tee -a $L | cut -c1-200; done
cat $F/scan/scan_D19.25_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$F/scan/scan_D19.25_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# the reading: read_lower.py (dh170's, blob 89309d3c) on the six files, the repeat check on the merged file
cd $IN
{ echo "=== read_lower.py $F/scan 1.59 1.80"; $PY -W ignore read_lower.py $F/scan 1.59 1.80; echo "read_lower exit $?"
  echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $F/scan/scan_D19.25_1025.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
say "scan done; reading in read_lower.txt"
exit 0
}
