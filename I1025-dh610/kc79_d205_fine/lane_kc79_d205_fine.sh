#!/bin/bash
# #1025 kc79_d205_fine (dh610), the coordinator's order of 23 Nov (hc, after kc87_d205, raw 2514221e): dh170's k_c 79 D 20.5 state (raw I1025-dh170/kc79_d205 at 9535a78a: state blob 30a92b78, record 5406e21c) on this build:
#  1. kc79_syscheck_1025.py accepts it (exit 0; its --mutate=F and --mutate=steps exit 1);
#  2. d18_hybsign.py (e089207a, unmodified) at lambda 1.060 to 1.090 by 0.005 (7 evaluations, 5 processes of 1 thread, nice 10: p0 1.060,1.085; p1 1.090,1.065; p2 1.070; p3 1.075; p4 1.080; 1.060 and 1.090 are dh170's two
#     rows of the same state, repeated on another build), in ~/Source/choptuik-large-d-1025f at 505d8399;
#  3. read_lower.py (89309d3c) on the scan, rows_check.py (this machine's rows at 1.060 and 1.090 against dh170's: same sign, ln|det| within 1e-9 relative), fine_read.py (the change beside the k_c 87 root 1.077872 and dh170's 1.087574).
# Each step stops the lane when it fails and nothing later runs, except that the reading is written before a rows_check failure is reported (a control that fires stops the work, and I report it). Free memory: refuses to start the scan
# with less than 5 x 2.5 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt. usage: bash lane_kc79_d205_fine.sh [dry]
{
set -u
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc79_d205_fine; IN=$F/in; S=$F/scan; RG=$F/src
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=20.5; TAG=l1kc79dh170d205; L=$F/exits_kc79_d205_fine.txt; MEMSTOP=4194304
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_d205_fine: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
stop() { say "STOP: $*"; exit 1; }
mkdir -p $S $RG
bad=0
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { say "refuse: $WT is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { say "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ "$(git -C $WTF rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WTF status --short)" ] || { say "refuse: $WTF is not clean at 505d8399"; bad=1; }
[ -e $S/scan_D20.5_p0.jsonl ] && { say "refuse: $S/scan_D20.5_p0.jsonl exists"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( 5 * 2500000 + 4000000 )) ] || { say "refuse: MemAvailable $av kB is below 5 x 2.5 GB + 4 GB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs.txt, worktrees 1025g 48c36355 and 1025f 505d8399, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -V 2>&1))"
export D18_DIR=$IN
( cd $IN
  $PY -I kc79_syscheck_1025.py --selftest > $F/selftest_kc79_syscheck.log 2>&1; a0=$?
  $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY -I fine_read.py selftest > $F/selftest_fine_read.log 2>&1; f0=$?
  $PY -I fine_read.py selftest --mutate > $F/selftest_fine_read_mutate.log 2>&1; f1=$?
  $PY -I rows_check.py selftest > $F/selftest_rows_check.log 2>&1; w0=$?
  $PY -I rows_check.py selftest --mutate > $F/selftest_rows_check_mutate.log 2>&1; w1=$?
  echo "$a0 $r0 $r1 $r2 $f0 $f1 $w0 $w1" > $F/selftest_exits.txt )
read -r a0 r0 r1 r2 f0 f1 w0 w1 < $F/selftest_exits.txt
[ "$a0 $r0 $r1 $r2 $f0 $f1 $w0 $w1" = "0 0 1 1 0 1 0 1" ] || stop "the selftests did not behave (kc79_syscheck $a0, read_lower $r0 $r1 $r2, fine_read $f0 $f1, rows_check $w0 $w1; wanted 0 0 1 1 0 1 0 1)"
say "selftests as wanted (kc79_syscheck, read_lower, mutate shift, mutate round2, fine_read, mutate, rows_check, mutate: 0 0 1 1 0 1 0 1)"
[ "${1:-}" = dry ] && { say "dry run: nothing started"; exit 0; }
# 1. the source
STATE=$IN/sol_${TAG}_D20.5000.npy
$PY -I $IN/kc79_syscheck_1025.py $IN/$TAG.jsonl $STATE $D $WTM > $RG/syscheck.txt 2>&1; s=$?
for m in F steps; do $PY -I $IN/kc79_syscheck_1025.py $IN/$TAG.jsonl $STATE $D $WTM --mutate=$m > $RG/syscheck_mutate_$m.txt 2>&1; eval "c$m=$?"; done
say "source check: kc79_syscheck_1025.py exit $s; controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each): $(tail -n 3 $RG/syscheck.txt | cut -c1-330 | tr '\n' ' ')"
[ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] || stop "the state is not accepted by the k_c 79 check on this build, or a control did not exit 1"
# 2. the scan
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WF
LISTS=("1.060,1.085" "1.090,1.065" "1.070" "1.075" "1.080")
say "scan: lambda 1.060 to 1.090 by 0.005 (7 evaluations), lists ${LISTS[*]}, 5 processes of 1 thread, nice 10, cap 28800 s each"
pids=()
for j in 0 1 2 3 4; do
  ( cd $WF && nice -n 10 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $IN/$TAG.jsonl $STATE $D ${LISTS[$j]} $S/scan_D20.5_p$j.jsonl < /dev/null > $S/scan_p$j.raw 2>&1
    echo "$(date -u '+%F %T') UTC scan p$j (${LISTS[$j]}) exit $?" >> $L ) &
  pids+=($!)
done
( sleep 10; while pgrep -f "d18_hybsign.py.*$TAG" > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f "d18_hybsign.py.*$TAG" | wc -l), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/scan_D20.5_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_scan.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for j in 0 1 2 3 4; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_p$j.raw > $S/scan_p$j.log; say "p$j: $(grep -E 'record system' $S/scan_p$j.log | head -1 | cut -c1-150)"; done
cat $S/scan_D20.5_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D20.5_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# 3. the reading
cd $IN
{ echo "=== read_lower.py $S 1.060 1.090"; $PY -W ignore read_lower.py $S 1.060 1.090; echo "read_lower exit $?"; } > $F/read_lower.txt 2>&1
$PY -I fine_read.py $F/read_lower.txt > $F/fine_read.txt 2>&1
$PY -I rows_check.py $S/scan_D20.5_all.jsonl $IN/ref_dh170_k79_scan_D20.5.jsonl 1.06 1.09 > $F/rows_check.txt 2>&1; rc=$?
say "rows_check.py (1.060 and 1.090 against dh170's rows) exit $rc: $(cut -c1-60 $F/rows_check.txt | tr '\n' ' ')"
[ $rc = 0 ] || stop "rows_check fired: this build's rows at 1.060 or 1.090 differ from dh170's (sign or ln|det| beyond 1e-9 relative); the reading is in read_lower.txt and fine_read.txt"
say "scan done; readings in read_lower.txt, fine_read.txt, rows_check.txt; kc79_fine done"
exit 0
}
