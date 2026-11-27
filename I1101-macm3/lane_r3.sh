#!/bin/bash
# RUST BLOCK 12 (t5, hc 04:23 UTC 27 Nov 2026, #1102): the scan (pointr3.sh) and the secant of this lane run with --b12=rust --b12_threads=4 (ellrs in ~/Source/ellrs-site-1102m3, worktree 1102m3 at d4b6b6ce, d18_secant.py 9706e506); changes read in rust_b12/diff_lane_rs.txt and the README.
# #1101 macm3 R3 (t5's order, hc 27 Nov 17:4x UTC and #1101 comment 7224728711): a RE-SOLVE AT KAPPA 0.25 from R1's state (l1kc127k050m3: kappa 0.5, 5847 steps, blobs 0124dbd2 and 944a8179), tag l1kc127k025m3, in the 48c36355 worktree
# (ell_refine.py 631e5801, dss_ell.py 5d28c19e): the fourth consistent kappa point (R0 0.7: 0.045968, R1 0.5: 0.09500769, R2 0.35: in (0.100, 0.129367)). Derived from lane_r1.sh by mk_r3.py (diff_lane_r3.txt): tags, kappa 0.25, bars |F| <= 5e-10 and
# steps 11700 +- 2% (11466 to 11934, STOP when not met), the scan of lambda 0.100, 0.115, 0.130, 0.145 with the result's own steps (pointr3.sh = pointr3.sh with the repeat optional and one process; no --kappa_mm; scanner d18_secant.py 9706e506), the secant at tol 5e-5
# on the change; no change: the scan of 0.085 and 0.160, merged with the first scan (merge_scans.py) and read as one (6 points required), then the secant on the change; the root against 0.111 (kappa^4), 0.120 (kappa^3), 0.133 (kappa^2). An hc at the regrid's start and end.
# Stops (hc to t5): a source or result not accepted, a bar not met, an exception (an array limit included), a reading of fewer points than evaluations, more than one robust change, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane_r3.sh [dry|check]
{
set -u
MODE=${1:-}
F=$HOME/Source/choptuik-large-d-raw-903/I1101-macm3; IN=$F/in; K=$F/r3; OUT=$K/regrid; C=$K/checks
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
WT=$HOME/Source/choptuik-large-d-1025m2; WTM=$WT/solver/matter
WT5=$HOME/Source/choptuik-large-d-1025m; WTM5=$WT5/solver/matter
WTS=$HOME/Source/choptuik-large-d-1102m3/solver/matter; SITE=$HOME/Source/ellrs-site-1102m3   # Rust block 12 (t5, hc 04:23 UTC 27 Nov, #1102): the scanner worktree is the branch's
PY=$HOME/Source/venv-macm3-1058b/bin/python; RAWG=$HOME/Source/choptuik-large-d-raw-1076p
SRC=l1kc127k050m3; TAG=l1kc127k025m3; D=23.0; DT=D23.0000; SRCFILE=sol_${SRC}_D23.0000.npy; LAM0=2.0992182200; DN=23.0_r3k025; DNX=23.0_r3k025_ext; DNG=23.0_r3k025_m; SCAN=$L/$DN; SCANX=$L/$DNX; SCANG=$L/$DNG; SEC=$K/secant
HC=$(command -v hc); LOG=$K/exits_r3.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC I1101 R3: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; tell "macm3 #1101 R3 STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $OUT $C
export PYTHONDONTWRITEBYTECODE=1
say "start (mode ${MODE:-full}; load $(sysctl -n vm.loadavg), $(availgib) GiB available)"
# 1. pins
while read bb f; do case "$bb" in "#"*) continue;; esac
  p=$F/$f; [ -f $p ] && [ "$(blob $p | cut -c1-8)" = "$bb" ] || stop "$p missing or not blob $bb"; done < $K/in_blobs.txt
