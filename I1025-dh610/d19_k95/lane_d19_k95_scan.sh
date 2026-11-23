#!/bin/bash
# #1025 d19_k95 scan (dh610), the coordinator's order of 23 Nov (hc ~20:08 UTC): d18_hybsign.py at D 19.0, k_c 95, on this folder's accepted regrid (state and record at the folder root, blobs in in_blobs_regrid.txt): lambda 1.395 to 1.435 at
# 0.005 (9 values), a repeat of 1.415 on another process, and lambda_1 bracketed by 1.535 and 1.545 (2 values): 12 evaluations over 6 processes of 1 thread, nice 10, two rounds (round 1: the six points around the expected
# lower root 1.415, 1.410, 1.420, 1.405, 1.425 and the repeat 1.415; round 2: 1.395, 1.400, 1.430, 1.435, 1.535, 1.545). Reading: read_lower.py (dh170's, blob 89309d3c) on each window separately (1.395 to 1.435; 1.535 to 1.545),
# repeat_check.py on the merged file. d18_hybsign.py is xfkappa's, blob e089207a, unmodified. Memory: refuses to start with less than 6 x 4 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of
# 2026-11-08): below 4 GiB the sampler only writes MEMALERT_scan.txt. usage: bash lane_d19_k95_scan.sh [dry]
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/d19_k95; IN=$F/in; S=$F/scan; RG=$F/scan_src
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=19.0; TAG=l1kc95dh610d19; STATE=$F/sol_${TAG}_D19.0000.npy; REC=$F/$TAG.jsonl
NP=6; CAP_SCAN=28800; RSS_GUESS=4000000; MEMSTOP=4194304
L=$F/exits_d19k95_scan.txt
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC d19_k95 scan: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
stop() { say "STOP: $*"; exit 1; }
mkdir -p $S $RG
bad=0
# pins: the scan tools, the accepted regrid's state and record (blobs written at its acceptance), the checks
while read bb f; do [ -f $IN/$f ] && [ "$(hb $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_scan.txt
while read bb f; do [ -f $F/$f ] && [ "$(hb $F/$f)" = "$bb" ] || { say "refuse: $F/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs_regrid.txt
[ "$(wc -l < $F/in_blobs_regrid.txt)" = 2 ] || { say "refuse: in_blobs_regrid.txt does not list the state and the record"; bad=1; }
head -1 $F/regrid/VERDICT.txt | grep -q '^ACCEPTED' || { say "refuse: regrid/VERDICT.txt is not ACCEPTED"; bad=1; }
for pb in "$IN/kc87_syscheck_1025.py 6df5d9600edebeae8cc4e602025e42e79925b7d6" "$IN/kc95_syscheck_1025.py d487e628f61d1accae8e09f7d1ad438c1d787883"; do
  set -- $pb; [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { say "refuse: $WT is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { say "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ "$(git -C $WTF rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WTF status --short)" ] || { say "refuse: $WTF is not clean at 505d8399"; bad=1; }
for f in $S/scan_D19.0_p0.jsonl; do [ -e $f ] && [ "$MODE" != dry ] && { say "refuse: $f exists"; bad=1; }; done
# the lists, checked against the order: 9 grid values, the repeat of 1.415 on another process than the first 1.415, the two lambda_1 points
LISTS=("1.415,1.395" "1.410,1.400" "1.420,1.430" "1.405,1.435" "1.425,1.535" "1.415,1.545")
$PY -I -c "
import sys
L = [x.split(',') for x in sys.argv[1:]]
flat = sorted(v for l in L for v in l)
want = sorted([f'{1.395 + 0.005 * i:.3f}' for i in range(9)] + ['1.415', '1.535', '1.545'])
rep = [i for i, l in enumerate(L) if '1.415' in l]
sys.exit(0 if len(L) == 6 and all(len(l) == 2 for l in L) and flat == want and len(rep) == 2 else 1)" "${LISTS[@]}" || { say "refuse: the lists are not the order's 12 evaluations"; bad=1; }
export D18_DIR=$IN
( cd $IN && $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I kc95_syscheck_1025.py --selftest > $F/selftest_kc95_syscheck_scan.log 2>&1; r4=$?
  echo "$r4 $r0 $r1 $r2 $r3" > $F/selftest_exits_scan.txt )
read -r r4 r0 r1 r2 r3 < $F/selftest_exits_scan.txt
[ "$r4 $r0 $r1 $r2 $r3" = "0 0 1 1 0" ] || { say "refuse: the selftests did not behave (kc95_syscheck $r4, read_lower $r0 $r1 $r2, repeat_check $r3; wanted 0 0 1 1 0)"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( NP * RSS_GUESS + 4000000 )) ] || { say "refuse: MemAvailable $av kB is below $NP x $RSS_GUESS kB (above the 3.1 to 3.3 GB of k_c 95 at D 19.5 and 19.75) + 4 GB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs_scan.txt, in_blobs_regrid.txt, checks, d18_hybsign e089207a, worktrees 1025g 48c36355 and 1025f 505d8399 clean, $($PY -V 2>&1)), selftests as wanted (kc95_syscheck, read_lower, mutate shift, mutate round2, repeat_check: $r4 $r0 $r1 $r2 $r3); MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg); lists ${LISTS[*]}"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
# the source: the k_c 95 check accepts the pinned copies on this build, both controls exit 1, the k_c 87 check refuses
C95="nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $REC $STATE $D $WTM"
$C95 > $RG/syscheck.txt 2>&1; a0=$?
$C95 --mutate=F > $RG/syscheck_mutF.txt 2>&1; a1=$?
$C95 --mutate=steps > $RG/syscheck_mutsteps.txt 2>&1; a2=$?
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $REC $STATE $D $WTM > $RG/syscheck_kc87check_refuses.txt 2>&1; a3=$?
say "source check on the pinned copies: kc95_syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); kc87_syscheck exit $a3 (1 wanted)"
[ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ] || stop "the k_c 95 check, a control or the refusing k_c 87 check did not behave"
export P4_WT_MATTER=$WF
say "scan: D 19.0, k_c 95, 12 evaluations, lists ${LISTS[*]}, $NP processes of 1 thread, nice 10, cap ${CAP_SCAN} s each by timeout"
pids=()
for ((j = 0; j < NP; j++)); do
  ( cd $WF && nice -n 10 /usr/bin/time -v timeout -s TERM $CAP_SCAN $PY -u $IN/d18_hybsign.py $REC $STATE $D ${LISTS[$j]} $S/scan_D19.0_p$j.jsonl < /dev/null > $S/scan_p$j.raw 2>&1
    echo "$(date -u '+%F %T') UTC scan p$j (${LISTS[$j]}) exit $?" >> $L ) &
  pids+=($!)
done
( sleep 10; while kill -0 ${pids[0]} 2>/dev/null || kill -0 ${pids[1]} 2>/dev/null || kill -0 ${pids[2]} 2>/dev/null || kill -0 ${pids[3]} 2>/dev/null || kill -0 ${pids[4]} 2>/dev/null || kill -0 ${pids[5]} 2>/dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC RSS_kB $(ps -eo rss,cmd | awk '/d18_hybsign.py.*l1kc95dh610d19/ && !/awk|time|timeout/ {s+=$1} END {print s+0}'), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/scan_D19.0_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_scan.txt
    sleep 30
  done ) &
wait "${pids[@]}"
nr=0
for ((j = 0; j < NP; j++)); do
  grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_p$j.raw > $S/scan_p$j.log
  say "p$j: $(grep -E 'record system' $S/scan_p$j.log | head -1 | cut -c1-150)"
  grep -q 'the record system' $S/scan_p$j.log && ! grep -q 'NOT the record system' $S/scan_p$j.log && nr=$((nr + 1))
done
[ $nr = $NP ] || stop "only $nr of $NP processes print the record system"
cat $S/scan_D19.0_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D19.0_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# the reading: read_lower.py on each window separately (a single call would bracket a change across the 0.1 gap), the repeat check on the merged file
cd $IN
{ echo "=== read_lower.py $S 1.395 1.435"; $PY -W ignore read_lower.py $S 1.395 1.435; echo "read_lower exit $?"
  echo "=== read_lower.py $S 1.535 1.545"; $PY -W ignore read_lower.py $S 1.535 1.545; echo "read_lower exit $?"
  echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $S/scan_D19.0_1025.jsonl; echo "repeat_check exit $?"; } > $F/read_lower_scan.txt 2>&1
say "reading: $(grep -E 'robust change|hybrid signs|^robust changes|repeat check' $F/read_lower_scan.txt | cut -c1-160 | tr '\n' '|')"
say "scan done; reading in read_lower_scan.txt"
exit 0
}
