#!/bin/bash
# #1104's second run (t5's order, comment 7226665371): after the kappa 0.5 re-solve passed its bars (DONE_resolve.txt PASS), scan the re-solved state on the Rust block 12 at
# lambda -0.020, -0.005, +0.010, +0.025 (one process each, 1 thread, nice 10), widen to -0.035 and +0.040 if no robust change (t5), then `run` at tol 5e-5 on the first robust change
# (--ends takes the scan's two end records), then the reading against the kappa 0.7 re-root (results_1104.py read; exit 4 if that secant has not ended, then it is run by hand).
# usage: run_scan1104.sh         Stops at the first failure (STOP_scan050.txt); DONE_scan050.txt when it ends. No further widening.
# Priority (t5): while R3's driver (I1101-dh170, unit i1101r3) holds /tmp/dh170_prio_r3 this driver starts no scan process.
# Memory rule (scan_admit.sh, also used by I1101-dh170's R3 driver): at most 4 scanner processes on the machine while ell_refine.py runs, 5 otherwise; a process waits for a slot.
# Environment overrides (OUT WT WTM SITE PY DRY) are only for the dry-run test with a fake scanner; DRY skips the pins of the real worktree and the d18_secant selftests.
{
: "${OUT:=/home/nathan/Source/choptuik-large-d-raw-p4/I1104-dh170}"
: "${WT:=/home/nathan/Source/choptuik-large-d-1101k}"
: "${WTM:=$WT/solver/matter}"
: "${SITE:=/home/nathan/Source/ellrs-site-1102}"
: "${PY:=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python}"
: "${DRY:=}"
D=23.125; NI=10
NEW=l1kc127k050dh170d23125; SF=sol_${NEW}_D23.1250.npy; RF=$NEW.jsonl
TAG=scan050
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
head -1 DONE_resolve.txt | grep -q '^PASS' || stop "DONE_resolve.txt is not PASS"
[ "$(tail -1 $RF | jq -r '(.F <= 5e-10) and (.steps >= 5855*0.98) and (.steps <= 5855*1.02) and (.kappa == 0.5) and (.kc == 127) and (.D == 23.125)')" = true ] || stop "the record of the re-solve does not meet the bars"
SB=$(blob $SF); RB=$(blob $RF)
if [ -z "$DRY" ]; then
[ "$(git -C $WT rev-parse --short=8 HEAD)" = f56f91d2 ] && [ -z "$(git -C $WT status --short solver | head -1)" ] || stop "the scanner worktree is not f56f91d2 or not clean"
[ "$(blob $WTM/d18_secant.py)" = 2f3ee874 ] && [ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "d18_secant.py is not 2f3ee874 or ell_b12rs.py not a1fff74f"
[ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] && [ "$(blob results_1104.py)" = a1dd91ba ] || stop "read_lower.py, its change finder or results_1104.py is not the pinned blob"
fi
[ "$(blob scan_admit.sh)" = e61f8891 ] || stop "scan_admit.sh is not e61f8891"
. $OUT/scan_admit.sh
[ -e scan_050/scan_D23.125_p0.jsonl ] && stop "scan_050/scan_D23.125_p0.jsonl exists: not overwriting"
step "pins ok: re-solved state $SB, record $RB (|F| and steps in the bars), scanner worktree f56f91d2 (d18_secant.py 2f3ee874), read_lower.py 89309d3c, results_1104.py a1dd91ba; nice $NI"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
if [ -z "$DRY" ]; then
cd $WTM
nice -n $NI $PY -I d18_secant.py selftest > $OUT/selftests/selftest_secant_scan050.txt 2>&1; e0=$?
nice -n $NI $PY -I d18_secant.py selftest --mutate=half > $OUT/selftests/selftest_secant_scan050_half.txt 2>&1; e1=$?
nice -n $NI $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftests/selftest_secant_scan050_norobust.txt 2>&1; e2=$?
nice -n $NI $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftests/selftest_secant_scan050_nosigncheck.txt 2>&1; e3=$?
cd $OUT
step "d18_secant.py selftest exit $e0 (0 wanted); mutations half exit $e1, norobust exit $e2, nosigncheck exit $e3 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] && [ $e3 = 1 ] || stop "a d18_secant.py selftest or mutation did not read as written"
fi
one_scan() {   # one_scan LAM I
  ( cd $WTM && PYTHONPATH=$SITE nice -n $NI /usr/bin/time -v $PY -u $WTM/d18_secant.py scan $OUT/$RF $OUT/$SF $D $1 $OUT/scan_050/scan_D23.125_p$2.jsonl --b12=rust --b12_threads=1 --pin=$SB,$RB > $OUT/scan_050_p$2.raw 2>&1
    rc=$?; echo "$(stamp) UTC [$TAG] lambda $1 exit $rc" >> $OUT/steps.txt )
}
scan() {   # scan LAMS I0: one process per lambda, admitted by the memory rule (scan_admit.sh); record-system check; waits for all
  local LAMS=$1 I0=$2 i=$2 n=0 pids=() ts=() L j k now f
  step "scan starts: D $D, lambda $LAMS, files p$I0.., one process per lambda, 1 thread each, nice $NI, --b12=rust --b12_threads=1, scanner processes capped by the memory rule"
  for L in ${LAMS//,/ }; do
    while [ -f /tmp/dh170_prio_r3 ] && systemctl --user is-active --quiet i1101r3; do sleep 30; done   # t5: R3's scan goes first (run_scan_r3.sh holds the file while it starts its scans)
    bg_admit one_scan $L $i
    pids+=($ADMIT_PID); ts+=($(date +%s)); step "lambda $L (p$i) started, pid $ADMIT_PID, after waiting ${ADMIT_WAITED}s for a slot"
    i=$((i+1)); n=$((n+1))
  done
  while true; do   # each started process prints the record system within 2400 s or the group is killed
    k=0; now=$(date +%s)
    for j in $(seq 0 $((n-1))); do
      f=scan_050_p$((I0+j)).raw
      if grep -q 'NOT the record system' $f 2>/dev/null; then pkill -f "d18_secant.py scan $OUT/$RF"; wait "${pids[@]}"; stop "$f: NOT the record system; the scans were killed"; fi
      if grep -q ': the record system' $f 2>/dev/null; then k=$((k+1))
      elif [ $((now - ts[j])) -gt 2400 ] || ! kill -0 ${pids[j]} 2>/dev/null; then pkill -f "d18_secant.py scan $OUT/$RF"; wait "${pids[@]}"; stop "$f: no record-system line within 2400 s or the process ended (see $f)"; fi
    done
    [ $k = $n ] && break; sleep 20
  done
  : > recsys_050_p$I0.txt; for j in $(seq 0 $((n-1))); do grep -h 'the record system' scan_050_p$((I0+j)).raw >> recsys_050_p$I0.txt; done
  step "record-system lines (p$I0..): $(grep -c 'NOT the record system' recsys_050_p$I0.txt) NOT, $(grep -c ': the record system' recsys_050_p$I0.txt) of $n ok: $(head -1 recsys_050_p$I0.txt | cut -c1-200)"
  wait "${pids[@]}"
  for j in $(seq 0 $((n-1))); do grep -hE 'the record system|block 12 by ellrs|Elapsed|Maximum resident' scan_050_p$((I0+j)).raw | head -4 >> steps.txt; done
  [ "$(grep -c "\[$TAG\] lambda .* exit 0" steps.txt)" -ge $((I0 + n)) ] || stop "a scan did not exit 0"
}
read_scans() {   # read_scans LO HI: read_lower and the reader over scan_050
  ( cd in; { echo "== scan050: read_lower.py scan_050 $1 $2"; $PY -I read_lower.py $OUT/scan_050 $1 $2; echo "(exit $?)"; } > $OUT/read_lower_050.txt 2>&1 )
  $PY -I results_1104.py scan scan_050 > results_050.md 2> results_050.err; return $?
}
t0=$(date +%s)
scan -0.020,-0.005,0.010,0.025 0
step "scan (four points) done: $(( $(date +%s) - t0 )) s"
read_scans -0.020 0.025; rc=$?
step "results_1104.py scan (four points) exit $rc (0 a bracket, 2 no robust change), results_050.md"
if [ $rc = 2 ]; then
  step "no robust change in -0.020 .. +0.025: widening to -0.035 and +0.040 (t5's order), nothing further"
  scan -0.035,0.040 4
  read_scans -0.035 0.040; rc=$?
  step "results_1104.py scan (six points) exit $rc"
  if [ $rc = 2 ]; then echo "scan050 DONE $(stamp) UTC, no robust change in -0.035 .. +0.040 (report and wait)" > DONE_scan050.txt; step "done: no robust change in the six points, no secant"; exit 0; fi
fi
[ $rc = 0 ] || stop "results_1104.py scan exit $rc"
PAIR=$($PY -I results_1104.py scan scan_050 --pair); LO=${PAIR% *}; HI=${PAIR#* }
cat scan_050/scan_D23.125_p*.jsonl > scan_050_all.jsonl
step "secant starts: d18_secant.py run $RF $SF $D $LO $HI secant_050.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --ends=scan_050_all.jsonl --pin=$SB,$RB"
t0=$(date +%s)
one_secant() { ( cd $WTM && PYTHONPATH=$SITE nice -n $NI /usr/bin/time -v $PY -u $WTM/d18_secant.py run $OUT/$RF $OUT/$SF $D $LO $HI $OUT/secant_050.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --ends=$OUT/scan_050_all.jsonl --pin=$SB,$RB > $OUT/secant_050.log 2>&1 ); }
bg_admit one_secant; wait $ADMIT_PID; rs=$?
step "secant exit $rs (0 tol, 4 maxev or non-robust, 2 refused, 3 not the record system), $(( $(date +%s) - t0 )) s; $(tail -1 secant_050.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
$PY -I results_1104.py read --scan070=scan_070 --scan050=scan_050 --s070=secant_070.jsonl --s050=secant_050.jsonl > results_1104_read.md 2> results_1104_read.err; rr=$?
step "results_1104.py read exit $rr (0 formed, 4 a record not read: the kappa 0.7 secant may still run)"
echo "scan050 DONE $(stamp) UTC, secant exit $rs, reading exit $rr" > DONE_scan050.txt
step "done"
exit 0
}