diff -u $IN/kc135_syscheck_1025.py $IN/kc143_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
[ "$(grep -c '^[-+][^-+]' $OUT/diff_rebuilt.txt)" = 8 ] && [ "$(grep -c '^-[^-].*135' $OUT/diff_rebuilt.txt)" = 4 ] && [ "$(grep -c '^+[^+].*143' $OUT/diff_rebuilt.txt)" = 4 ] || stop "the diff of the k_c 135 and k_c 143 checks is not a header comment line and three lines changed from 135 to 143"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree $WT not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] && [ "$(blob $WTM/ell_delta.py | cut -c1-8)" = fde699f5 ] || stop "ell_refine.py or ell_delta.py is not 631e5801 / fde699f5"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WT5 rev-parse --short=8 HEAD)" = 505d8399 ] && [ -z "$(git -C $WT5 status --short solver | grep -v 'solver/matter/data/')" ] || stop "the scan worktree $WT5 is not clean at 505d8399"
[ "$(git -C ${WTS%/solver/matter} rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ "$(blob $WTS/d18_secant.py | cut -c1-8)" = 9706e506 ] || stop "the scanner worktree is not at d4b6b6ce with d18_secant.py 9706e506"
[ "$(blob $WTS/ell_b12rs.py | cut -c1-8)" = a1fff74f ] && [ -z "$(git -C ${WTS%/solver/matter} status --short solver)" ] || stop "ell_b12rs.py is not a1fff74f or the scanner worktree is not clean"
[ "$(shasum -a 256 $SITE/ellrs/ellrs.cpython-314-darwin.so | cut -c1-12)" = d2221460d02c ] || stop "the ellrs module in $SITE is not the one gated (sha256 d2221460d02c)"
for f in dss_ell ell_ddm ell_dd ddnp; do [ "$(blob $WTS/$f.py | cut -c1-8)" = "$(blob $WTM5/$f.py | cut -c1-8)" ] || stop "$f.py of the scanner worktree differs from the scan worktree's (505d8399)"; done
[ "$MODE" != dry ] && [ "$MODE" != check ] && { [ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"; [ -e $WTM/data/sol_${TAG}_$DT.npy ] && stop "the result state exists in $WTM/data"; }
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print('%.10f' % ell_delta.lam0_at($D, *ell_delta.lam0_table())[0])")
python3 -c "import sys; sys.exit(0 if abs(float('$L0') - float('$LAM0')) < 1e-10 else 1)" || stop "lambda_0($D) reads $L0, not $LAM0"
say "pins checked (in_blobs.txt; the diff of the k_c 135 and k_c 143 checks: a header comment line and 3 lines changed from 135 to 143), worktrees $WT 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801, ell_delta.py fde699f5), $WT5 505d8399 and the scanner worktree d4b6b6ce (d18_secant.py 9706e506, ell_b12rs.py a1fff74f, ellrs sha256 d2221460d02c in $SITE) clean; lambda_0($D) $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# 2. selftests
export D18_DIR=$IN OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
( cd $IN
  nice -n 10 $PY -I kc127_syscheck_1025.py --selftest > $C/selftest_kc127_syscheck.txt 2>&1; a0=$?
  nice -n 10 $PY -I kc135_syscheck_1025.py --selftest > $C/selftest_kc135_syscheck.txt 2>&1; a1=$?
  nice -n 10 $PY -I kc143_syscheck_1025.py --selftest > $C/selftest_kc143_syscheck.txt 2>&1; a2=$?
  $PY -W ignore read_lower.py selftest > $C/selftest_read_lower.txt 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $C/selftest_read_lower_shift.txt 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $C/selftest_read_lower_round2.txt 2>&1; r2=$?
  $PY repeat_check.py selftest > $C/selftest_repeat_check.txt 2>&1; r3=$?
  echo "$a0 $a1 $a2 $r0 $r1 $r2 $r3" > $C/selftest_exits.txt )
[ "$(cat $C/selftest_exits.txt)" = "0 0 0 0 1 1 0" ] || stop "the selftests did not behave ($(cat $C/selftest_exits.txt); wanted 0 0 0 0 1 1 0: kc127_syscheck, kc135_syscheck, kc143_syscheck, read_lower, mutate shift, mutate round2, repeat_check)"
say "selftests as wanted (0 0 0 0 1 1 0)"
# 2b. the new scanner (t5's order): selftest exit 0, --mutate=half|norobust|nosigncheck exit 1 each, logged
( cd $WTS && export PYTHONPATH=$SITE RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  nice -n 10 $PY d18_secant.py selftest > $C/newscan_selftest.txt 2>&1; n0=$?; nx="$n0"
  for m in half norobust nosigncheck; do nice -n 10 $PY d18_secant.py selftest --mutate=$m > $C/newscan_selftest_$m.txt 2>&1; nx="$nx $?"; done
  for m in "" nolam harm; do nice -n 10 $PY ell_b12rs.py selftest ${m:+--mutate=$m} > $C/b12rs_selftest${m:+_$m}.txt 2>&1; nx="$nx $?"; done
  echo "$nx" > $C/newscan_exits.txt )
[ "$(cat $C/newscan_exits.txt)" = "0 1 1 1 0 1 1" ] || stop "the new scanner's and ell_b12rs's selftest exits '$(cat $C/newscan_exits.txt)' (wanted '0 1 1 1 0 1 1': selftest, half, norobust, nosigncheck, ell_b12rs selftest, nolam, harm)"
say "new scanner d18_secant.py (blob $(blob $WTS/d18_secant.py | cut -c1-8), worktree d4b6b6ce): selftest exit 0, --mutate=half exit 1, --mutate=norobust exit 1, --mutate=nosigncheck exit 1; ell_b12rs.py selftest exit 0, --mutate=nolam exit 1, --mutate=harm exit 1 (logged before the scan, as t5 ordered)"
# 3. the source: the k_c 127 check accepts it with controls 1 1; the k_c 135 and k_c 143 checks refuse it
STATE=$IN/$SRCFILE; REC=$IN/$SRC.jsonl
C127S="nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $REC $STATE $D $WTM"
$C127S > $OUT/source_syscheck.txt 2>&1; s0=$?; $C127S --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?; $C127S --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc135_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc135check_refuses.txt 2>&1; s3=$?
nice -n 10 $PY -I $IN/kc143_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc143check_refuses.txt 2>&1; s4=$?
say "source check (R1's k_c 127 state at D $D, I1101 R1, kappa 0.5): kc127_syscheck exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc135_syscheck on the source exit $s3, kc143_syscheck on the source exit $s4 (1 wanted each): $(grep -E '^D ' $OUT/source_syscheck.txt | cut -c1-300)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] && [ $s4 = 1 ] || stop "the source check or a control did not read as written"
[ "$MODE" = dry ] && { say "dry run: pins, selftests and the source check passed; nothing started"; exit 0; }
[ "$MODE" = check ] && { say "check run: nothing regridded"; exit 0; }
# 4. wait for no other scan or regrid, then for memory
while pgrep -f 'd18_hybsign|ell_refine|d18_secant.py run' > /dev/null; do sleep 30; done
while python3 -c "import sys; sys.exit(0 if $(availgib) >= 8 else 1)"; [ $? != 0 ]; do sleep 60; done
# 5. the regrid (only the state is copied into the worktree's data, under the name ell_refine reads)
[ -e $WTM/data/sol_${SRC}_$DT.npy ] && [ "$(blob $WTM/data/sol_${SRC}_$DT.npy | cut -c1-8)" = 0124dbd2 ] || cp $STATE $WTM/data/sol_${SRC}_$DT.npy
[ "$(blob $WTM/data/sol_${SRC}_$DT.npy | cut -c1-8)" = 0124dbd2 ] || stop "copied source state blob differs"
[ "$(blob $REC | cut -c1-8)" = 944a8179 ] || stop "the source record blob differs"
CMD="nice -n 10 $PY -u $IN/capped_run.py 28800 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_refine.py $SRC 127 $TAG 127 1 $D $LAM0 --kappa 0.25 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM): $CMD" > $OUT/regrid.log
say "regrid starts: $CMD"
tell "macm3 #1101 R3 START (pilot): R1's k_c 127 D 23.0 state (0124dbd2, record 944a8179: |F| 3.12e-10, steps 5847 at kappa 0.5) accepted by the k_c 127 check (controls 1 1, the k_c 135 and k_c 143 checks refuse it); the pins and selftests as wanted; regrid at kappa 0.25 starts now: $(echo $CMD | sed 's/.*ell_refine.py/ell_refine.py/'); bars |F| <= 5e-10 and steps 11700 +- 2%, 6 threads, cap 28800 s, load $(sysctl -n vm.loadavg), $(availgib) GiB available"
echo "time_utc,rss_kB,pcpu,avail_GiB" > $OUT/regrid_samples.csv
( while sleep 60; do
    echo "$(stamp),$(ps -axo rss=,pcpu=,command= | grep 'ell_refine.py' | grep -v grep | grep -v capped_run | head -1 | awk '{print $1","$2}'),$(availgib)" >> $OUT/regrid_samples.csv
    av=$(availgib); python3 -c "import sys; sys.exit(0 if $av < 2 else 1)" && echo "$(stamp) UTC $av GiB available (alert only; nothing is stopped)" >> $OUT/MEMALERT.txt
  done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
say "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap of 8 h)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_$DT.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $IN/ ; cp $WTM/data/sol_${TAG}_$DT.npy $IN/
C127R="nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM"
$C127R > $OUT/syscheck.txt 2>&1; c0=$?; $C127R --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?; $C127R --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $IN/kc135_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM > $OUT/syscheck_kc135check_refuses.txt 2>&1; c3=$?
nice -n 10 $PY -I $IN/kc143_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM > $OUT/syscheck_kc143check_refuses.txt 2>&1; c4=$?
say "kc127 syscheck exit $c0 (0 wanted); controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each); kc135_syscheck on the result exit $c3, kc143_syscheck on the result exit $c4 (1 wanted each): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-300)"
[ $c0 = 0 ] && [ $c1 = 1 ] && [ $c2 = 1 ] && [ $c3 = 1 ] && [ $c4 = 1 ] || stop "the regrid result is not accepted (syscheck $c0, controls $c1 $c2, kc135 check on the result $c3, kc143 check on the result $c4)"
# t5's bars: |F| <= 5e-10 and steps 11700 +- 2% (5734 to 5968)
python3 - $IN/$TAG.jsonl $D <<'PY' > $OUT/bars.txt; bars=$?
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip() and json.loads(l)["D"] == float(sys.argv[2])][-1]
okF = rec["F"] <= 5e-10; okS = 11700 * 0.98 <= rec["steps"] <= 11700 * 1.02
print("bars: |F| %.4e <= 5e-10: %s; steps %d in [%.1f, %.1f] (11700 +- 2%%, %+.2f%%): %s" % (rec["F"], okF, rec["steps"], 11700 * 0.98, 11700 * 1.02, 100.0 * (rec["steps"] / 11700.0 - 1), okS))
sys.exit(0 if okF and okS else 1)
PY
say "$(cat $OUT/bars.txt)"
[ $bars = 0 ] || stop "a bar of t5's is not met: $(cat $OUT/bars.txt)"
echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
{ echo "$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8) sol_${TAG}_$DT.npy"; echo "$(blob $IN/$TAG.jsonl | cut -c1-8) $TAG.jsonl"; } > $K/in_blobs_regrid.txt
python3 - $IN/$TAG.jsonl $IN/$SRC.jsonl $D <<'PY' > $OUT/regrid_summary.txt
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip()][-1]; src = [json.loads(l) for l in open(sys.argv[2]) if l.strip() and json.loads(l)["D"] == float(sys.argv[3])][-1]
print("kappa 0.25 record: D %r |F| %.4e steps %d psi-constraint %.4e Delta %.12f (R1 kappa 0.5 source: |F| %.4e steps %d constraint %.4e Delta %.12f); Delta shift %+.4e, steps ratio %.3f, constraint ratio %.3f" % (
    rec["D"], rec["F"], rec["steps"], rec["constraint"], rec["Delta"], src["F"], src["steps"], src["constraint"], src["Delta"], rec["Delta"] - src["Delta"], rec["steps"] / src["steps"], rec["constraint"] / src["constraint"]))
PY
RP=$(bash $F/push_i1101.sh "I1101-macm3: R3 regrid accepted (state, record, checks)" 2>&1 | tail -1); say "pushed regrid: $RP"
tell "macm3 #1101 R3 regrid END: ACCEPTED ($(cat $OUT/regrid_summary.txt)); $(cat $OUT/bars.txt); regrid wall $(( $(date +%s) - t0 )) s; the scan of lambda 0.100 0.115 0.130 0.145 (own steps, 1 process) starts now; raw $RP"
# 6. the scan folder (pins from the pushed commit), the lock, then point87.sh scan
RAWC=$(echo "$RP" | awk '{print $2}')
git -C $RAWG cat-file -e $RAWC:I1101-macm3/in/$TAG.jsonl 2>/dev/null || stop "the pushed commit $RAWC does not hold the regrid record"
mkdir -p $SCAN
{ cat <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=sol_${TAG}_$DT.npy
STATEBLOB=$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8)
RECBLOB=$(blob $IN/$TAG.jsonl | cut -c1-8)
SRC=I1101-macm3/in
PENV
  cat $K/scan_plan.env; } > $SCAN/point.env
bash $L/prepare87.sh $DN > $SCAN/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCAN/prepare.log)"
for f in sol_${TAG}_$DT.npy; do cp $SCAN/in/$f $WTM5/data/$f; done; cp $SCAN/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
echo "ACCEPTED $(stamp) UTC (the k_c 127 check of the lane on the kappa 0.25 result, $OUT/syscheck.txt; controls and the k_c 135 and k_c 143 refusals in $OUT; t5's bars $OUT/bars.txt)" > $SCAN/VERDICT.txt
echo "$(stamp) UTC accept (lane_r3.sh): kc127_syscheck_1025.py exit $c0 (0 wanted); controls exit $c1 $c2 (1 wanted); kc135 and kc143 checks on the result exit $c3 $c4 (1 wanted each): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN pins and verdict (I1101 R3, kappa 0.25)" > /dev/null 2>&1
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "scan starts (pointr3.sh $DN scan: the scanner d18_secant.py scan with --b12=rust --b12_threads=4)"
bash $F/pointr3.sh $DN scan >> $SCAN/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "scan exit $sc"
[ -e $SCAN/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCAN/steps.txt)"
bash $L/push87.sh "kc87_leg_lambda: D $DN (I1101 R3) scan done" > /dev/null 2>&1
nch=$(grep -c 'robust change (' $SCAN/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCAN/read_lower.txt | head -1 | grep -o '[0-9]*')
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint|^repeated|^float64' $SCAN/read_lower.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1101 R3: the scan is read: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint' $SCAN/read_lower.txt | tr '\n' ';' | cut -c1-900) (raw kc87_leg_lambda/$DN/)"
RL=$SCAN/read_lower.txt; SUMD=$SCAN
if [ "$nch" = 0 ] && [ "$nrb" = 0 ]; then
  # t5's order: none: widen to 0.085 and 0.160, merged with the first scan for one reading, then the secant on the change
  tell "macm3 #1101 R3: the scan reads 0 robust changes in 0.100-0.145 ($(grep -h '^hybrid signs' $SCAN/read_lower.txt | head -1)): the scan of 0.085 and 0.160 starts now (your order), merged with it for one reading of 6 points, then the secant on the change"
  mkdir -p $SCANX
{ cat <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=sol_${TAG}_$DT.npy
STATEBLOB=$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8)
RECBLOB=$(blob $IN/$TAG.jsonl | cut -c1-8)
SRC=I1101-macm3/in
PENV
  cat $K/scan_plan_ext.env; } > $SCANX/point.env
