#!/bin/bash
{
# #1025 d19125 (dh610): the coordinator's task of 22 Nov: the hybrid sign scan at D 19.125 (k_c 63), lambda 1.505 to 1.545 at 0.0025 (17 values) plus a repeat of 1.525 (18 evaluations),
# 6 processes of 1 thread, nice 10; value i goes to process i mod 6 (I1025-dh370/scan_hyb.sh's splitting; the repeat, index 17, runs on process 5 and its original, index 8, on process 2).
# No control rerun (the coordinator): same machine and build as the D 19.09375 scan (I1025-dh610/d1909, control passed). d18_hybsign.py is xfkappa's, blob e089207a, unmodified. usage: bash lane_d19125.sh [dry]
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/d19125; IN=$F/in
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
NP=6; CAP_SCAN=28800
L=$F/exits_d19125.txt
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC d19125: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$IN/sol_l1kc63dh370_D19.125000.npy 832e07e483bc5e2a731261e15c49f74f3cf137b6" \
          "$IN/l1kc63dh370.jsonl 11454d97ce024164af7e0acbb0d0ee2bc5704dc5" "$IN/read_lower.py 89309d3c8e4f758bb5f936f7d24796b594e4cbdb" \
          "$IN/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$IN/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$IN/repeat_check.py aaf598a98c05d8d67f740b5a3b0675b422daad6a"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
[ -e $F/scan/scan_D19.125_p0.jsonl ] && { say "refuse: scan files exist"; bad=1; }
LAMS=$($PY -c 'print(",".join([f"{round(1.505 + 0.0025 * i, 4):.4f}" for i in range(17)] + ["1.5250"]))'); NEV=18
# the pre-run checks: the reader's selftest and mutations, the repeat check's selftest, and the planted four-decimal grid (plain must pass, both mutations must fail)
export D18_DIR=$IN
( cd $IN && $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  cd $F && $PY plant_grid4.py > $F/selftest_plant_grid4.log 2>&1; r4=$?
  $PY plant_grid4.py --mutate=shift > $F/selftest_plant_grid4_mutate_shift.log 2>&1; r5=$?
  $PY plant_grid4.py --mutate=round2 > $F/selftest_plant_grid4_mutate_round2.log 2>&1; r6=$?
  echo "$r0 $r1 $r2 $r3 $r4 $r5 $r6" > $F/selftest_exits.txt )
read r0 r1 r2 r3 r4 r5 r6 < $F/selftest_exits.txt
[ $r0 = 0 ] && [ $r1 = 1 ] && [ $r2 = 1 ] && [ $r3 = 0 ] && [ $r4 = 0 ] && [ $r5 = 1 ] && [ $r6 = 1 ] || { say "refuse: the selftests did not behave (read_lower $r0, mutate shift $r1, mutate round2 $r2, repeat_check $r3, plant_grid4 $r4, its shift $r5, its round2 $r6; wanted 0 1 1 0 0 1 1)"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (inputs in in_blobs.txt, d18_hybsign e089207a, worktree 505d8399 clean, $PY), selftests as wanted (exits $r0 $r1 $r2 $r3 $r4 $r5 $r6); lambda list $LAMS ($NEV evaluations over $NP processes of 1 thread, nice 10)"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( NP * 1500000 + 4000000 )) ] || { say "STOP: MemAvailable $av kB is below $NP x 1.5 GB + 4 GB (the D 19.09375 processes peaked at 1.36 GB): no scan"; exit; }
cd $W
say "scan: D 19.125, lambda $LAMS ($NEV evaluations), $NP processes of 1 thread, nice 10, cap ${CAP_SCAN} s each by exact pid"
mapfile -t LA < <(echo $LAMS | tr ',' '\n')
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LA[@]}; i += NP)); do mine="$mine,${LA[$i]}"; done
  mine=${mine#,}
  say "process $p: lambda $mine"
  ( nice -n 10 /usr/bin/time -v timeout -s TERM $CAP_SCAN $PY -u $IN/d18_hybsign.py $IN/l1kc63dh370.jsonl $IN/sol_l1kc63dh370_D19.125000.npy 19.125 $mine $F/scan/scan_D19.125_p$p.jsonl < /dev/null > $F/scan/scan_p$p.raw 2>&1
    echo "$(date -u '+%F %T') UTC process $p exit $?" >> $L ) &
  pids+=($!)
done
( while kill -0 ${pids[0]} 2>/dev/null || kill -0 ${pids[1]} 2>/dev/null || kill -0 ${pids[2]} 2>/dev/null || kill -0 ${pids[3]} 2>/dev/null || kill -0 ${pids[4]} 2>/dev/null || kill -0 ${pids[5]} 2>/dev/null; do
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*19.125' | wc -l) python, RSS_kB $(ps -eo rss,cmd | awk '/d18_hybsign.py.*19.125/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $(awk '/MemAvailable/ {print $2}' /proc/meminfo), load $(cut -d' ' -f1 /proc/loadavg), points $(cat $F/scan/scan_D19.125_p*.jsonl 2>/dev/null | wc -l)" >> $F/scan/sampler.log; sleep 60
  done ) &
wait "${pids[@]}"
for p in 0 1 2 3 4 5; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $F/scan/scan_p$p.raw > $F/scan/scan_p$p.log; head -1 $F/scan/scan_p$p.log | tee -a $L | cut -c1-200; done
cat $F/scan/scan_D19.125_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$F/scan/scan_D19.125_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# the reading: read_lower.py (dh170's, blob 89309d3c) on the six files, the repeat check on the merged file, and the table with the smallest ln|det|
cd $IN
{ echo "=== read_lower.py $F/scan 1.505 1.545"; $PY -W ignore read_lower.py $F/scan 1.505 1.545; echo "read_lower exit $?"
  echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $F/scan/scan_D19.125_1025.jsonl; echo "repeat_check exit $?"
  echo "=== table (exact lambdas)"
  $PY -I -c "
import json
rows = [json.loads(l) for l in open('$F/scan/scan_D19.125_1025.jsonl')]
for r in rows: print(f\"{r['lam']:.4f} hybrid {r['sign']:+.0f} ln|det| {r['ln']:.10f} noise {r['noise']} float64 {r['f64_sign']:+.0f} {r['f64_ln']:.6f} {r['sec']} s\")
m = min(rows, key=lambda r: r['ln']); print('smallest ln|det|: lambda', m['lam'], 'hybrid', m['sign'], 'ln', m['ln'])
"; } > $F/read_lower.txt 2>&1
say "scan done; reading in read_lower.txt"
exit 0
}
