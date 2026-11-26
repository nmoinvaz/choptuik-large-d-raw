#!/bin/bash
# #1025 kc135_d230625 (dh610), the coordinator's order of 26 Nov (hc): k_c 135 at D 23.0625 from macm3's accepted k_c 127 state there (raw I1025-macm3/kc127_d230625/in: state blob 7aae10c6, record blob 85a685f1; the source check
# kc127_syscheck_1025.py 898ebefa exits 0 with controls 1 1 and the k_c 119 (fc6e0dd6) and k_c 135 (b353d466, raw 576050bfc) checks refuse it), ell_refine.py in solver/matter of the worktree 48c36355 (`--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60
# --no-gamma`, 6 threads, nice 10 raised to 19 by watch_i1088a.sh while an i1088a unit is active, cap 43200 s, lambda_0(23.0625) = 2.0990016035 from ell_delta.lam0_at), accepted only by kc135_syscheck_1025.py (b353d466: selftest, both controls exit 1,
# the k_c 127 check refusing the result); then stage_scan.sh, a separate file read when it starts (`d18_secant.py scan`, wip/ell1-speed 92b9bf53, blob eb1396ad: lambda 0.00, 0.005, 0.01, 0.015 and a repeat of 0.01 on 4 processes, then read_lower.py,
# repeat_check.py, leg_read.py against PRED 0.008, bar 0.004); the secant is not run here (it goes to macm3 or winb). Stops (and the runner reports) on: a pin that differs, a selftest or control that does not read as written, the source not
# accepted, the regrid not accepted or with an exception (including an array limit at k_c 135) or over the cap, a stage that fails; no robust change in the window is reported as read, with no widening. Nothing is stopped or terminated for memory
# (Nathan's rule of 2026-11-08). usage: bash lane_kc135.sh [dry|check]   (dry stops after the selftests, check after the source check)
{
set -u
MODE=${1:-}
source /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc135_d230625/common_kc135.sh
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
mkdir -p $OUT $S
av0=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
say "start (mode ${MODE:-full}; load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $av0 kB)"
[ "$MODE" != dry ] && [ "$av0" -lt $MEMSTART ] && stop "MemAvailable $av0 kB is below 8 GiB"
# 1. pins
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || stop "$IN/$f missing or not blob $bb"; done < $F/in_blobs.txt
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || stop "$IN/$f missing or not blob $bb"; done < $F/in_blobs_src.txt
diff -u $IN/kc127_syscheck_1025.py $IN/kc135_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
tail -n +3 $F/kc135_syscheck_1025.diff | cmp -s - $OUT/diff_rebuilt.txt || stop "kc135_syscheck_1025.diff is not the diff of the k_c 127 and k_c 135 checks"
[ "$(grep -c '^[-+][^-+]' $OUT/diff_rebuilt.txt)" = 8 ] || stop "the diff of the two checks is not four changed lines each side (a comment line and the three lines with the k_c number)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ "$(blob $WTM/ell_delta.py | cut -c1-8)" = fde699f5 ] || stop "ell_delta.py is not blob fde699f5"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WTF rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WTF status --short)" ] || stop "$WTF is not clean at 505d8399"
[ "$(git -C $SW rev-parse HEAD)" = 92b9bf533ff371247be642c47e067a9042cabed1 ] && [ -z "$(git -C $SW status --short)" ] || stop "$SW is not clean at 92b9bf53"
[ "$(blob $SWM/d18_secant.py | cut -c1-8)" = eb1396ad ] && [ "$(blob $SWM/ell_fastm.py | cut -c1-8)" = 93f963f6 ] || stop "d18_secant.py or ell_fastm.py is not the pinned blob (eb1396ad, 93f963f6)"
for f in dss_ell ell_ddm ell_dd ddnp; do [ "$(blob $SWM/$f.py)" = "$(blob $WTM/$f.py)" ] || stop "$f.py of the secant worktree differs from the regrid worktree's"; done
[ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"
[ -e $S/scan_D${D}_p0.jsonl ] && [ -z "$MODE" ] && stop "$S/scan_D${D}_p0.jsonl exists"
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$($PY -c "print(abs($L0 - $LAM0) < 1e-10)")" = True ] || stop "lambda_0($D) reads $L0, not $LAM0"
$PY -c "import multidouble; assert hasattr(multidouble, 'dd_logdet')" || stop "the venv's multidouble has no dd_logdet"
say "pins checked (in_blobs.txt, in_blobs_src.txt), diff of the k_c 127 and k_c 135 checks rebuilt (a comment line and 3 lines, 4 each side), worktrees 1025g 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801, ell_delta.py fde699f5), 1025f 505d8399 and 1025s 92b9bf53 clean (d18_secant.py eb1396ad, ell_fastm.py 93f963f6, the four shared files equal 1025g's); lambda_0($D) $L0; $($PY -VV 2>&1 | head -1 | cut -c1-30), multidouble $($PY -c 'import multidouble as m; print(m.__version__)' 2>/dev/null)"
# 2. selftests
export D18_DIR=$IN
( cd $IN
  nice -n 10 $PY -I kc119_syscheck_1025.py --selftest > $F/selftest_kc119_syscheck.log 2>&1; a0=$?
  nice -n 10 $PY -I kc127_syscheck_1025.py --selftest > $F/selftest_kc127_syscheck.log 2>&1; a1=$?
  nice -n 10 $PY -I kc135_syscheck_1025.py --selftest > $F/selftest_kc135_syscheck.log 2>&1; a2=$?
  $PY -W ignore read_lower.py selftest > $F/selftest_read_lower.log 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $F/selftest_read_lower_mutate_shift.log 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $F/selftest_read_lower_mutate_round2.log 2>&1; r2=$?
  $PY repeat_check.py selftest > $F/selftest_repeat_check.log 2>&1; r3=$?
  $PY -I leg_read.py selftest > $F/selftest_leg_read.log 2>&1; g0=$?
  $PY -I leg_read.py selftest --mutate > $F/selftest_leg_read_mutate.log 2>&1; g1=$?
  cd $SWM
  nice -n 10 $PY d18_secant.py selftest > $F/selftest_d18_secant.log 2>&1; k0=$?
  nice -n 10 $PY d18_secant.py selftest --mutate=half > $F/selftest_d18_secant_half.log 2>&1; k1=$?
  nice -n 10 $PY d18_secant.py selftest --mutate=norobust > $F/selftest_d18_secant_norobust.log 2>&1; k2=$?
  nice -n 10 $PY d18_secant.py selftest --mutate=nosigncheck > $F/selftest_d18_secant_nosigncheck.log 2>&1; k3=$?
  echo "$a0 $a1 $a2 $r0 $r1 $r2 $r3 $g0 $g1 $k0 $k1 $k2 $k3" > $F/selftest_exits.txt )
read -r a0 a1 a2 r0 r1 r2 r3 g0 g1 k0 k1 k2 k3 < $F/selftest_exits.txt
[ "$a0 $a1 $a2 $r0 $r1 $r2 $r3 $g0 $g1 $k0 $k1 $k2 $k3" = "0 0 0 0 1 1 0 0 1 0 1 1 1" ] || stop "the selftests did not behave (kc119_syscheck $a0, kc127_syscheck $a1, kc135_syscheck $a2, read_lower $r0 $r1 $r2, repeat_check $r3, leg_read $g0 $g1, d18_secant $k0 and half $k1, norobust $k2, nosigncheck $k3; wanted 0 0 0 0 1 1 0 0 1 0 1 1 1)"
say "selftests as wanted (kc119_syscheck, kc127_syscheck, kc135_syscheck, read_lower, mutate shift, mutate round2, repeat_check, leg_read, mutate, d18_secant, half, norobust, nosigncheck: 0 0 0 0 1 1 0 0 1 0 1 1 1)"
[ -z "$(git -C $SW status --short)" ] || stop "the selftests changed the secant worktree"
[ "$MODE" = dry ] && { say "dry run: nothing started"; exit 0; }
# 3. the source: kc127_syscheck accepts it with both controls exit 1, and kc119_syscheck and kc135_syscheck refuse it
STATE=$IN/sol_${SRC}_D${DS}.npy; REC=$IN/$SRC.jsonl
C127="nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $REC $STATE $D $WTM"
$C127 > $OUT/source_syscheck.txt 2>&1; s0=$?
$C127 --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
$C127 --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc119_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc119check_refuses.txt 2>&1; s3=$?
nice -n 10 $PY -I $IN/kc135_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc135check_refuses.txt 2>&1; s4=$?
say "source check (kc127_syscheck_1025.py on macm3's k_c 127 D 23.0625 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc119_syscheck exit $s3 and kc135_syscheck exit $s4 on macm3's k_c 127 source (1 wanted each): $(tail -n 3 $OUT/source_syscheck.txt | cut -c1-300 | tr '\n' ' ')"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] && [ $s4 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
[ "$MODE" = check ] && { say "check run: source accepted, nothing regridded"; exit 0; }
# 4. the regrid (the source goes into the regrid worktree's data/ under the name ell_refine.py reads)
[ -e $WTM/data/sol_${SRC}_D${DS}.npy ] || cp $STATE $WTM/data/sol_${SRC}_D${DS}.npy
[ "$(blob $WTM/data/sol_${SRC}_D${DS}.npy | cut -c1-8)" = 7aae10c6 ] || stop "the source state in the regrid worktree is not blob 7aae10c6"
CMD="nice -n 10 timeout 43200 $PY -u ell_refine.py $SRC 127 $TAG 135 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 6 threads, nice 10, cap 43200 s): $CMD" > $OUT/regrid.log
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
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap of 12 h)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D${DS}.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $F/ ; cp $WTM/data/sol_${TAG}_D${DS}.npy $F/
C135="nice -n 10 $PY -I $IN/kc135_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D${DS}.npy $D $WTM"
$C135 > $OUT/syscheck.txt 2>&1; c0=$?
$C135 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?
$C135 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D${DS}.npy $D $WTM > $OUT/syscheck_kc127check_refuses.txt 2>&1; c3=$?
nice -n 10 $PY -I $IN/kc119_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D${DS}.npy $D $WTM > $OUT/syscheck_kc119check_refuses.txt 2>&1; c4=$?
say "kc135 syscheck exit $c0 (0 wanted); controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each); kc127_syscheck exit $c3 and kc119_syscheck exit $c4 on the k_c 135 result (1 wanted each)"
if [ $c0 = 0 ] && [ $c1 = 1 ] && [ $c2 = 1 ] && [ $c3 = 1 ] && [ $c4 = 1 ]; then
  cp $F/sol_${TAG}_D${DS}.npy $F/$TAG.jsonl $IN/
  { echo "$(blob $IN/sol_${TAG}_D${DS}.npy) sol_${TAG}_D${DS}.npy"; echo "$(blob $IN/$TAG.jsonl) $TAG.jsonl"; } > $F/in_blobs_regrid.txt
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else echo "REFUSED: syscheck $c0, controls $c1 $c2, kc127 check on the result $c3, kc119 check on the result $c4" > $OUT/VERDICT.txt; stop "the regrid result is not accepted: $(cat $OUT/VERDICT.txt)"; fi
say "verdict: $(cat $OUT/VERDICT.txt); $(tail -n 3 $OUT/syscheck.txt | cut -c1-330 | tr '\n' ' ')"
bash $PUSH I1025-dh610/kc135_d230625 "I1025-dh610/kc135_d230625: k_c 135 D 23.0625 regrid accepted" > $F/push_regrid.txt 2>&1
# 5. the stages, each read when it starts
for st in stage_scan.sh; do
  say "stage $st starts (blob $(blob $F/$st | cut -c1-8))"
  bash $F/$st; rc=$?
  [ $rc = 0 ] || halt "stage $st exit $rc"
done
say "kc135 D 23.0625 point done; readings in read_lower.txt and leg_read.txt"
exit 0
}
