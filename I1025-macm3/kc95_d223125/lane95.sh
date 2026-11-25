#!/bin/bash
# #1025 macm3 kc95_d223125 (t5's order, hc 25 Nov ~08:1x UTC, after my D 22.1875 mid scan): k_c 95 at D 22.3125 from my part b2 k_c 87 state, by dh610's recipe (raw I1025-dh610/kc95_d22375/lane_kc95.sh, README):
# source check (kc87 accepts, controls exit 1 1, kc95 check refuses), regrid with ell_refine.py (worktree 48c36355, blob 631e5801; "--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma", lambda_0(22.3125) = 2.1016708417 from
# ell_delta.lam0_at, 6 threads, nice 10, cap 21600 s), accepted only by kc95_syscheck_1025.py (selftest, both controls exit 1, the k_c 87 check refusing the result); then a WIDE hybrid sign scan, lambda -0.10 to 0.50 by 0.04 plus a repeat of 0.14,
# 17 evaluations on 4 processes of 1 thread at nice 15 (kc87_leg_lambda/point87.sh scan machinery, folder 22.3125_kc95), read by read_lower.py and wide_read.py (every robust change by position and printed orientation).
# The regrid waits for the D 22.15625 high scan (22.15625_high/SCAN_DONE.txt) and for no d18_hybsign process; it waits for memory (8 GiB available), never stops for it (alert only).
# Stops (hc to t5): a pin, selftest or control that does not read as written, the source not accepted, the regrid not accepted or an exception or the cap, any scan failure. usage: bash lane95.sh [dry|check]
{
set -u
MODE=${1:-}
F=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc95_d223125; IN=$F/in; OUT=$F/regrid; C=$F/checks
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda; L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
WT=$HOME/Source/choptuik-large-d-1025m2; WTM=$WT/solver/matter
WT5=$HOME/Source/choptuik-large-d-1025m; WTM5=$WT5/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python; RAWG=$HOME/Source/choptuik-large-d-raw-1076p
SRC=l1kc87Lmacm3b2; TAG=l1kc95macm3d223125; D=22.3125; LAM0=2.1016708417; DN=22.3125_kc95; SCAN=$L/$DN
HC=$(command -v hc); LOG=$F/exits_kc95.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc95_d223125: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; tell "macm3 #1025 kc95_d223125 STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $OUT $C
export PYTHONDONTWRITEBYTECODE=1
say "start (mode ${MODE:-full}; load $(sysctl -n vm.loadavg), $(availgib) GiB available)"
# 1. pins
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f | cut -c1-8)" = "$bb" ] || stop "$IN/$f missing or not blob $bb"; done < $F/in_blobs.txt
diff -u $IN/kc87_syscheck_1025.py $IN/kc95_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
tail -n +3 $F/kc95_syscheck_1025.diff | cmp -s - $OUT/diff_rebuilt.txt || stop "kc95_syscheck_1025.diff is not the diff of the two checks"
[ "$(grep -c '^[-+][^-+]' $OUT/diff_rebuilt.txt)" = 6 ] || stop "the diff of the two checks is not three changed lines"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree $WT not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WT5 rev-parse --short=8 HEAD)" = 505d8399 ] && [ -z "$(git -C $WT5 status --short solver | grep -v 'solver/matter/data/')" ] || stop "the scan worktree $WT5 is not clean at 505d8399"
[ "$MODE" != dry ] && [ "$MODE" != check ] && { [ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"; [ -e $WTM/data/sol_${TAG}_D22.3125.npy ] && stop "the result state exists in $WTM/data"; }
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$L0" = "$LAM0" ] || stop "lambda_0($D) reads $L0, not $LAM0"
say "pins checked (in_blobs.txt, diff of the two checks rebuilt: 3 changed lines), worktrees $WT 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801) and $WT5 505d8399 clean; lambda_0($D) $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# 2. selftests
export D18_DIR=$IN OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
( cd $IN
  nice -n 10 $PY -I kc87_syscheck_1025.py --selftest > $C/selftest_kc87_syscheck.txt 2>&1; a0=$?
  nice -n 10 $PY -I kc95_syscheck_1025.py --selftest > $C/selftest_kc95_syscheck.txt 2>&1; a1=$?
  $PY -W ignore read_lower.py selftest > $C/selftest_read_lower.txt 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $C/selftest_read_lower_shift.txt 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $C/selftest_read_lower_round2.txt 2>&1; r2=$?
  $PY repeat_check.py selftest > $C/selftest_repeat_check.txt 2>&1; r3=$?
  $PY -I wide_read.py selftest > $C/selftest_wide_read.txt 2>&1; w0=$?
  $PY -I wide_read.py selftest --mutate > $C/selftest_wide_read_mutate.txt 2>&1; w1=$?
  ( cd $F && $PY -I in/planted_wide.py in > $C/selftest_planted_wide.txt 2>&1 ); p0=$?
  ( cd $F && $PY -I in/planted_wide.py --mutate in > $C/selftest_planted_wide_mutate.txt 2>&1 ); p1=$?
  echo "$a0 $a1 $r0 $r1 $r2 $r3 $w0 $w1 $p0 $p1" > $C/selftest_exits.txt )
[ "$(cat $C/selftest_exits.txt)" = "0 0 0 1 1 0 0 1 0 1" ] || stop "the selftests did not behave ($(cat $C/selftest_exits.txt); wanted 0 0 0 1 1 0 0 1 0 1: kc87_syscheck, kc95_syscheck, read_lower, mutate shift, mutate round2, repeat_check, wide_read, mutate, planted_wide, mutate)"
say "selftests as wanted (0 0 0 1 1 0 0 1 0 1)"
# 3. the source: the kc87 check accepts it with both controls exit 1, and the kc95 check refuses it
STATE=$IN/sol_${SRC}_D22.312500.npy; REC=$IN/$SRC.jsonl
C87="nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $REC $STATE $D $WTM"
$C87 > $OUT/source_syscheck.txt 2>&1; s0=$?; $C87 --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?; $C87 --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc95check_refuses.txt 2>&1; s3=$?
say "source check (my k_c 87 D 22.3125 state): kc87_syscheck exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc95_syscheck on the source exit $s3 (1 wanted): $(grep -E '^D ' $OUT/source_syscheck.txt | cut -c1-300)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "the source check or a control did not read as written"
[ "$MODE" = dry ] && { say "dry run: pins, selftests and the source check passed; nothing started"; exit 0; }
[ "$MODE" = check ] && { say "check run: nothing regridded"; exit 0; }
# 4. wait for the D 22.15625 high scan (and any d18_hybsign process), then for memory
while [ ! -e $L/22.15625_high/SCAN_DONE.txt ] || pgrep -f d18_hybsign > /dev/null; do sleep 30; done
say "the D 22.15625 high scan is done (SCAN_DONE.txt) and no d18_hybsign runs"
while python3 -c "import sys; sys.exit(0 if $(availgib) >= 8 else 1)"; [ $? != 0 ]; do sleep 60; done
# 5. the regrid
cp $STATE $WTM/data/sol_${SRC}_D22.3125.npy
[ "$(blob $WTM/data/sol_${SRC}_D22.3125.npy | cut -c1-8)" = 96b8990e ] || stop "copied source state blob differs"
CMD="nice -n 10 $PY -u $L2/in/capped_run.py 21600 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_refine.py $SRC 87 $TAG 95 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM): $CMD" > $OUT/regrid.log
say "regrid starts: $CMD"
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
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap of 6 h)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D22.3125.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $F/in/ ; cp $WTM/data/sol_${TAG}_D22.3125.npy $F/in/
C95="nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_D22.3125.npy $D $WTM"
$C95 > $OUT/syscheck.txt 2>&1; c0=$?; $C95 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?; $C95 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_D22.3125.npy $D $WTM > $OUT/syscheck_kc87check_refuses.txt 2>&1; c3=$?
say "kc95 syscheck exit $c0 (0 wanted); controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each); kc87_syscheck on the k_c 95 result exit $c3 (1 wanted): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-300)"
[ $c0 = 0 ] && [ $c1 = 1 ] && [ $c2 = 1 ] && [ $c3 = 1 ] || stop "the regrid result is not accepted (syscheck $c0, controls $c1 $c2, kc87 check on the result $c3)"
echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
{ echo "$(blob $IN/sol_${TAG}_D22.3125.npy | cut -c1-8) sol_${TAG}_D22.3125.npy"; echo "$(blob $IN/$TAG.jsonl | cut -c1-8) $TAG.jsonl"; } > $F/in_blobs_regrid.txt
python3 - $IN/$TAG.jsonl $IN/$SRC.jsonl $D $OUT/regrid.log <<'PY' > $OUT/regrid_summary.txt
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip()][-1]; src = [json.loads(l) for l in open(sys.argv[2]) if l.strip() and json.loads(l)["D"] == float(sys.argv[3])][-1]
print("k_c 95 record: D %r |F| %.4e steps %d psi-constraint %.4e Delta %.12f (k_c 87 source: |F| %.4e steps %d constraint %.4e Delta %.12f); Delta shift %+.4e, steps ratio %.3f" % (
    rec["D"], rec["F"], rec["steps"], rec["constraint"], rec["Delta"], src["F"], src["steps"], src["constraint"], src["Delta"], rec["Delta"] - src["Delta"], rec["steps"] / src["steps"]))
