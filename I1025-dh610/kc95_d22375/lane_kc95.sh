#!/bin/bash
# #1025 kc95_d22375 (dh610), the coordinator's order of 25 Nov (hc, read at about 06:14 UTC): macm3's k_c 87 leg state at D 22.375 (raw I1025-macm3/kc87_leg2/b2/, tag l1kc87Lmacm3b2, commit 79ae81f4) regridded to k_c 95 with
# ell_refine.py as ../kc95_d1975/lane_kc95_regrid.sh did (worktree 48c36355, `--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 8 threads, nice 10, cap 21600 s, lambda_0(22.375) = 2.1014424345 from
# ell_delta.lam0_at), accepted only by kc95_syscheck_1025.py (selftest, both controls exit 1, the k_c 87 check refusing the result); then a WIDE d18_hybsign.py scan at lambda -0.10 to 0.50 by 0.04 plus a repeat of 0.14
# (17 evaluations on 4 processes of 1 thread, nice 10: p0 -0.10 0.06 0.22 0.38 and the repeat of 0.14, p1 -0.06 0.10 0.26 0.42, p2 -0.02 0.14 0.30 0.46, p3 0.02 0.18 0.34 0.50), read_lower.py on -0.10 to 0.50 and wide_read.py (every robust change by position and printed orientation; no prediction line).
# differs, a selftest or control that does not read as written, the source not accepted, the regrid not accepted or with an exception or over the 6 h cap, any scan process that fails; no robust change in the window is
# reported as read, with no widening. Free memory: the lane refuses to start the regrid with less than 8 GiB available and waits (6 h cap) for 7 x 3.6 GB + 4 GB before the scan; nothing is stopped or terminated for
# memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT*.txt. usage: bash lane_kc95.sh [dry|check]   (dry stops after the selftests, check after the source check)
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc95_d22375; IN=$F/in; OUT=$F/regrid; S=$F/scan
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
SRC=l1kc87Lmacm3b2; TAG=l1kc95dh610d22375; D=22.375; LAM0=2.1014424345; PRED=none; MEMSTOP=4194304; MEMSTART=8388608; RSS_GUESS=3600000; NP=4
L=$F/exits_kc95.txt; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
mkdir -p $OUT $S
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc95_d22375: $*" | tee -a $L; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; say "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
av0=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
say "start (mode ${MODE:-full}; load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $av0 kB)"
[ "$MODE" != dry ] && [ "$av0" -lt $MEMSTART ] && stop "MemAvailable $av0 kB is below 8 GiB"
# 1. pins
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || stop "$IN/$f missing or not blob $bb"; done < $F/in_blobs.txt
[ -s $F/in_blobs_src.txt ] || stop "in_blobs_src.txt is missing or empty (run fetch_src.sh first)"
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || stop "$IN/$f missing or not blob $bb"; done < $F/in_blobs_src.txt
diff -u $IN/kc87_syscheck_1025.py $IN/kc95_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
tail -n +3 $F/kc95_syscheck_1025.diff | cmp -s - $OUT/diff_rebuilt.txt || stop "kc95_syscheck_1025.diff is not the diff of the two checks"
[ "$(grep -c '^[-+][^-+]' $OUT/diff_rebuilt.txt)" = 6 ] || stop "the diff of the two checks is not three changed lines"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WTF rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WTF status --short)" ] || stop "$WTF is not clean at 505d8399"
[ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"
[ -e $S/scan_D${D}_p0.jsonl ] && [ -z "$MODE" ] && stop "$S/scan_D${D}_p0.jsonl exists"
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$L0" = "$LAM0" ] || stop "lambda_0($D) reads $L0, not $LAM0"
say "pins checked (in_blobs.txt, in_blobs_src.txt), diff of the two checks rebuilt (3 changed lines), worktrees 1025g 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801) and 1025f 505d8399 clean; lambda_0($D) $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# 2. selftests
export D18_DIR=$IN
( cd $IN
  nice -n 10 $PY -I kc87_syscheck_1025.py --selftest > $F/selftest_kc87_syscheck.log 2>&1; a0=$?
  nice -n 10 $PY -I kc95_syscheck_1025.py --selftest > $F/selftest_kc95_syscheck.log 2>&1; a1=$?
  $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I leg_read.py selftest > $F/selftest_leg_read.log 2>&1; g0=$?
  $PY -I leg_read.py selftest --mutate > $F/selftest_leg_read_mutate.log 2>&1; g1=$?
  $PY -I $F/wide_read.py selftest > $F/selftest_wide_read.log 2>&1; w0=$?
  $PY -I $F/wide_read.py selftest --mutate > $F/selftest_wide_read_mutate.log 2>&1; w1=$?
  ( cd $F && $PY -I planted_wide.py in > $F/selftest_planted_wide.log 2>&1 ); p0=$?
  ( cd $F && $PY -I planted_wide.py --mutate in > $F/selftest_planted_wide_mutate.log 2>&1 ); p1=$?
  echo "$a0 $a1 $r0 $r1 $r2 $r3 $g0 $g1 $w0 $w1 $p0 $p1" > $F/selftest_exits.txt )
read -r a0 a1 r0 r1 r2 r3 g0 g1 w0 w1 p0 p1 < $F/selftest_exits.txt
[ "$a0 $a1 $r0 $r1 $r2 $r3 $g0 $g1 $w0 $w1 $p0 $p1" = "0 0 0 1 1 0 0 1 0 1 0 1" ] || stop "the selftests did not behave (kc87_syscheck $a0, kc95_syscheck $a1, read_lower $r0 $r1 $r2, repeat_check $r3, leg_read $g0 $g1, wide_read $w0 $w1, planted_wide $p0 $p1; wanted 0 0 0 1 1 0 0 1 0 1 0 1)"
say "selftests as wanted (kc87_syscheck, kc95_syscheck, read_lower, mutate shift, mutate round2, repeat_check, leg_read, mutate, wide_read, mutate, planted_wide, mutate: 0 0 0 1 1 0 0 1 0 1 0 1)"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
# 3. the source: kc87_syscheck accepts it with both controls exit 1, and kc95_syscheck refuses it
STATE=$IN/sol_${SRC}_D22.375000.npy; REC=$IN/$SRC.jsonl
C87="nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $REC $STATE $D $WTM"
$C87 > $OUT/source_syscheck.txt 2>&1; s0=$?
$C87 --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
$C87 --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc95check_refuses.txt 2>&1; s3=$?
say "source check (kc87_syscheck_1025.py on macm3's k_c 87 D 22.375 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc95_syscheck on the k_c 87 source exit $s3 (1 wanted): $(tail -n 3 $OUT/source_syscheck.txt | cut -c1-330 | tr '\n' ' ')"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
[ "$MODE" = check ] && { say "check run: source accepted, nothing regridded"; exit 0; }
# 4. the regrid (the source goes into the regrid worktree's data/ under the name ell_refine.py reads)
cp $STATE $WTM/data/sol_${SRC}_D22.3750.npy
[ "$(blob $WTM/data/sol_${SRC}_D22.3750.npy | cut -c1-8)" = d7bfdaa2 ] || stop "copied source state blob differs"
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 87 $TAG 95 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $OUT/regrid.log
say "regrid starts: $CMD"
( while sleep 60; do
    echo "$(stamp),$(ps -C python -o rss=,pcpu=,nlwp=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-4)" >> $OUT/regrid_samples.csv
    av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$av" -lt $MEMSTOP ] && echo "$(stamp) UTC MemAvailable $av kB below 4 GiB (alert only; nothing is stopped)" >> $OUT/MEMALERT.txt
  done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
say "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap of 6 h)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D22.3750.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $F/ ; cp $WTM/data/sol_${TAG}_D22.3750.npy $F/
C95="nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D22.3750.npy $D $WTM"
$C95 > $OUT/syscheck.txt 2>&1; c0=$?
$C95 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?
$C95 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D22.3750.npy $D $WTM > $OUT/syscheck_kc87check_refuses.txt 2>&1; c3=$?
say "kc95 syscheck exit $c0 (0 wanted); controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each); kc87_syscheck on the k_c 95 result exit $c3 (1 wanted)"
if [ $c0 = 0 ] && [ $c1 = 1 ] && [ $c2 = 1 ] && [ $c3 = 1 ]; then
  cp $F/sol_${TAG}_D22.3750.npy $F/$TAG.jsonl $IN/
  { echo "$(blob $IN/sol_${TAG}_D22.3750.npy) sol_${TAG}_D22.3750.npy"; echo "$(blob $IN/$TAG.jsonl) $TAG.jsonl"; } > $F/in_blobs_regrid.txt
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else echo "REFUSED: syscheck $c0, controls $c1 $c2, kc87 check on the result $c3" > $OUT/VERDICT.txt; stop "the regrid result is not accepted: $(cat $OUT/VERDICT.txt)"; fi
say "verdict: $(cat $OUT/VERDICT.txt); $(tail -n 3 $OUT/syscheck.txt | cut -c1-330 | tr '\n' ' ')"
bash $PUSH I1025-dh610/kc95_d22375 "I1025-dh610/kc95_d22375: k_c 95 D 22.375 regrid accepted" > $F/push_regrid.txt 2>&1
# 5. the scan: wait for memory (a wait, not a stop), then 7 processes
# the coordinator's order: the wide scan runs on 4 processes (17 evaluations: p0 -0.10 0.06 0.22 0.38 and the repeat of 0.14, p1 -0.06 0.10 0.26 0.42, p2 -0.02 0.14 0.30 0.46, p3 0.02 0.18 0.34 0.50)
NP=4
tw=$(date +%s)
while :; do
  av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
  [ "$av" -ge $(( NP * RSS_GUESS + 4000000 )) ] && break
  [ -e $F/scan_mem_wait.txt ] || say "waiting for memory: MemAvailable $av kB is below $NP x $RSS_GUESS kB + 4 GB (nothing is stopped)"
  echo "$(stamp) UTC MemAvailable $av kB" > $F/scan_mem_wait.txt
  [ $(( $(date +%s) - tw )) -lt 21600 ] || stop "the memory wait before the scan ended after 6 h"
  sleep 60
done
say "scan memory gate passed (MemAvailable $av kB, waited $(( $(date +%s) - tw )) s, load $(cut -d' ' -f1-3 /proc/loadavg))"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WF
SST=$IN/sol_${TAG}_D22.3750.npy; SREC=$IN/$TAG.jsonl
LISTS=("-0.10,0.06,0.22,0.38,0.14" "-0.06,0.10,0.26,0.42" "-0.02,0.14,0.30,0.46" "0.02,0.18,0.34,0.50")
say "scan: lambda -0.10 to 0.50 by 0.04 and a repeat of 0.14 (17 evaluations), lists ${LISTS[*]}, $NP processes of 1 thread, nice 10, cap 28800 s each"
pids=()
for ((j = 0; j < NP; j++)); do
  ( cd $WF && nice -n 10 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $SREC $SST $D ${LISTS[$j]} $S/scan_D${D}_p$j.jsonl < /dev/null > $S/scan_p$j.raw 2>&1
    echo "$(stamp) UTC scan p$j (${LISTS[$j]}) exit $?" >> $L ) &
  pids+=($!)
done
( sleep 10; while pgrep -f "d18_hybsign.py.*sol_${TAG}_D22.3750" > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(stamp) UTC alive $(pgrep -f "d18_hybsign.py.*sol_${TAG}_D22.3750" | wc -l), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/scan_D${D}_p*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(stamp) UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_scan.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for ((j = 0; j < NP; j++)); do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/scan_p$j.raw > $S/scan_p$j.log; say "p$j: $(grep -E 'record system' $S/scan_p$j.log | head -1 | cut -c1-150)"; done
cat $S/scan_D${D}_p*.jsonl | $PY -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: (r['lam'], r['sec']))
open('$S/scan_D${D}_all.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" | tee -a $L
# 6. the reading
( cd $IN; { echo "=== read_lower.py $S -0.10 0.50"; $PY -W ignore read_lower.py $S -0.10 0.50; echo "read_lower exit $?"; echo "=== repeat_check.py (merged scan file)"; $PY repeat_check.py $S/scan_D${D}_all.jsonl; echo "repeat_check exit $?"; } > $F/read_lower.txt 2>&1
  $PY -I $F/wide_read.py $F/read_lower.txt > $F/wide_read.txt 2>&1 )
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(' $F/wide_read.txt | tr '\n' ' ' | cut -c1-700)"
[ "$(grep -c '   change (' $F/wide_read.txt)" = 0 ] && say "no robust change in the window: reported as read"
bash $PUSH I1025-dh610/kc95_d22375 "I1025-dh610/kc95_d22375: D 22.375 scan rows and reading" > $F/push_scan.txt 2>&1
say "scan done; readings in read_lower.txt and wide_read.txt; kc95 D 22.375 point done"
exit 0
}
