#!/bin/bash
# #1025 kc87_d205 (dh610), the coordinator's order of 23 Nov (hc, after kc87_d205, raw 10ddc4be): k_c 87 at D 20.5 on Linux from dh170's accepted k_c 79 D 20.5 state (raw I1025-dh170/kc79_d205 at 9535a78a: state blob 30a92b78, record 5406e21c):
#  1. the source: kc79_syscheck_1025.py accepts it (its --mutate=F and --mutate=steps exit 1) and kc87_syscheck_1025.py refuses it (exit 1);
#  2. ell_refine.py l1kc79dh170d205 79 l1kc87dh610d205 87 1 20.5 2.1088217835 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (8 threads, nice 10, cap 21600 s), in solver/matter of ~/Source/choptuik-large-d-1025g at 48c36355;
#  3. accepted only by kc87_syscheck_1025.py (exit 0; its --mutate=F and --mutate=steps exit 1) with kc79_syscheck_1025.py refusing the result (exit 1);
#  4. d18_hybsign.py (e089207a, unmodified) at lambda 1.050 to 1.120 by 0.005 plus a repeat of 1.085 (16 evaluations, 5 processes of 1 thread, nice 10; p0 1.085(repeat),1.050,1.075,1.100; p1 1.055,1.080,1.105; p2 1.085,1.060,1.110;
#     p3 1.065,1.090,1.115; p4 1.070,1.095,1.120: the repeat and its original run in the first round on two processes), in ~/Source/choptuik-large-d-1025f at 505d8399; a watcher compares the two 1.085 rows when both exist (repeat_check.py; it logs, it stops nothing);
#  5. read_lower.py (89309d3c) and repeat_check.py, then kc87d205_read.py (the changes beside dh170's k_c 79 D 20.5 ones: the coordinator's 1.087574, or dh170's final reading when `in/dh170_k79_read_lower.txt` exists).
# Each step stops the lane when it fails and nothing later runs. Free memory: refuses to start the regrid with less than 8 GiB available and the scan with less than 5 x 2.5 GB + 4 GB; nothing is stopped or terminated for memory (Nathan's rule of
# 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt. usage: bash lane_kc87_d205.sh [dry]
{
set -u
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc87_d205; IN=$F/in; S=$F/scan; RG=$F/regrid
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=20.5; LAM0=2.1088217835; SRC=l1kc79dh170d205; TAG=l1kc87dh610d205; L=$F/exits_kc87_d205.txt; MEMSTOP=4194304
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_d205: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
stop() { say "STOP: $*"; exit 1; }
mkdir -p $S $RG
bad=0
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { say "refuse: $WT is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { say "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] && [ "$(blob $WTM/ell_delta.py | cut -c1-8)" = fde699f5 ] || { say "refuse: ell_refine.py is not 631e5801 or ell_delta.py is not fde699f5"; bad=1; }
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || { say "refuse: $WT solver/ has changes"; bad=1; }
[ "$(git -C $WTF rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WTF status --short)" ] || { say "refuse: $WTF is not clean at 505d8399"; bad=1; }
for f in $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.5000.npy $S/scan_D20.5_p0.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ -e $WTM/data/sol_${SRC}_D20.5000.npy ] && [ "$(blob $WTM/data/sol_${SRC}_D20.5000.npy | cut -c1-8)" != 30a92b78 ] && { say "refuse: data/sol_${SRC}_D20.5000.npy exists and is not blob 30a92b78"; bad=1; }
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$($PY -c "print(float('$L0') == float('$LAM0'))")" = True ] || { say "refuse: lambda_0(20.5) reads $L0, not $LAM0"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 8388608 ] || { say "refuse: MemAvailable $av kB is below 8 GiB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs.txt, worktrees 1025g 48c36355 and 1025f 505d8399, ell_refine.py 631e5801, ell_delta.py fde699f5, lambda_0(20.5) $L0, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -V 2>&1))"
export D18_DIR=$IN
( cd $IN
  $PY -I kc79_syscheck_1025.py --selftest > $F/selftest_kc79_syscheck.log 2>&1; a0=$?
  $PY -I kc87_syscheck_1025.py --selftest > $F/selftest_kc87_syscheck.log 2>&1; a1=$?
  $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I kc87d205_read.py selftest > $F/selftest_kc87d205_read.log 2>&1; k0=$?
  $PY -I kc87d205_read.py selftest --mutate > $F/selftest_kc87d205_read_mutate.log 2>&1; k1=$?
  echo "$a0 $a1 $r0 $r1 $r2 $r3 $k0 $k1" > $F/selftest_exits.txt )