PY
RP=$(bash $F/push95.sh "kc95_d223125: k_c 95 D 22.3125 regrid accepted (state, record, checks)" 2>&1 | tail -1); say "pushed regrid: $RP"
tell "macm3 #1025 kc95_d223125: the k_c 95 D 22.3125 regrid is ACCEPTED ($(cat $OUT/regrid_summary.txt)); regrid wall $(( $(date +%s) - t0 )) s; the wide scan (lambda -0.10 to 0.50 by 0.04 + repeat of 0.14, 4 procs) starts now; raw $RP"
# 6. the scan folder (pins from the pushed commit), the lock, then point87.sh scan
RAWC=$(echo "$RP" | awk '{print $2}')
git -C $RAWG cat-file -e $RAWC:I1025-macm3/kc95_d223125/in/$TAG.jsonl 2>/dev/null || stop "the pushed commit $RAWC does not hold the regrid record"
mkdir -p $SCAN
cat > $SCAN/point.env <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=sol_${TAG}_D22.3125.npy
STATEBLOB=$(blob $IN/sol_${TAG}_D22.3125.npy | cut -c1-8)
RECBLOB=$(blob $IN/$TAG.jsonl | cut -c1-8)
# t5's order (hc 25 Nov): the wide scan of macm3's k_c 95 D 22.3125 (regrid of my part b2 k_c 87 state), lambda -0.10 to 0.50 by 0.04 plus a repeat of 0.14, 4 processes at nice 15, beside part c's leap
NP=4; GATE=10; NICE=15
SRC=I1025-macm3/kc95_d223125/in
LAMP=("-0.10" "-0.06" "-0.02" "0.02" "0.06" "0.10" "0.14" "0.18" "0.22" "0.26" "0.30" "0.34" "0.38" "0.42" "0.46" "0.50" "0.14")
WIN="-0.10 0.50"; REP=0.14
PENV
bash $L/prepare87.sh $DN > $SCAN/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCAN/prepare.log)"
for f in sol_${TAG}_D22.3125.npy; do cp $SCAN/in/$f $WTM5/data/$f; done; cp $SCAN/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
echo "ACCEPTED $(stamp) UTC (the k_c 95 regrid check of the lane, $OUT/syscheck.txt; controls and the k_c 87 refusal in $OUT)" > $SCAN/VERDICT.txt
echo "$(stamp) UTC accept (lane95.sh): kc95_syscheck_1025.py exit $c0 (0 wanted); controls exit $c1 $c2 (1 wanted); kc87_syscheck on the result exit $c3 (1 wanted): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt
echo "$(stamp) UTC verdict: $(cat $SCAN/VERDICT.txt | cut -c1-30)" >> $SCAN/steps.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN pins and verdict (kc95 regrid of D 22.3125)" > /dev/null 2>&1
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "wide scan starts (point87.sh $DN scan)"
bash $L/point87.sh $DN scan >> $SCAN/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "scan exit $sc"
[ -e $SCAN/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCAN/steps.txt)"
( cd $IN && D18_DIR=$IN $PY -I wide_read.py $SCAN/read_lower.txt > $SCAN/wide_read.txt 2>&1 )
cp $SCAN/wide_read.txt $F/wide_read.txt; cp $SCAN/read_lower.txt $F/read_lower.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN (k_c 95) wide scan done" > /dev/null 2>&1; bash $F/push95.sh "kc95_d223125: wide scan reading" > /dev/null 2>&1
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(' $SCAN/wide_read.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1025 kc95_d223125: the k_c 95 D 22.3125 WIDE SCAN is read: $(grep -E '^hybrid signs|^robust changes|change ' $SCAN/wide_read.txt | tr '\n' ';' | cut -c1-900) (full table follows in my report; raw kc87_leg_lambda/$DN/ and kc95_d223125/)"
exit 0
}
