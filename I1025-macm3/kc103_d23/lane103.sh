#!/bin/bash
# #1025 macm3 kc103_d23 (t5's order, hc 25 Nov ~21:05 UTC): k_c 103 at D 23.0 from win2's accepted k_c 95 state (raw I1025-win2/kc95_d23: state blob 096f1cc0, record blob e3fff23f), by the regrid recipe of dh170/dh610/win2 (raw
# I1025-dh170/kc103_d21125/run_regrid.sh): source check (kc95 accepts, controls exit 1 1, the k_c 87 and k_c 103 checks refuse), regrid with ell_refine.py (worktree 48c36355, blob 631e5801:
# "--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma", lambda_0(23.0) = 2.0992182200 from ell_delta.lam0_at, 6 threads, nice 10, cap 21600 s), accepted only by kc103_syscheck_1025.py (3ab58d16: selftest, both controls
# exit 1, the k_c 95 check refusing the result); then a hybrid sign scan, lambda -0.06 to 0.06 by 0.01 plus a repeat of 0.00 (14 evaluations, 4 processes of 1 thread at nice 15, kc87_leg_lambda/point87.sh scan machinery, folder 23.0_kc103),
# read by read_lower.py and repeat_check.py. Memory: waits for 8 GiB available at the start, never stops for it (alert only).
# Stops (hc to t5): a pin, selftest or control that does not read as written, the source not accepted, the regrid not accepted or an exception or the cap, any scan failure. usage: bash lane103.sh [dry|check]
{
set -u
MODE=${1:-}
F=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc103_d23; IN=$F/in; OUT=$F/regrid; C=$F/checks
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
WT=$HOME/Source/choptuik-large-d-1025m2; WTM=$WT/solver/matter
WT5=$HOME/Source/choptuik-large-d-1025m; WTM5=$WT5/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python; RAWG=$HOME/Source/choptuik-large-d-raw-1076p
SRC=l1kc95win2d23; TAG=l1kc103macm3d23; D=23.0; DT=D23.0000; LAM0=2.0992182200; DN=23.0_kc103; SCAN=$L/$DN
HC=$(command -v hc); LOG=$F/exits_kc103.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc103_d23: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; tell "macm3 #1025 kc103_d23 STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $OUT $C
export PYTHONDONTWRITEBYTECODE=1
say "start (mode ${MODE:-full}; load $(sysctl -n vm.loadavg), $(availgib) GiB available)"
# 1. pins
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f | cut -c1-8)" = "$bb" ] || stop "$IN/$f missing or not blob $bb"; done < $F/in_blobs.txt
diff -u $IN/kc95_syscheck_1025.py $IN/kc103_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
tail -n +3 $IN/kc103_syscheck_1025.diff | cmp -s - $OUT/diff_rebuilt.txt || stop "dh610's kc103_syscheck_1025.diff is not the diff of the k_c 95 and k_c 103 checks"
[ "$(grep -c '^[-+][^-+]' $OUT/diff_rebuilt.txt)" = 6 ] || stop "the diff of the two checks is not three changed lines"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree $WT not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WT5 rev-parse --short=8 HEAD)" = 505d8399 ] && [ -z "$(git -C $WT5 status --short solver | grep -v 'solver/matter/data/')" ] || stop "the scan worktree $WT5 is not clean at 505d8399"
[ "$MODE" != dry ] && [ "$MODE" != check ] && { [ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"; [ -e $WTM/data/sol_${TAG}_$DT.npy ] && stop "the result state exists in $WTM/data"; }
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$L0" = "$LAM0" ] || stop "lambda_0($D) reads $L0, not $LAM0"
say "pins checked (in_blobs.txt; the diff of the k_c 95 and k_c 103 checks rebuilt: 3 changed lines, equal to dh610's), worktrees $WT 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801) and $WT5 505d8399 clean; lambda_0($D) $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# 2. selftests
export D18_DIR=$IN OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
( cd $IN
  nice -n 10 $PY -I kc87_syscheck_1025.py --selftest > $C/selftest_kc87_syscheck.txt 2>&1; a0=$?
  nice -n 10 $PY -I kc95_syscheck_1025.py --selftest > $C/selftest_kc95_syscheck.txt 2>&1; a1=$?
  nice -n 10 $PY -I kc103_syscheck_1025.py --selftest > $C/selftest_kc103_syscheck.txt 2>&1; a2=$?
  $PY -W ignore read_lower.py selftest > $C/selftest_read_lower.txt 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $C/selftest_read_lower_shift.txt 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $C/selftest_read_lower_round2.txt 2>&1; r2=$?
  $PY repeat_check.py selftest > $C/selftest_repeat_check.txt 2>&1; r3=$?
  echo "$a0 $a1 $a2 $r0 $r1 $r2 $r3" > $C/selftest_exits.txt )
[ "$(cat $C/selftest_exits.txt)" = "0 0 0 0 1 1 0" ] || stop "the selftests did not behave ($(cat $C/selftest_exits.txt); wanted 0 0 0 0 1 1 0: kc87_syscheck, kc95_syscheck, kc103_syscheck, read_lower, mutate shift, mutate round2, repeat_check)"
say "selftests as wanted (0 0 0 0 1 1 0)"
# 3. the source: the kc95 check accepts it with both controls exit 1; the kc87 and kc103 checks refuse it
STATE=$IN/sol_${SRC}_$DT.npy; REC=$IN/$SRC.jsonl
C95="nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $REC $STATE $D $WTM"
$C95 > $OUT/source_syscheck.txt 2>&1; s0=$?; $C95 --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?; $C95 --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc87check_refuses.txt 2>&1; s3=$?
nice -n 10 $PY -I $IN/kc103_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc103check_refuses.txt 2>&1; s4=$?
say "source check (win2's k_c 95 D 23.0 state): kc95_syscheck exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc87_syscheck on the source exit $s3, kc103_syscheck on the source exit $s4 (1 wanted each): $(grep -E '^D ' $OUT/source_syscheck.txt | cut -c1-300)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] && [ $s4 = 1 ] || stop "the source check or a control did not read as written"
[ "$MODE" = dry ] && { say "dry run: pins, selftests and the source check passed; nothing started"; exit 0; }
[ "$MODE" = check ] && { say "check run: nothing regridded"; exit 0; }
# 4. wait for no other scan or regrid, then for memory
while pgrep -f 'd18_hybsign|ell_refine' > /dev/null; do sleep 30; done
while python3 -c "import sys; sys.exit(0 if $(availgib) >= 8 else 1)"; [ $? != 0 ]; do sleep 60; done
# 5. the regrid (only the state is copied into the worktree's data, as in the earlier regrids)
cp $STATE $WTM/data/sol_${SRC}_$DT.npy
[ "$(blob $WTM/data/sol_${SRC}_$DT.npy | cut -c1-8)" = 096f1cc0 ] || stop "copied source state blob differs"
CMD="nice -n 10 $PY -u $IN/capped_run.py 21600 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_refine.py $SRC 95 $TAG 103 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
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
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_$DT.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $IN/ ; cp $WTM/data/sol_${TAG}_$DT.npy $IN/
C103="nice -n 10 $PY -I $IN/kc103_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM"
$C103 > $OUT/syscheck.txt 2>&1; c0=$?; $C103 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?; $C103 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM > $OUT/syscheck_kc95check_refuses.txt 2>&1; c3=$?
say "kc103 syscheck exit $c0 (0 wanted); controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each); kc95_syscheck on the k_c 103 result exit $c3 (1 wanted): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-300)"
[ $c0 = 0 ] && [ $c1 = 1 ] && [ $c2 = 1 ] && [ $c3 = 1 ] || stop "the regrid result is not accepted (syscheck $c0, controls $c1 $c2, kc95 check on the result $c3)"
echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
{ echo "$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8) sol_${TAG}_$DT.npy"; echo "$(blob $IN/$TAG.jsonl | cut -c1-8) $TAG.jsonl"; } > $F/in_blobs_regrid.txt
python3 - $IN/$TAG.jsonl $IN/$SRC.jsonl $D <<'PY' > $OUT/regrid_summary.txt
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip()][-1]; src = [json.loads(l) for l in open(sys.argv[2]) if l.strip() and json.loads(l)["D"] == float(sys.argv[3])][-1]
print("k_c 103 record: D %r |F| %.4e steps %d psi-constraint %.4e Delta %.12f (k_c 95 source: |F| %.4e steps %d constraint %.4e Delta %.12f); Delta shift %+.4e, steps ratio %.3f" % (
    rec["D"], rec["F"], rec["steps"], rec["constraint"], rec["Delta"], src["F"], src["steps"], src["constraint"], src["Delta"], rec["Delta"] - src["Delta"], rec["steps"] / src["steps"]))
PY
RP=$(bash $F/push103.sh "kc103_d23: k_c 103 D 23.0 regrid accepted (state, record, checks)" 2>&1 | tail -1); say "pushed regrid: $RP"
tell "macm3 #1025 kc103_d23: the k_c 103 D 23.0 regrid is ACCEPTED ($(cat $OUT/regrid_summary.txt)); regrid wall $(( $(date +%s) - t0 )) s; the scan (lambda -0.06 to 0.06 by 0.01 + repeat of 0.00, 4 procs) starts now; raw $RP"
# 6. the scan folder (pins from the pushed commit), the lock, then point87.sh scan
RAWC=$(echo "$RP" | awk '{print $2}')
git -C $RAWG cat-file -e $RAWC:I1025-macm3/kc103_d23/in/$TAG.jsonl 2>/dev/null || stop "the pushed commit $RAWC does not hold the regrid record"
mkdir -p $SCAN
cat > $SCAN/point.env <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=sol_${TAG}_$DT.npy
STATEBLOB=$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8)
RECBLOB=$(blob $IN/$TAG.jsonl | cut -c1-8)
# t5's order (hc 25 Nov): the scan of macm3's k_c 103 D 23.0 (regrid of win2's k_c 95 state), lambda -0.06 to 0.06 by 0.01 plus a repeat of 0.00, 4 processes at nice 15
NP=4; GATE=10; NICE=15
SRC=I1025-macm3/kc103_d23/in
LAMP=("0.00" "0.00" "-0.06" "-0.05" "-0.04" "-0.03" "-0.02" "-0.01" "0.01" "0.02" "0.03" "0.04" "0.05" "0.06")
WIN="-0.06 0.06"; REP=0.00
PENV
bash $L/prepare87.sh $DN > $SCAN/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCAN/prepare.log)"
for f in sol_${TAG}_$DT.npy; do cp $SCAN/in/$f $WTM5/data/$f; done; cp $SCAN/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
echo "ACCEPTED $(stamp) UTC (the k_c 103 regrid check of the lane, $OUT/syscheck.txt; controls and the k_c 95 refusal in $OUT)" > $SCAN/VERDICT.txt
echo "$(stamp) UTC accept (lane103.sh): kc103_syscheck_1025.py exit $c0 (0 wanted); controls exit $c1 $c2 (1 wanted); kc95_syscheck on the result exit $c3 (1 wanted): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt
echo "$(stamp) UTC verdict: $(cat $SCAN/VERDICT.txt | cut -c1-30)" >> $SCAN/steps.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN pins and verdict (kc103 regrid of D 23.0)" > /dev/null 2>&1
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "scan starts (point87.sh $DN scan)"
bash $L/point87.sh $DN scan >> $SCAN/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "scan exit $sc"
[ -e $SCAN/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCAN/steps.txt)"
cp $SCAN/read_lower.txt $F/read_lower.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN (k_c 103) scan done" > /dev/null 2>&1; bash $F/push103.sh "kc103_d23: scan reading" > /dev/null 2>&1
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(' $SCAN/read_lower.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1025 kc103_d23: the k_c 103 D 23.0 scan is read: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint' $SCAN/read_lower.txt | tr '\n' ';' | cut -c1-900) (raw kc87_leg_lambda/$DN/ and kc103_d23/)"
exit 0
}