read -r a0 a1 r0 r1 r2 r3 k0 k1 < $F/selftest_exits.txt
[ "$a0 $a1 $r0 $r1 $r2 $r3 $k0 $k1" = "0 0 0 1 1 0 0 1" ] || stop "the selftests did not behave (kc79_syscheck $a0, kc87_syscheck $a1, read_lower $r0 $r1 $r2, repeat_check $r3, kc87d205_read $k0 $k1; wanted 0 0 0 1 1 0 0 1)"
say "selftests as wanted (kc79_syscheck, kc87_syscheck, read_lower, mutate shift, mutate round2, repeat_check, kc87d205_read, mutate: 0 0 0 1 1 0 0 1)"
[ "${1:-}" = dry ] && { say "dry run: nothing started"; exit 0; }
# 1. the source
SRCST=$IN/sol_${SRC}_D20.5000.npy
$PY -I $IN/kc79_syscheck_1025.py $IN/$SRC.jsonl $SRCST $D $WTM > $RG/source_kc79_syscheck.txt 2>&1; s=$?
for m in F steps; do $PY -I $IN/kc79_syscheck_1025.py $IN/$SRC.jsonl $SRCST $D $WTM --mutate=$m > $RG/source_kc79_syscheck_mutate_$m.txt 2>&1; eval "c$m=$?"; done
$PY -I $IN/kc87_syscheck_1025.py $IN/$SRC.jsonl $SRCST $D $WTM > $RG/source_kc87_syscheck_refuses.txt 2>&1; k=$?
say "source check: kc79_syscheck_1025.py exit $s ($(grep -E '^(ACCEPTED|NOT ACCEPTED)' $RG/source_kc79_syscheck.txt | cut -c1-110)); its controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each); kc87_syscheck_1025.py on it exit $k (1 wanted: $(grep -E '^(ACCEPTED|NOT ACCEPTED)' $RG/source_kc87_syscheck_refuses.txt | cut -c1-110))"
[ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] && [ $k = 1 ] || stop "the source is not accepted by the k_c 79 check, a control did not exit 1, or the k_c 87 check did not refuse it"
# 2. the regrid
if [ ! -e $WTM/data/sol_${SRC}_D20.5000.npy ]; then cp $SRCST $WTM/data/sol_${SRC}_D20.5000.npy; fi
[ "$(blob $WTM/data/sol_${SRC}_D20.5000.npy | cut -c1-8)" = 30a92b78 ] || stop "the source state in data/ is not blob 30a92b78"
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 79 $TAG 87 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(date -u '+%F %T') UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $RG/refine.log
say "regrid starts: $CMD"
( while sleep 60; do
    echo "$(date -u '+%F %T'),$(ps -C python -o rss=,pcpu=,nlwp=,args= | grep "ell_refine.py $SRC " | grep -v grep | head -1 | cut -c1-40)" >> $RG/samples.csv
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $RG/MEMALERT.txt
  done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $RG/refine.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
say "ell_refine exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] && [ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D20.5000.npy ] || stop "ell_refine exit $rc or no record or state written"
cp $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.5000.npy $RG/
{ echo "$(blob $RG/sol_${TAG}_D20.5000.npy) sol_${TAG}_D20.5000.npy"; echo "$(blob $RG/$TAG.jsonl) $TAG.jsonl"; } > $F/in_blobs_regrid.txt
# 3. the acceptance
$PY -I $IN/kc87_syscheck_1025.py $RG/$TAG.jsonl $RG/sol_${TAG}_D20.5000.npy $D $WTM > $RG/syscheck.txt 2>&1; s=$?
for m in F steps; do $PY -I $IN/kc87_syscheck_1025.py $RG/$TAG.jsonl $RG/sol_${TAG}_D20.5000.npy $D $WTM --mutate=$m > $RG/syscheck_mutate_$m.txt 2>&1; eval "c$m=$?"; done
$PY -I $IN/kc79_syscheck_1025.py $RG/$TAG.jsonl $RG/sol_${TAG}_D20.5000.npy $D $WTM > $RG/syscheck_kc79_refuses.txt 2>&1; k=$?
say "acceptance: kc87_syscheck_1025.py exit $s; controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each); kc79_syscheck_1025.py on the result exit $k (1 wanted): $(tail -n 3 $RG/syscheck.txt | cut -c1-330 | tr '\n' ' ')"
[ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] && [ $k = 1 ] || stop "the regrid is not accepted, a control did not exit 1, or the k_c 79 check did not refuse the result"
cp $RG/syscheck.txt $RG/ACCEPTED.txt; say "regrid ACCEPTED"
# 4. the scan
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( 5 * 2500000 + 4000000 )) ] || stop "the scan refused to start: MemAvailable $av kB is below 5 x 2.5 GB + 4 GB"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WF
LISTS=("1.085,1.050,1.075,1.100" "1.055,1.080,1.105" "1.085,1.060,1.110" "1.065,1.090,1.115" "1.070,1.095,1.120")
say "scan: lambda 1.050 to 1.120 by 0.005 and a repeat of 1.085 (16 evaluations), lists ${LISTS[*]}, 5 processes of 1 thread, nice 10, cap 28800 s each"
pids=()
for j in 0 1 2 3 4; do
  ( cd $WF && nice -n 10 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $RG/$TAG.jsonl $RG/sol_${TAG}_D20.5000.npy $D ${LISTS[$j]} $S/scan_D20.5_p$j.jsonl < /dev/null > $S/scan_p$j.raw 2>&1
    echo "$(date -u '+%F %T') UTC scan p$j (${LISTS[$j]}) exit $?" >> $L ) &
  pids+=($!)
