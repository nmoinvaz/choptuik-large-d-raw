#!/bin/bash
# #1101 dh170, R3 (t5's order of 28 Nov, comment 7231154979): R3 is R1's state re-solved at kappa 0.25 on mm5 (raw I1101-mm5/: sol_l1kc127k025mm5_D23.0000.npy, l1kc127k025mm5.jsonl).
# Waits for both files on the raw repository's main (a fetch every 5 min in the push worktree, which is only fetched here), checks that the two blobs hold for 2 min, copies them to in/,
# pins their blobs (pins_r3.txt), checks the re-solve's bars on the record (|F| <= 5e-10, steps 11700 +- 2%, kappa 0.25, kc 127, D 23), then d18_secant.py scan on the Rust block 12 at
# lambda 0.115, 0.125, 0.135, 0.145 (one process each, 1 thread, nice 10; at most 4 scanner processes at once on the machine, scan_admit.sh), widening to 0.105 and 0.155 if no robust
# change (nothing further), then d18_secant.py run at tol 5e-5 on the first robust change (--ends = the scan's records), then results_r3.py read (the root against 0.1272 +- 2e-3).
# Priority (t5): while this driver starts its scan processes it holds /tmp/dh170_prio_r3, and run_scan1104.sh waits for it to go before starting any of its own.
# usage: run_scan_r3.sh        Stops at the first failure (STOP_r3.txt); DONE_r3.txt when it ends. Steps and exits in steps.txt, tag [r3].
# Environment overrides (OUT WTM SITE PY RAWC REMOTE DRY) are only for the dry-run test with a fake scanner (selftests/dryrun_r3.sh); DRY skips the pins of the real worktree.
{
: "${OUT:=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170}"
: "${WTM:=/home/nathan/Source/choptuik-large-d-1102/solver/matter}"
: "${SITE:=/home/nathan/Source/ellrs-site-1102}"
: "${PY:=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python}"
: "${RAWC:=/home/nathan/Source/choptuik-large-d-raw-push}"
: "${REMOTE:=origin/main}"
: "${DRY:=}"
TAG=r3; D=23.0; NI=10; DS=D23.0
SN=sol_l1kc127k025mm5_D23.0000.npy; RN=l1kc127k025mm5.jsonl
RESB=50c83985          # results_r3.py blob (set when the driver is pinned)
LIBB=e61f8891          # scan_admit.sh blob
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
PRIO=/tmp/dh170_prio_r3   # exists while R3's scan processes are being started: #1104's scan driver waits for it to go (t5: R3's scan goes first)
stop() { rm -f $PRIO; step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
if [ -z "$DRY" ]; then
  [ "$(git -C $WTM rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ -z "$(git -C $WTM status --short . | head -1)" ] || stop "the scanner worktree is not d4b6b6ce or not clean"
  [ "$(blob $WTM/d18_secant.py)" = 9706e506 ] && [ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "d18_secant.py is not 9706e506 or ell_b12rs.py not a1fff74f"
  [ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] || stop "read_lower.py or its change finder is not the pinned blob"
  [ "$(blob results_r3.py)" = "$RESB" ] && [ "$(blob scan_admit.sh)" = "$LIBB" ] || stop "results_r3.py is not $RESB or scan_admit.sh not $LIBB"
fi
for f in scan_r3 in/$SN in/$RN; do [ -e $f ] && stop "$f exists: not overwriting"; done
. $OUT/scan_admit.sh
step "static pins ok (worktree d4b6b6ce, d18_secant.py 9706e506, ell_b12rs.py a1fff74f, read_lower.py 89309d3c, d185_scan_read.py 7c9d400f, results_r3.py $RESB, scan_admit.sh $LIBB); waiting for $SN and $RN in $RAWC $REMOTE I1101-mm5"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
mkdir -p selftests
e=""; for m in "" tol pred last sign; do
  if [ -z "$m" ]; then $PY -I results_r3.py selftest > selftests/selftest_results_r3.txt 2>&1; else $PY -I results_r3.py selftest --mutate=$m > selftests/selftest_results_r3_$m.txt 2>&1; fi; e="$e $?"
done
step "results_r3.py selftest exits (plain, tol, pred, last, sign):$e (0 1 1 1 1 wanted)"
[ "$e" = " 0 1 1 1 1" ] || stop "a results_r3.py selftest or mutation did not read as written"
if [ -z "$DRY" ]; then
  cd $WTM
  nice -n $NI $PY -I d18_secant.py selftest > $OUT/selftests/selftest_secant_r3.txt 2>&1; s0=$?
  nice -n $NI $PY -I d18_secant.py selftest --mutate=half > $OUT/selftests/selftest_secant_r3_half.txt 2>&1; s1=$?
  nice -n $NI $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftests/selftest_secant_r3_norobust.txt 2>&1; s2=$?
  nice -n $NI $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftests/selftest_secant_r3_nosigncheck.txt 2>&1; s3=$?
  cd $OUT
  step "d18_secant.py selftest exit $s0 (0 wanted); mutations half exit $s1, norobust exit $s2, nosigncheck exit $s3 (1 wanted each)"
  [ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "a d18_secant.py selftest or mutation did not read as written"
fi
# ---- wait for the two files
found() {   # found: both files exactly once under I1101-mm5 -> sets SP RP, prints their git blob ids
  local files; files=$(git -C $RAWC ls-tree -r --name-only $REMOTE -- I1101-mm5 2>/dev/null)
  SP=$(echo "$files" | grep -E "(^|/)$SN\$"); RP=$(echo "$files" | grep -E "(^|/)$RN\$")
  [ "$(echo "$SP" | grep -c .)" = 1 ] && [ "$(echo "$RP" | grep -c .)" = 1 ] || return 1
  echo "$(git -C $RAWC rev-parse $REMOTE:$SP) $(git -C $RAWC rev-parse $REMOTE:$RP)"
}
fetch() { [ -n "$DRY" ] || git -C $RAWC fetch -q origin 2>> $OUT/fetch_r3.err; }
POLL=${POLL:-300}
while true; do
  fetch
  b1=$(found) && { sleep ${HOLD:-120}; fetch; b2=$(found); [ "$b1" = "$b2" ] && break; step "the blobs changed within ${HOLD:-120} s ($b1 -> $b2): waiting again"; }
  sleep $POLL
done
found > /dev/null || stop "the files vanished from $REMOTE"      # sets SP and RP in this shell (the loop ran found in command substitutions)
RAWCOMMIT=$(git -C $RAWC rev-parse --short=9 $REMOTE)
mkdir -p in
git -C $RAWC show $REMOTE:$SP > in/$SN && git -C $RAWC show $REMOTE:$RP > in/$RN || stop "git show of the two files failed"
SB=$(blob in/$SN); RB=$(blob in/$RN)
[ "$SB" = "$(echo $b1 | cut -c1-8)" ] && [ "$RB" = "$(echo $b1 | cut -d' ' -f2 | cut -c1-8)" ] || stop "the copies' blobs ($SB, $RB) differ from git's ($b1)"
echo "R3 state $SP blob $SB; record $RP blob $RB; raw main $RAWCOMMIT; landed $(stamp) UTC" > pins_r3.txt
step "R3 landed: $SP blob $SB, $RP blob $RB (raw main $RAWCOMMIT), unchanged for ${HOLD:-120} s; copied to in/; pins_r3.txt"
rec=$(tail -1 in/$RN)
echo "$rec" | jq -c '{F,steps,kappa,kc,D,u0,l,src,seconds}' >> steps.txt
[ "$(echo "$rec" | jq -r '(.F|fabs <= 5e-10) and (.steps >= 11700*0.98) and (.steps <= 11700*1.02) and (.kappa == 0.25) and (.kc == 127) and (.D == 23) and (.l == 1)')" = true ] || stop "the record does not meet the bars (|F| <= 5e-10, steps 11700 +- 2%, kappa 0.25, kc 127, D 23, l 1): $(echo "$rec" | jq -c '{F,steps,kappa,kc,D,l}')"
step "the re-solve's bars pass: |F| $(echo "$rec" | jq -r .F), steps $(echo "$rec" | jq -r .steps) (11466 to 11934)"
# ---- scans
one_scan() {   # one_scan LAM I
  ( cd $WTM && PYTHONPATH=$SITE nice -n $NI /usr/bin/time -v $PY -u $WTM/d18_secant.py scan $OUT/in/$RN $OUT/in/$SN $D $1 $OUT/scan_$TAG/scan_${DS}_p$2.jsonl --b12=rust --b12_threads=1 --pin=$SB,$RB > $OUT/scan_${TAG}_p$2.raw 2>&1
    rc=$?; echo "$(stamp) UTC [$TAG] lambda $1 exit $rc" >> $OUT/steps.txt )
}
scan() {   # scan LAMS I0: one process per lambda, admitted by the memory rule; record-system check; waits for all
  local LAMS=$1 I0=$2 i=$2 n=0 pids=() ts=() L j k now
  step "scan starts: D $D, lambda $LAMS, files p$I0.., one process per lambda, 1 thread each, nice $NI, --b12=rust --b12_threads=1, at most $MAXP scanner processes at once"
  touch $PRIO
  for L in ${LAMS//,/ }; do
    bg_admit one_scan $L $i
    pids+=($ADMIT_PID); ts+=($(date +%s)); step "lambda $L (p$i) started, pid $ADMIT_PID, after waiting ${ADMIT_WAITED}s for a slot"
    i=$((i+1)); n=$((n+1))
  done
  rm -f $PRIO
  while true; do   # each started process prints the record system within 2400 s or the group is killed
    k=0; now=$(date +%s)
    for j in $(seq 0 $((n-1))); do
      f=scan_${TAG}_p$((I0+j)).raw
      if grep -q 'NOT the record system' $f 2>/dev/null; then pkill -f "d18_secant.py scan $OUT/in/$RN"; wait "${pids[@]}"; stop "$f: NOT the record system; the scans were killed"; fi
      if grep -q ': the record system' $f 2>/dev/null; then k=$((k+1))
      elif [ $((now - ts[j])) -gt 2400 ] || ! kill -0 ${pids[j]} 2>/dev/null; then pkill -f "d18_secant.py scan $OUT/in/$RN"; wait "${pids[@]}"; stop "$f: no record-system line within 2400 s or the process ended (see $f)"; fi
    done
    [ $k = $n ] && break; sleep 20
  done
  : > recsys_${TAG}_p$I0.txt; for j in $(seq 0 $((n-1))); do grep -h 'the record system' scan_${TAG}_p$((I0+j)).raw >> recsys_${TAG}_p$I0.txt; done
  step "record-system lines (p$I0..): $(grep -c 'NOT the record system' recsys_${TAG}_p$I0.txt) NOT, $(grep -c ': the record system' recsys_${TAG}_p$I0.txt) of $n ok: $(head -1 recsys_${TAG}_p$I0.txt | cut -c1-200)"
  wait "${pids[@]}"
  for j in $(seq 0 $((n-1))); do grep -hE 'the record system|block 12 by ellrs|Elapsed|Maximum resident' scan_${TAG}_p$((I0+j)).raw | head -4 >> steps.txt; done
  [ "$(grep -c "\[$TAG\] lambda .* exit 0" steps.txt)" -ge $((I0 + n)) ] || stop "a scan did not exit 0"
}
read_scans() {   # read_scans LO HI: read_lower and the reader over scan_r3 (all points so far)
  ( cd in; { echo "== r3: read_lower.py scan_r3 $1 $2"; $PY -I read_lower.py $OUT/scan_r3 $1 $2; echo "(exit $?)"; } > $OUT/read_lower_r3.txt 2>&1 )
  $PY -I results_r3.py scan scan_r3 > results_r3.md 2> results_r3.err; return $?
}
mkdir -p scan_$TAG
t0=$(date +%s)
scan 0.115,0.125,0.135,0.145 0
step "scan (four points) done: $(( $(date +%s) - t0 )) s"
read_scans 0.115 0.145; rc=$?
step "results_r3.py scan (four points) exit $rc (0 a bracket, 2 no robust change), results_r3.md"
if [ $rc = 2 ]; then
  step "no robust change in 0.115 .. 0.145: widening to 0.105 and 0.155 (t5's order), nothing further"
  scan 0.105,0.155 4
  read_scans 0.105 0.155; rc=$?
  step "results_r3.py scan (six points) exit $rc"
  if [ $rc = 2 ]; then echo "$TAG DONE $(stamp) UTC, no robust change in 0.105 .. 0.155 (report and wait)" > DONE_$TAG.txt; step "done: no robust change in the six points, no secant"; exit 0; fi
fi
[ $rc = 0 ] || stop "results_r3.py scan exit $rc"
PAIR=$($PY -I results_r3.py scan scan_r3 --pair); LO=${PAIR% *}; HI=${PAIR#* }
cat scan_r3/scan_${DS}_p*.jsonl > scan_r3_all.jsonl
step "secant starts: d18_secant.py run $RN $SN $D $LO $HI secant_r3.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --ends=scan_r3_all.jsonl --pin=$SB,$RB"
t0=$(date +%s)
one_secant() { ( cd $WTM && PYTHONPATH=$SITE nice -n $NI /usr/bin/time -v $PY -u $WTM/d18_secant.py run $OUT/in/$RN $OUT/in/$SN $D $LO $HI $OUT/secant_r3.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --ends=$OUT/scan_r3_all.jsonl --pin=$SB,$RB > $OUT/secant_r3.log 2>&1 ); }
bg_admit one_secant; wait $ADMIT_PID; rs=$?
step "secant exit $rs (0 tol, 4 maxev or non-robust, 2 refused, 3 not the record system), $(( $(date +%s) - t0 )) s; $(tail -1 secant_r3.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
$PY -I results_r3.py read scan_r3 --secant=secant_r3.jsonl > results_r3_secant.md 2> results_r3_secant.err; rr=$?
step "results_r3.py read exit $rr (0 formed, 4 the secant record is not read), results_r3_secant.md"
echo "$TAG DONE $(stamp) UTC, secant exit $rs, reading exit $rr" > DONE_$TAG.txt
step "done"
exit 0
}
