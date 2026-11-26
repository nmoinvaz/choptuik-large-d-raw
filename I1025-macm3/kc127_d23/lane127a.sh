#!/bin/bash
# #1025 macm3 kc127_d23: k_c 127 at D 23.0 from my accepted k_c 119 state there (raw I1025-macm3/kc119_d23/in), the second D of k_c 127 for the threshold zero AND the second seed of the k_c 127 leg: ell_leap.py needs two states of one k_c, and the leg order (t5, hc 26 Nov ~15:23 UTC)
# names only the D 23.0625 state; winb's k_c 127 regrid at D 23.0 is pending (4 to 10 h on his side). Same steps as kc127_d23/ (source check kc119 accepts, controls 1 1, kc111 and kc127 refuse; ell_refine.py 631e5801 "l1kc119macm3d23 119 l1kc127macm3d23 127 1 23.0 2.0992182200
# --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma", 6 threads, nice 10, capped_run.py 28800 s; kc127 check on the result: exit 0, controls 1 1, kc119 refuses; the NEW scanner d18_secant.py scan (92b9bf53, eb1396ad) at lambda 0.03, 0.04, 0.05,
# 0.06 plus a repeat of 0.05 on 2 processes (kc87_leg_lambda/pointnew.sh, folder kc87_leg_lambda/23.0_kc127/), then d18_secant.py run (92b9bf53, --tol=1e-5 --maxev=10, one process). Stops (hc to t5): a source or result not accepted, an exception, no robust change or
# more than one, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane127a.sh [dry|check]
{
set -u
MODE=${1:-}
F=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc127_d23; IN=$F/in; OUT=$F/regrid; C=$F/checks
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
WT=$HOME/Source/choptuik-large-d-1025m2; WTM=$WT/solver/matter
WT5=$HOME/Source/choptuik-large-d-1025m; WTM5=$WT5/solver/matter
WTS=$HOME/Source/choptuik-large-d-1025s2/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python; RAWG=$HOME/Source/choptuik-large-d-raw-1076p
SRC=l1kc119macm3d23; TAG=l1kc127macm3d23; D=23.0; DT=D23.0000; SRCFILE=sol_${SRC}_D23.0000.npy; LAM0=2.0992182200; DN=23.0_kc127; SCAN=$L/$DN; SEC=$F/secant
HC=$(command -v hc); LOG=$F/exits_kc127a.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc127_d23: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; tell "macm3 #1025 kc127_d23 STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $OUT $C
export PYTHONDONTWRITEBYTECODE=1
say "start (mode ${MODE:-full}; load $(sysctl -n vm.loadavg), $(availgib) GiB available)"
# 1. pins
while read bb f; do case "$bb" in "#"*) continue;; esac
  p=$F/$f; [ -f $p ] && [ "$(blob $p | cut -c1-8)" = "$bb" ] || stop "$p missing or not blob $bb"; done < $F/in_blobs.txt