bash $L/prepare87.sh $DNX > $SCANX/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCANX/prepare.log)"
for f in sol_${TAG}_$DT.npy; do cp $SCANX/in/$f $WTM5/data/$f; done; cp $SCANX/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
echo "ACCEPTED $(stamp) UTC (the k_c 127 check of the lane on the kappa 0.25 result, $OUT/syscheck.txt; controls and the k_c 135 and k_c 143 refusals in $OUT; t5's bars $OUT/bars.txt)" > $SCANX/VERDICT.txt
echo "$(stamp) UTC accept (lane_r3.sh): kc127_syscheck_1025.py exit $c0 (0 wanted); controls exit $c1 $c2 (1 wanted); kc135 and kc143 checks on the result exit $c3 $c4 (1 wanted each): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-260)" >> $SCANX/steps.txt
bash $L/push87.sh "kc87_leg_lambda: D $DNX pins and verdict (I1101 R3 extension)" > /dev/null 2>&1
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "extension scan starts (pointr3.sh $DNX scan: the scanner d18_secant.py scan with --b12=rust --b12_threads=4)"
bash $F/pointr3.sh $DNX scan >> $SCANX/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "extension scan exit $sc"
[ -e $SCANX/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCANX/steps.txt)"
bash $L/push87.sh "kc87_leg_lambda: D $DNX (I1101 R3 extension) scan done" > /dev/null 2>&1
    $PY $F/merge_scans.py $DNG $DN $DNX > $K/merge_scans.txt 2>&1; mg=$?
  m1=1; m2=1; m3=1; $PY $F/merge_scans.py ${DNG}_mut $DN $DNX --mutate=dup > /dev/null 2>&1; m1=$?; $PY $F/merge_scans.py ${DNG}_mut $DN $DNX --mutate=state > /dev/null 2>&1; m2=$?; $PY $F/merge_scans.py ${DNG}_mut $DN $DNX --mutate=log > /dev/null 2>&1; m3=$?
  say "merge exit $mg (0 wanted), its mutations dup exit $m1, state exit $m2, log exit $m3 (1 wanted each): $(tail -1 $K/merge_scans.txt | cut -c1-300)"
  [ $mg = 0 ] && [ $m1 = 1 ] && [ $m2 = 1 ] && [ $m3 = 1 ] || stop "the merge of the two scans or its controls did not read as wanted ($mg $m1 $m2 $m3)"
  mv $L/${DNG}_mut $L/${DNG}_mut.removed.$(date +%s) 2>/dev/null
  ( cd $L/common/in
    { echo "== window: read_lower.py scan 0.085 0.160 (merged: $DN and $DNX)"; $PY -I read_lower.py $SCANG/scan 0.085 0.160; echo "(exit $?)"; } > $SCANG/read_lower.txt 2>&1 )
  cp $SCANG/read_lower.txt $K/read_lower_merged.txt
  NPTS=$(grep -h '^points ' $SCANG/read_lower.txt | head -1 | grep -o '^points [0-9]*' | grep -o '[0-9]*$')
  [ "${NPTS:-0}" = 6 ] || stop "READ FAILURE, not a result: read_lower.py read ${NPTS:-0} points of the 6 evaluations ($(grep -h '^points ' $SCANG/read_lower.txt | head -1))"
  nch=$(grep -c 'robust change (' $SCANG/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCANG/read_lower.txt | head -1 | grep -o '[0-9]*')
  say "merged reading ($NPTS points): $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint|^float64|not noise-robust' $SCANG/read_lower.txt | tr '\n' ' ' | cut -c1-1000)"
  bash $F/push_i1101.sh "I1101-macm3: R3 widened scan merged and read (6 points)" > /dev/null 2>&1
  bash $L/push87.sh "kc87_leg_lambda: D $DNG (I1101 R3 merged reading, 6 points)" > /dev/null 2>&1
  tell "macm3 #1101 R3: the merged reading of the six lambda (0.085 to 0.160, own steps, $NPTS points read): $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint|not noise-robust' $SCANG/read_lower.txt | tr '\n' ';' | cut -c1-1000) (raw kc87_leg_lambda/$DNG/)"
  if [ "$nch" = 0 ] && [ "$nrb" = 0 ]; then tell "macm3 #1101 R3: no robust change in 0.085 to 0.160 with all 6 points read: no secant; the lane ends and waits for your word"; exit 0; fi
  RL=$SCANG/read_lower.txt; SUMD=$SCANG
