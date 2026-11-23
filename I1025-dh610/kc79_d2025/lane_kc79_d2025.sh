#!/bin/bash
# #1025 kc79_d2025 (dh610), the coordinator's order of 23 Nov (hc, after repro_d1975): k_c 79 at D 20.25 on Linux from leg 3's k_c 71 D 20.25 state of win2 (raw 589d5f2a: sol_l1kc71Lw1025c_D20.250000.npy blob 8e137d6b, l1kc71Lw1025c.jsonl cc1e872c), as win2 did:
#  1. the source: kc71_syscheck.py accepts it (its --mutate=F and --mutate=steps exit 1);
#  2. ell_refine.py l1kc71Lw1025c 71 l1kc79dh610d2025 79 1 20.25 2.1099063840 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (8 threads, nice 10, cap 21600 s), in solver/matter of ~/Source/choptuik-large-d-1025g at 48c36355;
#  3. accepted only by kc79_syscheck_1025.py (exit 0; its --mutate=F and --mutate=steps exit 1);
#  4. d18_hybsign.py (e089207a, unmodified) at lambda 1.13 to 1.24 by 0.01 plus a repeat of 1.16 (13 evaluations, 4 processes of 1 thread, nice 10; value i to process i mod 4: p0 1.13,1.17,1.21,1.16(repeat); p1 1.14,1.18,1.22; p2 1.15,1.19,1.23; p3 1.16,1.20,1.24), in ~/Source/choptuik-large-d-1025f at 505d8399;
#  5. read_lower.py (89309d3c) and repeat_check.py, then kc79_read.py (win2's two robust changes beside mine).
# Each step stops the lane when it fails and nothing later runs. Free memory: refuses to start the regrid with less than 8 GiB available and the scan with less than 4 x 2.5 GB + 4 GB; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08):
# below 4 GiB the sampler only writes MEMALERT.txt. usage: bash lane_kc79_d2025.sh [dry]
{
set -u
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc79_d2025; IN=$F/in; S=$F/scan; RG=$F/regrid
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=20.25; LAM0=2.1099063840; SRC=l1kc71Lw1025c; TAG=l1kc79dh610d2025; L=$F/exits_kc79_d2025.txt; MEMSTOP=4194304
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_d2025: $*" | tee -a $L; }
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
for f in $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.2500.npy $S/scan_D20.25_p0.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$($PY -c "print(float('$L0') == float('$LAM0'))")" = True ] || { say "refuse: lambda_0(20.25) reads $L0, not $LAM0"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 8388608 ] || { say "refuse: MemAvailable $av kB is below 8 GiB"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked (in_blobs.txt, worktrees 1025g 48c36355 and 1025f 505d8399, ell_refine.py 631e5801, ell_delta.py fde699f5, lambda_0(20.25) $L0, MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -V 2>&1))"
# the controls of the tools
export D18_DIR=$IN
( cd $IN
  $PY -I kc79_syscheck_1025.py --selftest > $F/selftest_kc79_syscheck.log 2>&1; a0=$?
  $PY -I kc71_syscheck.py --selftest > $F/selftest_kc71_syscheck.log 2>&1; a1=$?
  $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I kc79_read.py selftest > $F/selftest_kc79_read.log 2>&1; k0=$?
  $PY -I kc79_read.py selftest --mutate > $F/selftest_kc79_read_mutate.log 2>&1; k1=$?
  echo "$a0 $a1 $r0 $r1 $r2 $r3 $k0 $k1" > $F/selftest_exits.txt )
read -r a0 a1 r0 r1 r2 r3 k0 k1 < $F/selftest_exits.txt
[ "$a0 $a1 $r0 $r1 $r2 $r3 $k0 $k1" = "0 0 0 1 1 0 0 1" ] || stop "the selftests did not behave (kc79_syscheck $a0, kc71_syscheck $a1, read_lower $r0 $r1 $r2, repeat_check $r3, kc79_read $k0 $k1; wanted 0 0 0 1 1 0 0 1)"
say "selftests as wanted (kc79_syscheck, kc71_syscheck, read_lower, mutate shift, mutate round2, repeat_check, kc79_read, mutate: 0 0 0 1 1 0 0 1)"
[ "${1:-}" = dry ] && { say "dry run: nothing started"; exit 0; }
# 1. the source
SRCST=$IN/sol_${SRC}_D20.250000.npy
$PY -I $IN/kc71_syscheck.py $IN/$SRC.jsonl $SRCST $D $WTM > $RG/source_kc71_syscheck.txt 2>&1; s=$?
for m in F steps; do $PY -I $IN/kc71_syscheck.py $IN/$SRC.jsonl $SRCST $D $WTM --mutate=$m > $RG/source_kc71_syscheck_mutate_$m.txt 2>&1; eval "c$m=$?"; done
say "source check: kc71_syscheck.py exit $s ($(grep -E '^(ACCEPTED|NOT ACCEPTED)' $RG/source_kc71_syscheck.txt | cut -c1-120)); controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each)"
[ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] || stop "the source is not accepted or a control did not exit 1"
# 2. the regrid
cp $SRCST $WTM/data/sol_${SRC}_D20.2500.npy
[ "$(blob $WTM/data/sol_${SRC}_D20.2500.npy | cut -c1-8)" = 8e137d6b ] || stop "the copied source state is not blob 8e137d6b"
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
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
[ $rc = 0 ] && [ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D20.2500.npy ] || stop "ell_refine exit $rc or no record or state written"
cp $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.2500.npy $RG/
{ echo "$(blob $RG/sol_${TAG}_D20.2500.npy) sol_${TAG}_D20.2500.npy"; echo "$(blob $RG/$TAG.jsonl) $TAG.jsonl"; } > $F/in_blobs_regrid.txt
# 3. the acceptance
$PY -I $IN/kc79_syscheck_1025.py $RG/$TAG.jsonl $RG/sol_${TAG}_D20.2500.npy $D $WTM > $RG/syscheck.txt 2>&1; s=$?
for m in F steps; do $PY -I $IN/kc79_syscheck_1025.py $RG/$TAG.jsonl $RG/sol_${TAG}_D20.2500.npy $D $WTM --mutate=$m > $RG/syscheck_mutate_$m.txt 2>&1; eval "c$m=$?"; done
say "acceptance: kc79_syscheck_1025.py exit $s; controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each): $(tail -n 3 $RG/syscheck.txt | cut -c1-330 | tr '\n' ' ')"
[ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] || stop "the regrid is not accepted or a control did not exit 1"
cp $RG/syscheck.txt $RG/ACCEPTED.txt; say "regrid ACCEPTED"
# 4. the scan
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( 4 * 2500000 + 4000000 )) ] || stop "the scan refused to start: MemAvailable $av kB is below 4 x 2.5 GB + 4 GB"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WF
LISTS=("1.13,1.17,1.21,1.16" "1.14,1.18,1.22" "1.15,1.19,1.23" "1.16,1.20,1.24")
say "scan: lambda 1.13 to 1.24 and a repeat of 1.16 (13 evaluations), lists ${LISTS[*]}, 4 processes of 1 thread, nice 10, cap 28800 s each"
pids=()
for j in 0 1 2 3; do
  ( cd $WF && nice -n 10 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $RG/$TAG.jsonl $RG/sol_${TAG}_D20.2500.npy $D ${LISTS[$j]} $S/scan_D20.25_p$j.jsonl < /dev/null > $S/scan_p$j.raw 2>&1
    echo "$(date -u '+%F %T') UTC scan p$j (${LISTS[$j]}) exit $?" >> $L ) &
  pids+=($!)
done
( sleep 10; while pgrep -f "d18_hybsign.py.*$TAG" > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f "d18_hybsign.py.*$TAG" | wc -l), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/scan_D20.25_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_scan.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for j in 0 1 2 3; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_p$j.raw > $S/scan_p$j.log; say "p$j: $(grep -E 'record system' $S/scan_p$j.log | head -1 | cut -c1-150)"; done
cat $S/scan_D20.25_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D20.25_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# 5. the reading
cd $IN
{ echo "=== read_lower.py $S 1.13 1.24"; $PY -W ignore read_lower.py $S 1.13 1.24; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $S/scan_D20.25_all.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
$PY -I kc79_read.py $F/read_lower.txt > $F/kc79_read.txt 2>&1
say "scan done; readings in read_lower.txt and kc79_read.txt; kc79 done"
exit 0
}