diff -u $IN/kc119_syscheck_1025.py $IN/kc127_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
[ "$(grep -c '^[-+][^-+]' $OUT/diff_rebuilt.txt)" = 8 ] && [ "$(grep -c '^-[^-].*119' $OUT/diff_rebuilt.txt)" = 4 ] && [ "$(grep -c '^+[^+].*127' $OUT/diff_rebuilt.txt)" = 4 ] || stop "the diff of the k_c 119 and k_c 127 checks is not a header comment line and three lines changed from 119 to 127"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree $WT not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] && [ "$(blob $WTM/ell_delta.py | cut -c1-8)" = fde699f5 ] || stop "ell_refine.py or ell_delta.py is not 631e5801 / fde699f5"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WT5 rev-parse --short=8 HEAD)" = 505d8399 ] && [ -z "$(git -C $WT5 status --short solver | grep -v 'solver/matter/data/')" ] || stop "the scan worktree $WT5 is not clean at 505d8399"
[ "$(git -C ${WTS%/solver/matter} rev-parse --short=8 HEAD)" = 92b9bf53 ] && [ "$(blob $WTS/d18_secant.py | cut -c1-8)" = eb1396ad ] || stop "the scanner worktree is not at 92b9bf53 with d18_secant.py eb1396ad"
for f in dss_ell ell_ddm ell_dd ddnp; do [ "$(blob $WTS/$f.py | cut -c1-8)" = "$(blob $WTM5/$f.py | cut -c1-8)" ] || stop "$f.py of the scanner worktree differs from the scan worktree's (505d8399)"; done
[ "$MODE" != dry ] && [ "$MODE" != check ] && { [ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"; [ -e $WTM/data/sol_${TAG}_$DT.npy ] && stop "the result state exists in $WTM/data"; }
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print('%.10f' % ell_delta.lam0_at($D, *ell_delta.lam0_table())[0])")
python3 -c "import sys; sys.exit(0 if abs(float('$L0') - float('$LAM0')) < 1e-10 else 1)" || stop "lambda_0($D) reads $L0, not $LAM0"
say "pins checked (in_blobs.txt; the diff of the k_c 119 and k_c 127 checks: a header comment line and 3 lines changed from 119 to 127), worktrees $WT 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801, ell_delta.py fde699f5), $WT5 505d8399 and the scanner worktree 92b9bf53 (d18_secant.py eb1396ad) clean; lambda_0($D) $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# 2. selftests
export D18_DIR=$IN OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
( cd $IN
  nice -n 10 $PY -I kc111_syscheck_1025.py --selftest > $C/selftest_kc111_syscheck.txt 2>&1; a0=$?
  nice -n 10 $PY -I kc119_syscheck_1025.py --selftest > $C/selftest_kc119_syscheck.txt 2>&1; a1=$?
  nice -n 10 $PY -I kc127_syscheck_1025.py --selftest > $C/selftest_kc127_syscheck.txt 2>&1; a2=$?
  $PY -W ignore read_lower.py selftest > $C/selftest_read_lower.txt 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $C/selftest_read_lower_shift.txt 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $C/selftest_read_lower_round2.txt 2>&1; r2=$?
  $PY repeat_check.py selftest > $C/selftest_repeat_check.txt 2>&1; r3=$?
  echo "$a0 $a1 $a2 $r0 $r1 $r2 $r3" > $C/selftest_exits.txt )
[ "$(cat $C/selftest_exits.txt)" = "0 0 0 0 1 1 0" ] || stop "the selftests did not behave ($(cat $C/selftest_exits.txt); wanted 0 0 0 0 1 1 0: kc111_syscheck, kc119_syscheck, kc127_syscheck, read_lower, mutate shift, mutate round2, repeat_check)"
say "selftests as wanted (0 0 0 0 1 1 0)"
# 2b. the new scanner (t5's order): selftest exit 0, --mutate=half|norobust|nosigncheck exit 1 each, logged
( cd $WTS && export RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
  nice -n 10 $PY d18_secant.py selftest > $C/newscan_selftest.txt 2>&1; n0=$?; nx="$n0"
  for m in half norobust nosigncheck; do nice -n 10 $PY d18_secant.py selftest --mutate=$m > $C/newscan_selftest_$m.txt 2>&1; nx="$nx $?"; done
  echo "$nx" > $C/newscan_exits.txt )
[ "$(cat $C/newscan_exits.txt)" = "0 1 1 1" ] || stop "the new scanner's selftest exits '$(cat $C/newscan_exits.txt)' (wanted '0 1 1 1': selftest, half, norobust, nosigncheck)"
say "new scanner d18_secant.py (blob $(blob $WTS/d18_secant.py | cut -c1-8), worktree 92b9bf53): selftest exit 0, --mutate=half exit 1, --mutate=norobust exit 1, --mutate=nosigncheck exit 1 (logged before the scan, as t5 ordered)"
# 3. the source: the k_c 111 check accepts it with controls 1 1; the k_c 103 and k_c 119 checks refuse it
STATE=$IN/$SRCFILE; REC=$IN/$SRC.jsonl
C119S="nice -n 10 $PY -I $IN/kc119_syscheck_1025.py $REC $STATE $D $WTM"
$C119S > $OUT/source_syscheck.txt 2>&1; s0=$?; $C119S --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?; $C119S --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc111_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc111check_refuses.txt 2>&1; s3=$?
nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc127check_refuses.txt 2>&1; s4=$?
say "source check (my k_c 119 state at D $D): kc119_syscheck exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc111_syscheck on the source exit $s3, kc127_syscheck on the source exit $s4 (1 wanted each): $(grep -E '^D ' $OUT/source_syscheck.txt | cut -c1-300)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] && [ $s4 = 1 ] || stop "the source check or a control did not read as written"
[ "$MODE" = dry ] && { say "dry run: pins, selftests and the source check passed; nothing started"; exit 0; }
[ "$MODE" = check ] && { say "check run: nothing regridded"; exit 0; }
# 4. wait for no other scan or regrid, then for memory
while pgrep -f 'd18_hybsign|ell_refine|d18_secant.py run' > /dev/null; do sleep 30; done
while python3 -c "import sys; sys.exit(0 if $(availgib) >= 8 else 1)"; [ $? != 0 ]; do sleep 60; done
# 5. the regrid (only the state is copied into the worktree's data, under the name ell_refine reads)
cp $STATE $WTM/data/sol_${SRC}_$DT.npy
[ "$(blob $WTM/data/sol_${SRC}_$DT.npy | cut -c1-8)" = 2771cf87 ] || stop "copied source state blob differs"
CMD="nice -n 10 $PY -u $IN/capped_run.py 28800 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_refine.py $SRC 119 $TAG 127 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
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
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap of 8 h)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_$DT.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $IN/ ; cp $WTM/data/sol_${TAG}_$DT.npy $IN/
C127="nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM"
$C127 > $OUT/syscheck.txt 2>&1; c0=$?; $C127 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?; $C127 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $IN/kc119_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM > $OUT/syscheck_kc119check_refuses.txt 2>&1; c3=$?
say "kc127 syscheck exit $c0 (0 wanted); controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each); kc119_syscheck on the k_c 127 result exit $c3 (1 wanted): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-300)"
[ $c0 = 0 ] && [ $c1 = 1 ] && [ $c2 = 1 ] && [ $c3 = 1 ] || stop "the regrid result is not accepted (syscheck $c0, controls $c1 $c2, kc119 check on the result $c3)"
echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
{ echo "$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8) sol_${TAG}_$DT.npy"; echo "$(blob $IN/$TAG.jsonl | cut -c1-8) $TAG.jsonl"; } > $F/in_blobs_regrid.txt
python3 - $IN/$TAG.jsonl $IN/$SRC.jsonl $D <<'PY' > $OUT/regrid_summary.txt
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip()][-1]; src = [json.loads(l) for l in open(sys.argv[2]) if l.strip() and json.loads(l)["D"] == float(sys.argv[3])][-1]
print("k_c 127 record: D %r |F| %.4e steps %d psi-constraint %.4e Delta %.12f (k_c 119 source: |F| %.4e steps %d constraint %.4e Delta %.12f); Delta shift %+.4e, steps ratio %.3f, constraint ratio %.3f" % (
    rec["D"], rec["F"], rec["steps"], rec["constraint"], rec["Delta"], src["F"], src["steps"], src["constraint"], src["Delta"], rec["Delta"] - src["Delta"], rec["steps"] / src["steps"], rec["constraint"] / src["constraint"]))
