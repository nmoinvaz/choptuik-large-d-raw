#!/bin/bash
{
# #1025 d1909 (dh610): the coordinator's task of 22 Nov. 1. the control: d18_hybsign.py at D 19.0, lambda 1.55 on dh370's state and record, 1 process (must read the record system and hybrid +1,
# ln|det| = dh370's to 1e-6 relative); 2. the scan at D 19.09375, lambda 1.480 to 1.540 at 0.005 (13 values) plus a repeat of 1.510 (14 evaluations) over 6 processes of 1 thread, nice 10; 3. the reading.
# The splitting of the lambdas over the processes is I1025-dh370/scan_hyb.sh's (blob 4be62f86, in/): value i goes to process i mod 6, the repeat (index 13) lands on process 1, the original of 1.510 (index 6) on process 0.
# d18_hybsign.py is xfkappa's, blob e089207a, unmodified. usage: bash lane_d1909.sh [dry]
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/d1909; IN=$F/in
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
NP=6; CAP_CONTROL=10800; CAP_SCAN=28800
L=$F/exits_d1909.txt
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC d1909: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$IN/sol_l1kc63dh370_D19.093750.npy 5583a185932c6d9f684e4f60f2c5119921bf5050" \
          "$IN/sol_l1kc63dh370_D19.000000.npy 589b55d75eac5b333eb5cec5bdf34b5771faeca7" "$IN/l1kc63dh370.jsonl d75eade533a7ff902360aa40bf246862eaace1c6" \
          "$IN/ref_dh370_scan_D19.000000_p0.jsonl 2b9be2cb5272fd8e2f43a6c88c697bc2bda6d72f" "$IN/read_lower.py 89309d3c8e4f758bb5f936f7d24796b594e4cbdb" \
          "$IN/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$IN/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$IN/repeat_check.py aaf598a98c05d8d67f740b5a3b0675b422daad6a"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $F/control/scan_D19.0_p0.jsonl $F/scan/scan_D19.09375_p0.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
LAMS=$($PY -c 'print(",".join([f"{1.480 + 0.005 * i:.3f}" for i in range(13)] + ["1.510"]))'); NEV=14
# the pre-run checks of the controls: the reader's selftest and its two mutations, the repeat check's selftest, the control check's selftest and mutation
export D18_DIR=$IN
( cd $IN && $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  cd $F && $PY control_check.py selftest > $F/selftest_control_check.log 2>&1; r4=$?
  $PY control_check.py selftest --mutate > $F/selftest_control_check_mutate.log 2>&1; r5=$?
  echo "$r0 $r1 $r2 $r3 $r4 $r5" > $F/selftest_exits.txt )
read r0 r1 r2 r3 r4 r5 < $F/selftest_exits.txt
[ $r0 = 0 ] && [ $r1 = 1 ] && [ $r2 = 1 ] && [ $r3 = 0 ] && [ $r4 = 0 ] && [ $r5 = 1 ] || { say "refuse: the selftests did not behave (read_lower $r0, mutate shift $r1, mutate round2 $r2, repeat_check $r3, control_check $r4, its mutate $r5; wanted 0 1 1 0 0 1)"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (inputs in in_blobs.txt, d18_hybsign e089207a, worktree 505d8399 clean, $PY), selftests as wanted (exits $r0 $r1 $r2 $r3 $r4 $r5); lambda list $LAMS ($NEV evaluations over $NP processes of 1 thread, nice 10)"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
cd $W
# 1. the control, 1 process
say "1. control: D 19.0, lambda 1.55, 1 process, cap ${CAP_CONTROL} s by exact pid"
t0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout -s TERM $CAP_CONTROL $PY -u $IN/d18_hybsign.py $IN/l1kc63dh370.jsonl $IN/sol_l1kc63dh370_D19.000000.npy 19.0 1.55 $F/control/scan_D19.0_p0.jsonl < /dev/null > $F/control/control.raw 2>&1
rc=$?; tc=$(( $(date +%s) - t0 ))
grep -vE 'Warning|^  [a-z]+ = |slogdet' $F/control/control.raw > $F/control/control.log
MAXRSS=$(awk '/Maximum resident set size/ {print $NF}' $F/control/control.raw); say "control exit $rc, wall $tc s, max RSS ${MAXRSS:-?} kB"
[ $rc = 0 ] || { say "STOP: the control did not end cleanly (exit $rc; 3 = not the record system, 124 = the cap): this machine's build or the state differs; no scan"; exit; }
$PY $F/control_check.py $F/control/control.log $F/control/scan_D19.0_p0.jsonl $IN/ref_dh370_scan_D19.000000_p0.jsonl 1.55 | tee $F/control/control_check.txt | tee -a $L
[ "${PIPESTATUS[0]}" = 0 ] || { say "STOP: the control does not match dh370's value: this machine's build differs; no scan"; exit; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
if [ -z "$MAXRSS" ] || [ "$av" -lt $(( NP * MAXRSS + 4000000 )) ]; then say "STOP: MemAvailable $av kB is below $NP x the control's max RSS (${MAXRSS:-?} kB) + 4 GB: no scan"; exit; fi
# 2. the scan, NP processes
say "2. scan: D 19.09375, lambda $LAMS ($NEV evaluations), $NP processes of 1 thread, nice 10, cap ${CAP_SCAN} s each by exact pid; the control took $tc s"
mapfile -t LA < <(echo $LAMS | tr ',' '\n')
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LA[@]}; i += NP)); do mine="$mine,${LA[$i]}"; done
  mine=${mine#,}
  say "process $p: lambda $mine"
  ( nice -n 10 /usr/bin/time -v timeout -s TERM $CAP_SCAN $PY -u $IN/d18_hybsign.py $IN/l1kc63dh370.jsonl $IN/sol_l1kc63dh370_D19.093750.npy 19.09375 $mine $F/scan/scan_D19.09375_p$p.jsonl < /dev/null > $F/scan/scan_p$p.raw 2>&1
    echo "$(date -u '+%F %T') UTC process $p exit $?" >> $L ) &
  pids+=($!)
done
( while kill -0 ${pids[0]} 2>/dev/null || kill -0 ${pids[1]} 2>/dev/null || kill -0 ${pids[2]} 2>/dev/null || kill -0 ${pids[3]} 2>/dev/null || kill -0 ${pids[4]} 2>/dev/null || kill -0 ${pids[5]} 2>/dev/null; do
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*19.09375' | wc -l) python, RSS_kB $(ps -eo rss,cmd | awk '/d18_hybsign.py.*19.09375/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $(awk '/MemAvailable/ {print $2}' /proc/meminfo), load $(cut -d' ' -f1 /proc/loadavg), points $(cat $F/scan/scan_D19.09375_p*.jsonl 2>/dev/null | wc -l)" >> $F/scan/sampler.log; sleep 60
  done ) &
wait "${pids[@]}"
for p in 0 1 2 3 4 5; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $F/scan/scan_p$p.raw > $F/scan/scan_p$p.log; head -1 $F/scan/scan_p$p.log | tee -a $L | cut -c1-200; done
cat $F/scan/scan_D19.09375_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$F/scan/scan_D19.09375_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# 3. the reading: read_lower.py (dh170's, blob 89309d3c) on the six files, the repeat check on the merged file
cd $IN
{ echo "=== read_lower.py $F/scan 1.480 1.540"; $PY -W ignore read_lower.py $F/scan 1.480 1.540; echo "read_lower exit $?"
  echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $F/scan/scan_D19.09375_1025.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
say "scan done; reading in read_lower.txt"
exit 0
}