done
( sleep 10; while pgrep -f "d18_hybsign.py.*$TAG" > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f "d18_hybsign.py.*$TAG" | wc -l), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/scan_D20.5_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_scan.txt
    sleep 30
  done ) &
( for i in $(seq 1 1500); do
    sleep 30
    n=$(cat $S/scan_D20.5_p*.jsonl 2>/dev/null | $PY -I -c "import sys, json; print(sum(1 for l in sys.stdin if l.strip() and abs(json.loads(l)['lam'] - 1.085) < 1e-9))")
    if [ "$n" = 2 ]; then
      cat $S/scan_D20.5_p*.jsonl > $S/pair_merged.jsonl
      $PY -I $IN/repeat_check.py $S/pair_merged.jsonl > $S/pair_check.txt 2>&1; pc=$?
      say "pair check of 1.085 (repeat_check.py, first round; logs only, stops nothing): exit $pc: $(tail -n 1 $S/pair_check.txt | cut -c1-200)"
      break
    fi
  done ) &
PW=$!
wait "${pids[@]}"
kill $PW 2>/dev/null
for j in 0 1 2 3 4; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_p$j.raw > $S/scan_p$j.log; say "p$j: $(grep -E 'record system' $S/scan_p$j.log | head -1 | cut -c1-150)"; done
cat $S/scan_D20.5_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D20.5_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# 5. the reading
cd $IN
{ echo "=== read_lower.py $S 1.050 1.120"; $PY -W ignore read_lower.py $S 1.050 1.120; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $S/scan_D20.5_all.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
if [ -e $IN/dh170_k79_read_lower.txt ]; then $PY -I kc87d205_read.py $F/read_lower.txt $IN/dh170_k79_read_lower.txt > $F/kc87d205_read.txt 2>&1; else $PY -I kc87d205_read.py $F/read_lower.txt > $F/kc87d205_read.txt 2>&1; fi
say "scan done; readings in read_lower.txt and kc87d205_read.txt; kc87 done"
exit 0
}