PY
RP=$(bash $F/push127a.sh "kc127_d23: k_c 127 D 23.0 regrid accepted (state, record, checks)" 2>&1 | tail -1); say "pushed regrid: $RP"
tell "macm3 #1025 kc127_d23: the k_c 127 D 23.0 regrid is ACCEPTED ($(cat $OUT/regrid_summary.txt)); regrid wall $(( $(date +%s) - t0 )) s; the scan ($(grep -c . $F/scan_plan.env) lines of plan, see scan_plan.env) starts now; raw $RP"
# 6. the scan folder (pins from the pushed commit), the lock, then point87.sh scan
RAWC=$(echo "$RP" | awk '{print $2}')
git -C $RAWG cat-file -e $RAWC:I1025-macm3/kc127_d23/in/$TAG.jsonl 2>/dev/null || stop "the pushed commit $RAWC does not hold the regrid record"
mkdir -p $SCAN
{ cat <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=sol_${TAG}_$DT.npy
STATEBLOB=$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8)
RECBLOB=$(blob $IN/$TAG.jsonl | cut -c1-8)
SRC=I1025-macm3/kc127_d23/in
PENV
  cat $F/scan_plan.env; } > $SCAN/point.env
bash $L/prepare87.sh $DN > $SCAN/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCAN/prepare.log)"
for f in sol_${TAG}_$DT.npy; do cp $SCAN/in/$f $WTM5/data/$f; done; cp $SCAN/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
echo "ACCEPTED $(stamp) UTC (the k_c 127 regrid check of the lane, $OUT/syscheck.txt; controls and the k_c 119 refusal in $OUT)" > $SCAN/VERDICT.txt
echo "$(stamp) UTC accept (lane127a.sh): kc127_syscheck_1025.py exit $c0 (0 wanted); controls exit $c1 $c2 (1 wanted); kc119_syscheck on the result exit $c3 (1 wanted): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN pins and verdict (kc127 regrid of D 23.0)" > /dev/null 2>&1
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "scan starts (pointnew.sh $DN scan: the new scanner d18_secant.py scan)"
bash $L/pointnew.sh $DN scan >> $SCAN/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "scan exit $sc"
[ -e $SCAN/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCAN/steps.txt)"
bash $L/push87.sh "kc87_leg_lambda: D $DN (k_c 127) scan done" > /dev/null 2>&1
nch=$(grep -c 'robust change (' $SCAN/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCAN/read_lower.txt | head -1 | grep -o '[0-9]*')
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint|^repeated|^float64' $SCAN/read_lower.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1025 kc127_d23: the k_c 127 D 23.0 scan is read: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint' $SCAN/read_lower.txt | tr '\n' ';' | cut -c1-900) (raw kc87_leg_lambda/$DN/)"
[ "$nch" = 1 ] && [ "$nrb" = 1 ] || { tell "macm3 #1025 kc127_d23: the scan reads $nrb robust changes (one wanted): no secant refinement; reported, the window is not widened without your word"; exit 0; }
# 7. the secant refinement of the one robust change
BR=$(grep 'robust change (' $SCAN/read_lower.txt | sed -E 's/.*robust change \((-?[0-9.]+), (-?[0-9.]+)\).*/\1 \2/')
LO=${BR% *}; HI=${BR#* }
S_STATE=$SCAN/in/sol_${TAG}_$DT.npy; S_REC=$SCAN/in/$TAG.jsonl; SB=$(blob $S_STATE | cut -c1-8); TB=$(blob $S_REC | cut -c1-8)
mkdir -p $SEC; [ -e $SEC/secant.jsonl ] && stop "$SEC/secant.jsonl exists"
say "secant starts: d18_secant.py run $S_REC $S_STATE $D $LO $HI secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB"
echo "time_utc,pid,rss_kB,pcpu,avail_GiB" > $SEC/samples.csv
( cd $WTS && env RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 $PY -u $IN/capped_run.py 18000 $PY -u $WTS/d18_secant.py run $S_REC $S_STATE $D $LO $HI $SEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB > $SEC/secant.log 2>&1; echo $? > $SEC/exit.txt ) &
sp=$!
( while kill -0 $sp 2>/dev/null; do for p in $(pgrep -f "d18_secant.py run.*kc127_d23/secant"); do echo "$(stamp),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(availgib)" >> $SEC/samples.csv; done; sleep 60; done ) &
wait $sp; se=$(cat $SEC/exit.txt)
say "secant exit $se"
[ "$se" = 0 ] || [ "$se" = 4 ] || stop "d18_secant.py exit $se (0 tol reached, 4 maxev or non-robust interior point; 2 refused, 3 pin or record system): see $SEC/secant.log"
$PY $F/summarize_point.py $SCAN $SEC > $F/point_summary.txt 2>&1
bash $F/push127a.sh "kc127_d23: D 23.0 scanned and its root refined (secant)" > /dev/null 2>&1
tell "macm3 #1025 kc127_d23 done: $(grep -E '^(scan:|secant: status|secant root)' $F/point_summary.txt | tr '\n' ';' | cut -c1-1400) (raw kc127_d23/ and kc87_leg_lambda/$DN/)"
exit 0
}
