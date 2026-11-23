#!/bin/bash
# #1025 cross_macm3_d1975 (dh610), the coordinator's cross-check of 23 Nov (the #1025 comment of 05:45 UTC): macm3's accepted k_c 87 D 19.75 state and record (raw I1025-macm3/kc87_d1975/, 03c79c79: state
# 5825f5d0, record 84f75a48) on this Linux machine. Step 1: kc87_syscheck_1025.py (6df5d960) accepts them (|F| and steps as recorded; selftest 0, --mutate=F and --mutate=steps exit 1). Step 2: d18_hybsign.py
# (e089207a, unmodified) on that state at lambda 1.32, 1.33, 1.34, 3 processes of 1 thread, nice 10, each printing the record system. The comparison is compare_cross.py (its selftest 0, --mutate 1). Beside the
# k_c 95 D 19.75 scan (../kc95_d1975, unit i1025w). Free memory: refuses to start with less than 3 x 4 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the
# sampler only writes run/MEMALERT.txt, which the runner session posts to the coordinator. usage: bash lane_cross.sh [dry]
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/cross_macm3_d1975; IN=$F/in; OUT=$F/run
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; WTM=/home/nathan/Source/choptuik-large-d-1025g/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
NP=3; CAP=28800; RSS_GUESS=4000000; MEMSTOP=4194304; D=19.75
L=$F/exits_cross.txt
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC cross_macm3_d1975: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
mkdir -p $OUT
bad=0
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$IN/kc87_syscheck_1025.py 6df5d9600edebeae8cc4e602025e42e79925b7d6" \
          "$IN/sol_l1kc87macm3d1975_D19.7500.npy 5825f5d00f50a068c244d08e5b66847c207ebd99" "$IN/l1kc87macm3d1975.jsonl 84f75a48beb7e245145ce8f0cf81cd0b425fdb00" \
          "$IN/ref_macm3_scan_D19.75_1025.jsonl 702717f3c351a33e3181cf3e77cd5b041736db95" "$F/compare_cross.py 93d5e98d5a61f39de73dbe2a5df1fdc1986a2ad3"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
[ "$(git -C ${WTM%/solver/matter} rev-parse --short=8 HEAD)" = 48c36355 ] || { say "refuse: worktree for the check is not at 48c36355"; bad=1; }
[ -e $OUT/xscan_D19.75_p0.jsonl ] && { say "refuse: $OUT/xscan_D19.75_p0.jsonl exists"; bad=1; }
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py --selftest > $OUT/selftest_kc87_syscheck.txt 2>&1; r1=$?
python3 $F/compare_cross.py selftest > $OUT/selftest_compare.txt 2>&1; r2=$?
python3 $F/compare_cross.py selftest --mutate > $OUT/selftest_compare_mutate.txt 2>&1; r3=$?
[ $r1 = 0 ] && [ $r2 = 0 ] && [ $r3 = 1 ] || { say "refuse: selftests (kc87_syscheck $r1, compare $r2, compare --mutate $r3; wanted 0 0 1)"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
if [ "$av" -lt $(( NP * RSS_GUESS + 4000000 )) ]; then say "refuse: MemAvailable $av kB is below $NP x $RSS_GUESS kB + 4 GB"; bad=1; fi
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs.txt, compare_cross.py, d18_hybsign e089207a, scan worktree 505d8399 clean, check worktree 48c36355, $PY), selftests as wanted (kc87_syscheck $r1, compare $r2, compare --mutate $r3); MemAvailable $av kB"
# step 1: the source check on macm3's state and record, on this machine
C="nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $IN/l1kc87macm3d1975.jsonl $IN/sol_l1kc87macm3d1975_D19.7500.npy $D $WTM"
$C > $OUT/syscheck.txt 2>&1; s0=$?
$C --mutate=F > $OUT/syscheck_mutF.txt 2>&1; s1=$?
$C --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; s2=$?
say "check (kc87_syscheck_1025.py on macm3's k_c 87 D 19.75 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each)"
if ! { [ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ]; }; then echo "REFUSED: check $s0, controls $s1 $s2" > $OUT/VERDICT.txt; say "STOP: the check or a control did not read as written; nothing started"; exit 1; fi
echo "ACCEPTED $(date -u '+%F %T') UTC" > $OUT/VERDICT.txt
[ "$MODE" = dry ] && { say "dry run: the three evaluations are not started"; exit 0; }
cd $W
LAMS=(1.32 1.33 1.34)
say "evaluations: D $D, k_c 87 (macm3's state), lambda ${LAMS[*]}, $NP processes of 1 thread, nice 10, cap ${CAP} s each by exact pid"
pids=()
for ((p = 0; p < NP; p++)); do
  say "process $p: lambda ${LAMS[$p]}"
  ( nice -n 10 /usr/bin/time -v timeout -s TERM $CAP $PY -u $IN/d18_hybsign.py $IN/l1kc87macm3d1975.jsonl $IN/sol_l1kc87macm3d1975_D19.7500.npy $D ${LAMS[$p]} $OUT/xscan_D19.75_p$p.jsonl < /dev/null > $OUT/p$p.raw 2>&1
    echo "$(date -u '+%F %T') UTC process $p exit $?" >> $L ) &
  pids+=($!)
done
( while kill -0 ${pids[0]} 2>/dev/null || kill -0 ${pids[1]} 2>/dev/null || kill -0 ${pids[2]} 2>/dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*cross_macm3_d1975' | wc -l) python, RSS_kB $(ps -eo rss,cmd | awk '/d18_hybsign.py.*cross_macm3_d1975/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $OUT/xscan_D19.75_p*.jsonl 2>/dev/null | wc -l)" >> $OUT/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $OUT/MEMALERT.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for p in 0 1 2; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $OUT/p$p.raw > $OUT/p$p.log; head -1 $OUT/p$p.log | tee -a $L | cut -c1-200; done
cat $OUT/xscan_D19.75_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$OUT/xscan_D19.75_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
python3 $F/compare_cross.py $OUT/xscan_D19.75_1025.jsonl $IN/ref_macm3_scan_D19.75_1025.jsonl $( [ -f $IN/ref_dh170_scan_D19.75_1025.jsonl ] && echo $IN/ref_dh170_scan_D19.75_1025.jsonl ) > $F/compare.txt 2>&1
say "evaluations done; comparison in compare.txt (exit $?)"
exit 0
}