fi
[ "$nch" = 1 ] && [ "$nrb" = 1 ] || { tell "macm3 #1101 R3 STOP: the reading has $nrb robust changes (one wanted): no secant; reported"; exit 1; }
# 7. the secant refinement of the one robust change
BR=$(grep 'robust change (' $RL | sed -E 's/.*robust change \((-?[0-9.]+), (-?[0-9.]+)\).*/\1 \2/')
LO=${BR% *}; HI=${BR#* }
S_STATE=$SCAN/in/sol_${TAG}_$DT.npy; S_REC=$SCAN/in/$TAG.jsonl; SB=$(blob $S_STATE | cut -c1-8); TB=$(blob $S_REC | cut -c1-8)
mkdir -p $SEC; [ -e $SEC/secant.jsonl ] && stop "$SEC/secant.jsonl exists"
say "secant starts: d18_secant.py run $S_REC $S_STATE $D $LO $HI secant.jsonl --tol=5e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4"
echo "time_utc,pid,rss_kB,pcpu,avail_GiB" > $SEC/samples.csv
( cd $WTS && env PYTHONPATH=$SITE OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 $PY -u $IN/capped_run.py 18000 $PY -u $WTS/d18_secant.py run $S_REC $S_STATE $D $LO $HI $SEC/secant.jsonl --tol=5e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4 > $SEC/secant.log 2>&1; echo $? > $SEC/exit.txt ) &
sp=$!
( while kill -0 $sp 2>/dev/null; do for p in $(pgrep -f "d18_secant.py run.*I1101-macm3/r3/secant"); do echo "$(stamp),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(availgib)" >> $SEC/samples.csv; done; sleep 60; done ) &
wait $sp; se=$(cat $SEC/exit.txt)
say "secant exit $se"
[ "$se" = 0 ] || [ "$se" = 4 ] || stop "d18_secant.py exit $se (0 tol reached, 4 maxev or non-robust interior point; 2 refused, 3 pin or record system): see $SEC/secant.log"
$PY $F/summarize_point.py $SUMD $SEC > $K/point_summary.txt 2>&1
bash $F/push_i1101.sh "I1101-macm3: R3 scanned and its root refined (secant)" > /dev/null 2>&1
RT=$(grep -o 'det-linear root [0-9.-]*' $K/point_summary.txt | head -1 | awk '{print $3}')
CMPR=$(python3 -c "
r = float('$RT'); h = [('0.111 (kappa^4)', 0.111), ('0.120 (kappa^3)', 0.120), ('0.133 (kappa^2)', 0.133)]
print('root %.8f: minus 0.111 %+.5f, minus 0.120 %+.5f, minus 0.133 %+.5f; nearest %s' % (r, r - 0.111, r - 0.120, r - 0.133, min(h, key=lambda t: abs(r - t[1]))[0]))")
tell "macm3 #1101 R3 done: $CMPR; $(grep -E '^(scan:|secant: status|secant root)' $K/point_summary.txt | tr '\n' ';' | cut -c1-1200) (raw I1101-macm3/r3/ and kc87_leg_lambda/$DN/)"
exit 0
}
